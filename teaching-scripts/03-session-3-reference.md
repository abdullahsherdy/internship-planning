# Session 3 Instructor Reference — Full Project Build (All Entities, Concrete Repositories)

**Scope change record (2026-08-02, rev 2):** Session 2 did not reach project creation. Session 3 now builds the **complete Task Tracker data layer in one session**: solution creation, full database design, **both entities (Project + TaskItem)**, EF Core with one reviewed migration, and a **simple concrete repository per aggregate**. Later sessions deepen this same codebase (LINQ/projection internals, services, testing) rather than adding entities.

The repository decision amends ADR-004 minimally: **one interface + one class per aggregate. No `Repository<T>`, no Unit of Work, no `IQueryable` leaks.** `SaveChangesAsync` inside the repository is the unit of work.

Everything below conforms to the frozen API contract (plan_v2 §6): endpoints, status codes, camelCase JSON, Problem Details errors, offset pagination (`pageSize` max 50, default 10).

---

## 1. Required Packages and Tools

Run inside `src/TaskTracker.Api/`:

```bash
dotnet add package Microsoft.EntityFrameworkCore.Sqlite
dotnet add package Microsoft.EntityFrameworkCore.Design
```

| Package / Tool | What it's for | Notes |
|---|---|---|
| `Microsoft.EntityFrameworkCore.Sqlite` | SQLite database provider (pulls in EF Core core) | The only provider we teach; SQL Server optional stretch (ADR-002) |
| `Microsoft.EntityFrameworkCore.Design` | Design-time services for migration tooling | Required or `dotnet ef migrations add` fails |
| `dotnet-ef` (global tool) | CLI that creates/applies migrations | `dotnet tool install --global dotnet-ef` |
| `Microsoft.EntityFrameworkCore.Tools` | **Only** for Visual Studio Package Manager Console (`Add-Migration`) | Optional — standardize on the `dotnet ef` CLI so every machine shares one workflow |

**Verify:** `dotnet ef --version` and `dotnet build` both succeed.

---

## 2. Solution Architecture

```bash
dotnet new sln -n TaskTracker
dotnet new webapi -o src/TaskTracker.Api --use-controllers
dotnet sln add src/TaskTracker.Api
```

```
TaskTracker/
├── TaskTracker.sln
├── api-contract.md                    # frozen copy of plan_v2 §6
└── src/
    └── TaskTracker.Api/
        ├── TaskTracker.Api.csproj     # <Nullable>enable</Nullable> stays on
        ├── Program.cs                 # DI: DbContext + both repositories
        ├── TaskTracker.Api.http       # every contract request
        ├── Controllers/
        │   ├── HealthController.cs
        │   ├── ProjectsController.cs  # depends on IProjectRepository
        │   └── TasksController.cs     # depends on ITaskRepository (+ IProjectRepository for 404s)
        ├── Contracts/                 # DTO records only — the API's public shape
        │   ├── ProjectContracts.cs
        │   ├── TaskContracts.cs
        │   └── PagedResponse.cs
        ├── Domain/                    # entities + rules; zero ASP.NET/EF usings
        │   ├── Project.cs
        │   ├── TaskItem.cs
        │   └── TaskStatus.cs
        └── Data/
            ├── AppDbContext.cs
            ├── Migrations/            # generated; ALWAYS read before applied
            └── Repositories/
                ├── IProjectRepository.cs
                ├── ProjectRepository.cs
                ├── ITaskRepository.cs
                └── TaskRepository.cs
```

**Rules (state once, enforce in review):**

- `Contracts/` types cross the HTTP boundary; `Domain/` types never do (contract §6.4).
- `Domain/` has zero `using Microsoft.AspNetCore.*` or `Microsoft.EntityFrameworkCore.*`.
- One concrete repository per aggregate root. Repositories return entities/primitives, never `IQueryable`.
- One migration per PR, read as text before `database update`. Today produces exactly one: `InitialCreate` with both tables.

---

## 3. Database Design (built in full today)

### 3.1 ERD

```
Projects                          Tasks
+---------------------+           +---------------------------+
| Id INT PK           |<---+      | Id INT PK                 |
| Name TEXT NN (100)  |    |      | ProjectId INT NN FK ------+  ON DELETE CASCADE
|   (UNIQUE: stretch) |    +------|                           |
| Description TEXT    |           | Title TEXT NN (200)       |
|   NULL (500)        |           | Description TEXT NULL     |
| CreatedAtUtc TEXT NN|           | Status TEXT NN (20)       |
+---------------------+           |   'Todo'|'InProgress'     |
                                  |   |'Done'                 |
    1 ──────────── many           | DueDate TEXT NULL         |
                                  | CreatedAtUtc TEXT NN      |
                                  +---------------------------+
Indexes:
  IX_Tasks_ProjectId_Status (ProjectId, Status)   ← created today; EXPLAIN demo stays in S4
  UX_Projects_Name (unique)                       ← stretch, as a SECOND migration
```

### 3.2 Design decisions to narrate

| Decision | Choice | Why (say this out loud) |
|---|---|---|
| Primary keys | `int` identity | Teaching simplicity; GUIDs discussed as a tradeoff, not adopted (contract §6.1) |
| Relationship | 1 project → many tasks via `Tasks.ProjectId` FK | Normalization payoff: each fact lives once, tasks *point* |
| Delete behavior | `ON DELETE CASCADE` | A *decision*, not a default — convenience vs. accidental mass-delete; we choose cascade and test it |
| Enum storage | `Status` as TEXT (`HasConversion<string>()`) | DB stays human-readable; C# enum ordering stops mattering |
| Dates | `CreatedAtUtc` DateTime UTC; `DueDate` as `DateOnly?` | A due date is a date, not a moment — type precision + nullability in one example |
| Nullability | `Description`, `DueDate` NULL; all else NOT NULL | Schema NULL ≡ C# `?` — same question, two type systems that must agree |
| Constraints in the DB too | max lengths, NOT NULL, FK, index | The API isn't the only possible writer; DB constraints can't be bypassed by a bug |

---

## 4. Domain (all entities — complete today)

```csharp
// Domain/TaskStatus.cs
public enum TaskStatus
{
    Todo = 0,
    InProgress = 1,
    Done = 2
}

// Domain/Project.cs
public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string? Description { get; set; }
    public DateTime CreatedAtUtc { get; set; }

    public List<TaskItem> Tasks { get; set; } = new();
}

// Domain/TaskItem.cs
public class TaskItem
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public Project Project { get; set; } = null!;   // required navigation — narrate the null! once

    public string Title { get; set; } = "";
    public string? Description { get; set; }
    public TaskStatus Status { get; set; } = TaskStatus.Todo;
    public DateOnly? DueDate { get; set; }
    public DateTime CreatedAtUtc { get; set; }
}
```

Note: `System.Threading.Tasks.TaskStatus` exists — if trainees hit the ambiguity, the fix is `using TaskStatus = TaskTracker.Api.Domain.TaskStatus;` (or fully qualify). Expect this question; it's a good namespaces moment.

---

## 5. Contracts (frozen shapes — plan_v2 §6)

```csharp
// Contracts/PagedResponse.cs
public record PagedResponse<T>(IReadOnlyList<T> Items, int Page, int PageSize, int TotalCount);

// Contracts/ProjectContracts.cs
public record ProjectResponse(int Id, string Name, string? Description, DateTime CreatedAtUtc, int TaskCount);
public record CreateProjectRequest([property: Required, property: StringLength(100, MinimumLength = 1)] string Name,
                                   [property: StringLength(500)] string? Description);
public record UpdateProjectRequest([property: Required, property: StringLength(100, MinimumLength = 1)] string Name,
                                   [property: StringLength(500)] string? Description);

// Contracts/TaskContracts.cs
public record TaskResponse(int Id, int ProjectId, string Title, string? Description,
                           string Status, DateOnly? DueDate, DateTime CreatedAtUtc);
public record CreateTaskRequest([property: Required, property: StringLength(200, MinimumLength = 1)] string Title,
                                string? Description, DateOnly? DueDate);
public record ChangeTaskStatusRequest([property: Required] string NewStatus);
```

Narration hooks: `TaskCount` exists only in the DTO — first proof the contract isn't the entity. `Status` is a `string` in the contract but an enum in the domain — the mapping is explicit and visible.

---

## 6. Data Layer

### 6.1 DbContext (both entities)

```csharp
// Data/AppDbContext.cs
public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<TaskItem> Tasks => Set<TaskItem>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<Project>(e =>
        {
            e.Property(p => p.Name).IsRequired().HasMaxLength(100);
            e.Property(p => p.Description).HasMaxLength(500);
            // Stretch (second migration): e.HasIndex(p => p.Name).IsUnique();
        });

        b.Entity<TaskItem>(e =>
        {
            e.Property(t => t.Title).IsRequired().HasMaxLength(200);
            e.Property(t => t.Status).HasConversion<string>().HasMaxLength(20);
            e.HasOne(t => t.Project)
             .WithMany(p => p.Tasks)
             .HasForeignKey(t => t.ProjectId)
             .OnDelete(DeleteBehavior.Cascade);
            e.HasIndex(t => new { t.ProjectId, t.Status });
        });
    }
}
```

Map every fluent line to the hand-drawn schema: `IsRequired` = NOT NULL, `HasMaxLength` = the constraint, `HasOne/WithMany/HasForeignKey` = the FK arrow, `OnDelete(Cascade)` = the vote you took.

### 6.2 Project repository

```csharp
// Data/Repositories/IProjectRepository.cs
public interface IProjectRepository
{
    Task<(List<Project> Items, int TotalCount)> GetPageAsync(int page, int pageSize, CancellationToken ct = default);
    Task<Project?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<bool> ExistsAsync(int id, CancellationToken ct = default);
    Task AddAsync(Project project, CancellationToken ct = default);
    Task UpdateAsync(Project project, CancellationToken ct = default);
    Task<bool> DeleteAsync(int id, CancellationToken ct = default);
}

// Data/Repositories/ProjectRepository.cs
public class ProjectRepository(AppDbContext db) : IProjectRepository
{
    public async Task<(List<Project> Items, int TotalCount)> GetPageAsync(int page, int pageSize, CancellationToken ct = default)
    {
        var total = await db.Projects.CountAsync(ct);
        var items = await db.Projects
            .AsNoTracking()
            .Include(p => p.Tasks)              // for TaskCount; S4 replaces with projection + explains why
            .OrderBy(p => p.Id)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);
        return (items, total);
    }

    public Task<Project?> GetByIdAsync(int id, CancellationToken ct = default) =>
        db.Projects.Include(p => p.Tasks).FirstOrDefaultAsync(p => p.Id == id, ct);

    public Task<bool> ExistsAsync(int id, CancellationToken ct = default) =>
        db.Projects.AnyAsync(p => p.Id == id, ct);

    public async Task AddAsync(Project project, CancellationToken ct = default)
    {
        db.Projects.Add(project);
        await db.SaveChangesAsync(ct);
    }

    public async Task UpdateAsync(Project project, CancellationToken ct = default) =>
        await db.SaveChangesAsync(ct);   // entity tracked from GetByIdAsync

    public async Task<bool> DeleteAsync(int id, CancellationToken ct = default)
    {
        var project = await db.Projects.FindAsync([id], ct);
        if (project is null) return false;
        db.Projects.Remove(project);     // cascade removes its tasks — the tested decision
        await db.SaveChangesAsync(ct);
        return true;
    }
}
```

Honesty note to narrate: `Include(p => p.Tasks)` loads whole task lists just to count them — deliberately naive today. Session 4's projection lesson fixes it and *measures* the difference. Write the TODO in the code live: `// TODO(S4): project TaskCount instead of loading tasks`.

### 6.3 Task repository

```csharp
// Data/Repositories/ITaskRepository.cs
public interface ITaskRepository
{
    Task<(List<TaskItem> Items, int TotalCount)> GetPageForProjectAsync(
        int projectId, TaskStatus? status, int page, int pageSize, CancellationToken ct = default);
    Task<TaskItem?> GetByIdAsync(int id, CancellationToken ct = default);
    Task AddAsync(TaskItem task, CancellationToken ct = default);
    Task UpdateAsync(TaskItem task, CancellationToken ct = default);
}

// Data/Repositories/TaskRepository.cs
public class TaskRepository(AppDbContext db) : ITaskRepository
{
    public async Task<(List<TaskItem> Items, int TotalCount)> GetPageForProjectAsync(
        int projectId, TaskStatus? status, int page, int pageSize, CancellationToken ct = default)
    {
        var query = db.Tasks.AsNoTracking().Where(t => t.ProjectId == projectId);
        if (status is not null) query = query.Where(t => t.Status == status);

        var total = await query.CountAsync(ct);
        var items = await query
            .OrderBy(t => t.Id)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);
        return (items, total);
    }

    public Task<TaskItem?> GetByIdAsync(int id, CancellationToken ct = default) =>
        db.Tasks.FirstOrDefaultAsync(t => t.Id == id, ct);

    public async Task AddAsync(TaskItem task, CancellationToken ct = default)
    {
        db.Tasks.Add(task);
        await db.SaveChangesAsync(ct);
    }

    public async Task UpdateAsync(TaskItem task, CancellationToken ct = default) =>
        await db.SaveChangesAsync(ct);
}
```

Note the filter composition inside the repository — the `IQueryable` is composed *and executed* here; it never escapes the interface. That's the guardrail in action.

---

## 7. Controllers (frozen contract endpoints)

### 7.1 ProjectsController

```csharp
[ApiController]
[Route("api/projects")]
public class ProjectsController(IProjectRepository repo) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<PagedResponse<ProjectResponse>>> GetAll(
        [FromQuery, Range(1, int.MaxValue)] int page = 1,
        [FromQuery, Range(1, 50)] int pageSize = 10,
        CancellationToken ct = default)
    {
        var (items, total) = await repo.GetPageAsync(page, pageSize, ct);
        return Ok(new PagedResponse<ProjectResponse>(items.Select(ToResponse).ToList(), page, pageSize, total));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProjectResponse>> GetById(int id, CancellationToken ct)
    {
        var project = await repo.GetByIdAsync(id, ct);
        return project is null ? NotFound() : Ok(ToResponse(project));
    }

    [HttpPost]
    public async Task<ActionResult<ProjectResponse>> Create(CreateProjectRequest request, CancellationToken ct)
    {
        var project = new Project
        {
            Name = request.Name,
            Description = request.Description,
            CreatedAtUtc = DateTime.UtcNow
        };
        await repo.AddAsync(project, ct);
        return CreatedAtAction(nameof(GetById), new { id = project.Id }, ToResponse(project));
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, UpdateProjectRequest request, CancellationToken ct)
    {
        var project = await repo.GetByIdAsync(id, ct);
        if (project is null) return NotFound();
        project.Name = request.Name;
        project.Description = request.Description;
        await repo.UpdateAsync(project, ct);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id, CancellationToken ct) =>
        await repo.DeleteAsync(id, ct) ? NoContent() : NotFound();

    private static ProjectResponse ToResponse(Project p) =>
        new(p.Id, p.Name, p.Description, p.CreatedAtUtc, p.Tasks.Count);
}
```

### 7.2 TasksController (nested list/create + status change)

```csharp
[ApiController]
public class TasksController(ITaskRepository tasks, IProjectRepository projects) : ControllerBase
{
    [HttpGet("api/projects/{projectId}/tasks")]
    public async Task<ActionResult<PagedResponse<TaskResponse>>> GetForProject(
        int projectId,
        [FromQuery] string? status,
        [FromQuery, Range(1, int.MaxValue)] int page = 1,
        [FromQuery, Range(1, 50)] int pageSize = 10,
        CancellationToken ct = default)
    {
        if (!await projects.ExistsAsync(projectId, ct)) return NotFound();

        TaskStatus? statusFilter = null;
        if (status is not null)
        {
            if (!Enum.TryParse<TaskStatus>(status, ignoreCase: true, out var parsed))
                return BadRequest($"Unknown status '{status}'. Valid: Todo, InProgress, Done.");
            statusFilter = parsed;
        }

        var (items, total) = await tasks.GetPageForProjectAsync(projectId, statusFilter, page, pageSize, ct);
        return Ok(new PagedResponse<TaskResponse>(items.Select(ToResponse).ToList(), page, pageSize, total));
    }

    [HttpPost("api/projects/{projectId}/tasks")]
    public async Task<ActionResult<TaskResponse>> Create(int projectId, CreateTaskRequest request, CancellationToken ct)
    {
        if (!await projects.ExistsAsync(projectId, ct)) return NotFound();

        var task = new TaskItem
        {
            ProjectId = projectId,
            Title = request.Title,
            Description = request.Description,
            DueDate = request.DueDate,
            CreatedAtUtc = DateTime.UtcNow
        };
        await tasks.AddAsync(task, ct);
        return CreatedAtAction(nameof(GetForProject), new { projectId }, ToResponse(task));
    }

    [HttpPatch("api/tasks/{id}/status")]
    public async Task<ActionResult<TaskResponse>> ChangeStatus(int id, ChangeTaskStatusRequest request, CancellationToken ct)
    {
        if (!Enum.TryParse<TaskStatus>(request.NewStatus, ignoreCase: true, out var newStatus))
            return BadRequest($"Unknown status '{request.NewStatus}'. Valid: Todo, InProgress, Done.");

        var task = await tasks.GetByIdAsync(id, ct);
        if (task is null) return NotFound();

        task.Status = newStatus;          // transition RULES (e.g. Done→Todo?) arrive S5 as TaskStatusService
        await tasks.UpdateAsync(task, ct);
        return Ok(ToResponse(task));
    }

    private static TaskResponse ToResponse(TaskItem t) =>
        new(t.Id, t.ProjectId, t.Title, t.Description, t.Status.ToString(), t.DueDate, t.CreatedAtUtc);
}
```

Deferred on purpose (say so out loud): status **transition rules** (`400` invalid transition) are Session 5's service lesson — today any valid status parses and is accepted. The `DueDate` not-in-the-past custom attribute is also S5.

---

## 8. Program.cs Wiring

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>(o =>
    o.UseSqlite(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddScoped<IProjectRepository, ProjectRepository>();
builder.Services.AddScoped<ITaskRepository, TaskRepository>();

var app = builder.Build();
app.MapControllers();
app.Run();
```

```jsonc
// appsettings.json
{ "ConnectionStrings": { "Default": "Data Source=tasktracker.db" } }
```

Lifetimes: `AddDbContext` = Scoped (one context per request); repositories **must** also be Scoped. A Singleton repo holding a Scoped DbContext is the classic DI bug — AI generators produce it; now trainees can spot it.

---

## 9. Migration Ritual (one migration, both tables)

```bash
dotnet ef migrations add InitialCreate     # 1. create
# 2. OPEN Data/Migrations/*_InitialCreate.cs — READ ALOUD: two CreateTable, the FK
#    with onDelete: CASCADE, the composite index. Every line maps to the drawing.
dotnet ef database update                  # 3. only then apply
```

Inspect `tasktracker.db` in the viewer — both tables, physically. **Cascade proof (the tested decision):** insert a project + 2 tasks via the API, `DELETE /api/projects/{id}`, then `SELECT COUNT(*) FROM Tasks;` in the viewer → 0. "The DB honored the decision we voted on."

Review rule: a migration review asks first — **does any operation destroy data?** (`DropColumn`, `DropTable`, some `AlterColumn`.)

Common failures: `dotnet-ef` not installed → command not found; wrong directory (solution vs project folder) → "no project found"; missing `Design` package → its explicit error; "no such table" at runtime → migration never applied; `.db` locked on Windows → close the viewer before `database update`.

---

## 10. Session 3 Definition of Done

| Item | Done today | Deferred (same codebase) |
|---|---|---|
| Solution + folders + health endpoint | ✅ | — |
| Both entities + enum, DbContext, one reviewed `InitialCreate` migration | ✅ | additive migrations (stretch: unique name) |
| `IProjectRepository` / `ITaskRepository` + implementations | ✅ | faked in unit tests, S6 |
| Full Project CRUD with paging per contract | ✅ | — |
| Task list (status filter + paging), task create, PATCH status | ✅ | transition rules → S5 `TaskStatusService` |
| Cascade delete proven in the viewer | ✅ | automated cascade test, S6 |
| Restart-survival proof (POST → restart → GET) | ✅ | — |
| `Include` for TaskCount (naive, TODO in code) | ✅ | `Select` projection + query log + N+1 demo, S4 |
| Error shape (Problem Details from `[ApiController]`) | ✅ automatic | exception middleware / no naked 500s, S5 |

This is ambitious for 3 hours: the timing that makes it fit is in the script — Tasks endpoints are live-coded fast *by repeating the Project pattern* ("same anatomy: validate → repo → map → status code"), and the pairs block builds TasksController while Projects was built together.
