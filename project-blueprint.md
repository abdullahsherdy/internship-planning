# Task Tracker - Technical Blueprint

**Purpose:** the buildable specification of the internship project. `plan_v2.md` says *who builds what, when*; this file says *exactly what gets built*. The instructor reference repo is constructed from this document, top to bottom.

**Companion docs:** contract in `plan_v2.md` §6 (frozen), per-track deliverables in `plan_v2.md` §5, session pacing in `teaching-scripts/`.

---

## 1. The Backend Landscape (Goal 1 — taught, not built)

Trainees must be able to place *what we're building* on the map of *what exists*. Taught as a 10-minute segment in Session 1 (extends the mental-model block) and revisited in Session 8 (deployment discussion). Never implemented beyond the monolith.

### 1.1 The map (draw this in S1)

```
                   "Where does backend code run?"
                              |
    +----------------+----------------+---------------------+
    | Monolith (us)  | Microservices  | Serverless (FaaS)   |
    | one process,   | many processes,| no process you own; |
    | one deploy     | network calls  | functions run       |
    | one database   | between them   | on-demand, billed   |
    |                |                | per invocation      |
    +----------------+----------------+---------------------+
      Task Tracker      "later, when      AWS Lambda /
      lives here         teams & scale     Azure Functions
                         force a split"
```

**Teaching lines (problem→solution):**

- *Problem:* "Our API runs 24/7 even at 3 a.m. with zero users. We pay for idle." → *Serverless answer:* "upload a function, the cloud starts it per request, bills per millisecond. Cost: cold starts, statelessness is forced, and your local `List<Project>` trick is impossible — there is no 'the process'."
- *Problem:* "One team of 200 devs deploying one monolith steps on each other." → *Microservices answer:* "split by business capability. Cost: every method call becomes a network call that can fail."
- **The honest rule:** "You earn the right to split a monolith by first building a good one. That's this internship."

### 1.2 Where it recurs

| Session | Touchpoint |
|---|---|
| S1 | The map above; "our API is a modular monolith of size 1" |
| S3 | "Serverless + SQLite don't mix — why?" (file on local disk vs ephemeral compute) |
| S8 | Deployment targets discussion: VM vs container vs PaaS vs FaaS; where a Task Tracker would really go (PaaS) and when Lambda would win (spiky, per-request workloads) |

---

## 2. Delivery Simulation: Agile Frame (Goal 3 — lived, not lectured)

The internship *is run as* a 4-sprint product delivery. Trainees learn Agile by being inside one, with 15 minutes of total lecture across 8 sessions.

### 2.1 The frame

| Element | Implementation in the internship |
|---|---|
| Product | Task Tracker API v1 (contract = plan_v2 §6) |
| Product Owner | Instructor (you) — owns backlog, accepts/rejects stories |
| Team | Trainees; pairs are "feature teams" per session |
| Sprint | 2 sessions = 1 sprint (4 sprints total) |
| Sprint planning | First 5 min of each sprint's first session: PO presents the sprint's stories |
| Daily standup | The retrieval quiz + blockers slot plays this role (say so explicitly in S1) |
| Sprint review | The checkpoint artifact = the demo to the PO |
| Retrospective | Exit ticket + first 5 min of next session ("what we change this sprint") |
| Board | GitHub Projects board on the instructor repo: `Backlog → Sprint → In Progress → In Review → Done`. Trainees move their own cards |
| Definition of Done | §8.4 — printed, enforced in PR review |

### 2.2 Product backlog (user stories with acceptance criteria)

Stories are written in standard form so trainees see real artifacts. IDs are stable — PRs must reference them (`TT-04: implement create project`).

**Sprint 1 — "It responds" (Sessions 1-2)**

- **TT-01** As an API consumer, I can check the service is alive, so that monitoring is possible.
  *AC:* `GET /api/health` → `200` with status + UTC time.
- **TT-02** As a user, I can list all projects, so that I can see my workspace.
  *AC:* `GET /api/projects` → `200`, array of project DTOs (pagination arrives in TT-08).
- **TT-03** As a user, I can fetch one project by id. *AC:* `200` with DTO; unknown id → `404` Problem Details.
- **TT-04** As a user, I can create a project. *AC:* valid body → `201` + `Location` header + created DTO; `Name` missing/blank/>100 chars → `400` with field errors.
- **TT-05** As a user, I can update and delete a project. *AC:* PUT valid → `204`; DELETE existing → `204`; unknown id → `404`.

**Sprint 2 — "It remembers" (Sessions 3-4)**

- **TT-06** As a user, my projects survive a service restart. *AC:* create → restart process → GET returns it. (EF Core + SQLite + first migration.)
- **TT-07** As a user, I can create tasks inside a project and list them. *AC:* `POST /api/projects/{projectId}/tasks` → `201`; unknown project → `404`; `GET .../tasks` returns only that project's tasks.
- **TT-08** As a user, I can filter tasks by status and page through results. *AC:* `?status=InProgress` filters; envelope `{items, page, pageSize, totalCount}`; `pageSize` > 50 → `400`.
- **TT-09** *(stretch)* As a user, I can sort tasks by an allow-listed field. *AC:* `?sortBy=dueDate` works; `?sortBy=evil` → `400`.

**Sprint 3 — "It's trustworthy" (Sessions 5-6)**

- **TT-10** As a user, task status changes follow the workflow. *AC:* the state machine in §6; invalid transition → `400` Problem Details with explanation.
- **TT-11** As an operator, all failures return Problem Details and are logged. *AC:* no naked 500s; unhandled exception → `500` Problem Details without stack trace in body; log entry contains traceId.
- **TT-12** As the team, business rules are proven by tests. *AC:* unit tests cover every allowed/forbidden transition; integration tests cover one GET happy path and one invalid POST.

**Sprint 4 — "It ships" (Sessions 7-8)**

- **TT-13** As an owner, only I can modify my projects. *AC:* (core: with auth starter) request without token → `401`; other user's project → `403`; own → succeeds.
- **TT-14** As the team, the API documents itself. *AC:* OpenAPI UI shows all endpoints with schemas and status codes; README reproduces setup on a clean machine.
- **TT-15** As the PO, the service passes the release checklist. *AC:* §10 checklist green.

Foundation track works the same stories with starter scaffolds; their sprint commitment is smaller, not different (plan_v2 §5).

---

## 3. Repository and Solution Structure

```
task-tracker/
├── .editorconfig                  # §8.1 — enforced style
├── .gitignore                     # dotnet new gitignore
├── README.md                      # setup: 5 commands, tested on a clean machine
├── AI-NOTES.md                    # verified AI assistance log (per plan.md §7)
├── TaskTracker.sln
├── api-contract.md                # frozen copy of plan_v2 §6
├── docs/
│   ├── decisions.md               # ADR-lite log (seeded from plan_v2 §7)
│   └── schema.png                 # exported ERD (source of truth: §5 below)
├── src/
│   └── TaskTracker.Api/
│       ├── TaskTracker.Api.csproj
│       ├── Program.cs
│       ├── TaskTracker.Api.http   # all contract requests, sectioned per sprint
│       ├── Controllers/
│       │   ├── HealthController.cs
│       │   ├── ProjectsController.cs
│       │   └── TasksController.cs
│       ├── Contracts/             # DTO records only — the API's public shape
│       │   ├── ProjectContracts.cs
│       │   ├── TaskContracts.cs
│       │   └── PagedResponse.cs
│       ├── Domain/                # entities + rules; no framework references
│       │   ├── Project.cs
│       │   ├── TaskItem.cs
│       │   ├── TaskStatus.cs
│       │   └── TaskStatusService.cs   (+ ITaskStatusService) — appears S5
│       └── Data/
│           ├── AppDbContext.cs
│           └── Migrations/        # generated; always reviewed before applied
└── tests/
    └── TaskTracker.Tests/
        ├── TaskTracker.Tests.csproj
        ├── Unit/TaskStatusServiceTests.cs
        └── Integration/
            ├── ApiFactory.cs
            └── ProjectEndpointTests.cs
```

**Folder rules (say them once, enforce in review):**

- `Contracts/` types cross the HTTP boundary; `Domain/` types never do.
- `Domain/` has zero `using Microsoft.AspNetCore.*` — if a domain file needs the framework, the design is wrong.
- One migration per PR, reviewed as text before `database update`.

---

## 4. Domain Model (code-complete)

### 4.1 Entities

```csharp
// Domain/Project.cs
public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string? Description { get; set; }
    public DateTime CreatedAtUtc { get; set; }

    public List<TaskItem> Tasks { get; set; } = new();
}

// Domain/TaskStatus.cs
public enum TaskStatus
{
    Todo = 0,
    InProgress = 1,
    Done = 2
}

// Domain/TaskItem.cs
public class TaskItem
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public Project Project { get; set; } = null!;   // required nav — S4 explains this line

    public string Title { get; set; } = "";
    public string? Description { get; set; }
    public TaskStatus Status { get; set; } = TaskStatus.Todo;
    public DateOnly? DueDate { get; set; }
    public DateTime CreatedAtUtc { get; set; }
}
```

Deliberate choices to narrate: `int` ids (ADR: teaching simplicity), `DateOnly?` for due dates (a date, not a moment — good nullability + type-precision example), enum stored as string in the DB (§5) so the database is human-readable during teaching.

### 4.2 Contracts (DTO records)

```csharp
// Contracts/ProjectContracts.cs
public record ProjectResponse(int Id, string Name, string? Description, DateTime CreatedAtUtc, int TaskCount);
public record CreateProjectRequest(string Name, string? Description);
public record UpdateProjectRequest(string Name, string? Description);

// Contracts/TaskContracts.cs
public record TaskResponse(int Id, int ProjectId, string Title, string? Description,
                           string Status, DateOnly? DueDate, DateTime CreatedAtUtc);
public record CreateTaskRequest(string Title, string? Description, DateOnly? DueDate);
public record ChangeTaskStatusRequest(string NewStatus);

// Contracts/PagedResponse.cs
public record PagedResponse<T>(IReadOnlyList<T> Items, int Page, int PageSize, int TotalCount);
```

Narration hooks: `TaskCount` on `ProjectResponse` exists *only* in the DTO — first proof the contract isn't the entity. `Status` is a `string` in the contract (JSON consumers shouldn't need our enum ordering) but an enum in the domain — the mapping is explicit and visible.

### 4.3 Validation rules (data annotations — deliberately, not FluentValidation)

| Field | Rules |
|---|---|
| `Project.Name` | required, 1-100 chars |
| `Project.Description` | optional, ≤ 500 chars |
| `TaskItem.Title` | required, 1-200 chars |
| `TaskItem.DueDate` | optional; if present, not in the past (custom attribute — S5 exercise) |
| `page` / `pageSize` | ≥ 1; `pageSize` ≤ 50 |
| `status` filter / `NewStatus` | must parse to `TaskStatus` (case-insensitive) → else `400` |

Data annotations keep validation *visible on the DTO* and framework-native. FluentValidation is a stretch comparison, not a dependency (consistent with ADR-004's no-premature-abstraction stance).

---

## 5. Database Design (Goal 4 — design first, optimization honestly)

### 5.1 Schema (drawn by hand in S3 before any EF Core)

```
projects                          task_items
+-----------------+               +----------------------+
| id INT PK       |<---+          | id INT PK            |
| name TEXT NN    |    |          | project_id INT NN FK--+  ON DELETE CASCADE
|   UNIQUE (str.) |    +----------|                       |
| description TEXT|               | title TEXT NN         |
| created_at_utc  |               | description TEXT      |
|   TEXT NN       |               | status TEXT NN        |
+-----------------+               |   CHECK(status IN     |
                                  |   ('Todo','InProgress'|
   1 ────────────── many          |    ,'Done'))          |
                                  | due_date TEXT         |
                                  | created_at_utc TEXT NN|
                                  +----------------------+
   Indexes:
   IX_task_items_project_id_status  (project_id, status)   ← §5.3
   UX_projects_name (stretch)
```

**S3 teaching sequence (problem→solution):** rows with duplicated project fields inside tasks → *normalization* → foreign key → "what stops me deleting a project with tasks?" → cascade as a *decision*, not a default (narrate the tradeoff: convenience vs accidental mass-delete; we choose cascade and *test* it).

### 5.2 EF Core configuration (code-complete)

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
            // Stretch (S3): e.HasIndex(p => p.Name).IsUnique();
        });

        b.Entity<TaskItem>(e =>
        {
            e.Property(t => t.Title).IsRequired().HasMaxLength(200);
            e.Property(t => t.Status).HasConversion<string>().HasMaxLength(20);
            e.HasOne(t => t.Project)
             .WithMany(p => p.Tasks)
             .HasForeignKey(t => t.ProjectId)
             .OnDelete(DeleteBehavior.Cascade);
            e.HasIndex(t => new { t.ProjectId, t.Status });   // §5.3 — the teaching index
        });
    }
}
```

Migration discipline: `dotnet ef migrations add <Name>` → **open and read the generated file aloud** → only then `dotnet ef database update`. The AI practice for S3 is reviewing a migration for accidental drops — this discipline is its setup.

### 5.3 Indexing and query optimization (the honest 30 minutes, Session 4)

Deep query tuning doesn't fit 24 hours. What fits — and sticks — is **one measurable demonstration** that gives trainees the mental model and the tool to continue alone.

**The demo (scripted, S4, after pagination works):**

1. Seed 50,000 tasks across 100 projects (provided seed script — SQLite handles this instantly).
2. Run the hot query without the index:
   ```sql
   EXPLAIN QUERY PLAN
   SELECT * FROM task_items WHERE project_id = 42 AND status = 'InProgress';
   -- → SCAN task_items          (reads all 50,000 rows)
   ```
3. *Problem stated:* "Every request reads the whole table. At 50k rows SQLite hides it; at 50M with 1,000 req/s it's an outage."
4. Add `IX_task_items_project_id_status` via a migration (they *watch an index arrive as a reviewed migration*, reinforcing S3 discipline).
   ```sql
   -- → SEARCH task_items USING INDEX IX_task_items_project_id_status (project_id=? AND status=?)
   ```
5. **The mental model to leave behind:** "An index is a sorted copy of chosen columns that trades write cost and storage for read speed. The database *tells you* whether it used one — never guess, always ask the plan."
6. Composite-order intuition: "why `(project_id, status)` and not `(status, project_id)`? Phone book: sorted by last-name-then-first helps you find 'Ahmed, *' — sorted by first name doesn't." Show the plan difference live.

**Also in S4 (measurable, not theoretical):** the N+1 demo — load projects then `Tasks.Count` in a loop with EF query logging on (101 queries scroll past), then fix with projection (1 query). Trainees *count the queries*.

**Explicitly deferred to the post-internship path (say so):** execution plans on SQL Server, statistics, covering indexes, lock contention, transaction isolation levels. The S4 exit ticket includes: "what question would you ask the query plan at your next job?"

---

## 6. The Business Rule: Task Status State Machine (Session 5's engine)

The one rule complex enough to justify a service, simple enough to hold in one head:

```
        start
          |
          v
   +-> [Todo] --------> [InProgress] <------ reopen ------ [Done]
   |                        |    ^                            ^
   +---- put back ----------+    +--------- complete --------+

   Allowed:  Todo→InProgress, InProgress→Done, InProgress→Todo, Done→InProgress
   Forbidden: Todo→Done  ("work can't be finished before it starts")
             X→X          (no-op transitions rejected — surfaces idempotency discussion)
```

```csharp
// Domain/TaskStatusService.cs
public interface ITaskStatusService
{
    TransitionResult TryTransition(TaskStatus current, TaskStatus target);
}

public record TransitionResult(bool Allowed, string? Reason)
{
    public static TransitionResult Ok() => new(true, null);
    public static TransitionResult Fail(string reason) => new(false, reason);
}

public class TaskStatusService : ITaskStatusService
{
    private static readonly HashSet<(TaskStatus, TaskStatus)> Allowed = new()
    {
        (TaskStatus.Todo, TaskStatus.InProgress),
        (TaskStatus.InProgress, TaskStatus.Done),
        (TaskStatus.InProgress, TaskStatus.Todo),
        (TaskStatus.Done, TaskStatus.InProgress),
    };

    public TransitionResult TryTransition(TaskStatus current, TaskStatus target)
    {
        if (current == target)
            return TransitionResult.Fail($"Task is already {current}.");
        return Allowed.Contains((current, target))
            ? TransitionResult.Ok()
            : TransitionResult.Fail($"Cannot move a task from {current} to {target}.");
    }
}
```

**Why this design is the lesson:** pure function (no DB, no HTTP) → trivially unit-testable → *that* is why the service exists and why it has an interface. `TransitionResult` instead of exceptions → expected domain failures aren't exceptional (S5 error-taxonomy lesson). The transition table is data → adding a `Cancelled` status is a one-line diff (stretch exercise proves it).

---

## 7. Application Wiring (code-complete skeletons)

### 7.1 Program.cs (final form — S1 starts smaller; comments mark arrival session)

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddProblemDetails();                                   // S5
builder.Services.AddDbContext<AppDbContext>(o =>                        // S3
    o.UseSqlite(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddScoped<ITaskStatusService, TaskStatusService>();    // S5
builder.Services.AddOpenApi();                                          // S8 polish

var app = builder.Build();

app.UseExceptionHandler();                                              // S5
app.MapOpenApi();                                                       // S8
app.MapControllers();

app.Run();

public partial class Program { }   // S6: visible to WebApplicationFactory
```

### 7.2 Representative controller (the pattern all endpoints follow)

```csharp
[ApiController]
[Route("api/projects")]
public class ProjectsController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<PagedResponse<ProjectResponse>>> GetAll(
        [FromQuery] int page = 1, [FromQuery] int pageSize = 10, CancellationToken ct = default)
    {
        if (page < 1 || pageSize is < 1 or > 50)
            return BadRequest(new ValidationProblemDetails
                { Detail = "page must be >= 1 and pageSize between 1 and 50." });

        var query = db.Projects.AsNoTracking().OrderBy(p => p.Id);
        var total = await query.CountAsync(ct);
        var items = await query
            .Skip((page - 1) * pageSize).Take(pageSize)
            .Select(p => new ProjectResponse(p.Id, p.Name, p.Description, p.CreatedAtUtc, p.Tasks.Count))
            .ToListAsync(ct);

        return Ok(new PagedResponse<ProjectResponse>(items, page, pageSize, total));
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
        db.Projects.Add(project);
        await db.SaveChangesAsync(ct);

        var response = new ProjectResponse(project.Id, project.Name, project.Description, project.CreatedAtUtc, 0);
        return CreatedAtAction(nameof(GetById), new { id = project.Id }, response);
    }
    // GetById, Update, Delete follow the same shape — 404 via
    //   return Problem(statusCode: 404, detail: $"Project {id} not found.");
}
```

Every endpoint in the project follows this exact anatomy: validate → query/mutate via `DbContext` (or service when a rule exists) → project to contract → correct status code. No endpoint deviates; predictability is the pedagogy.

### 7.3 Testing architecture

```csharp
// Integration/ApiFactory.cs — SQLite file-per-test-run, real migrations
public class ApiFactory : WebApplicationFactory<Program>
{
    private readonly string _dbPath = Path.Combine(Path.GetTempPath(), $"tt-tests-{Guid.NewGuid():N}.db");

    protected override void ConfigureWebHost(IWebHostBuilder builder) =>
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.AddDbContext<AppDbContext>(o => o.UseSqlite($"Data Source={_dbPath}"));
        });
}
```

| Layer | Proves | Example |
|---|---|---|
| Unit (`TaskStatusServiceTests`) | The rule table, exhaustively — all 4 allowed, all forbidden, no-ops | `[Theory]` + `[InlineData]` over the transition matrix |
| Integration (`ProjectEndpointTests`) | Contract compliance over real HTTP + real SQLite | `POST` invalid name → `400` + `application/problem+json`; `GET` unknown id → `404` |

Real SQLite file (not EF InMemory provider) so tests exercise migrations, constraints, and cascades — the things that actually break. This is also the tests-hit-real-database principle stated honestly at teaching scale.

---

## 8. Engineering Standards (Goal 5 — the senior additions)

Things a 15-year engineer installs on day one because they're nearly free and compound daily:

### 8.1 `.editorconfig` in the repo root
Style stops being a review topic forever. Ship the standard dotnet one; add `csharp_style_var_when_type_is_apparent = true`. One S1 sentence: "the machine enforces style so humans can review *design*."

### 8.2 Commit and PR conventions
- Commits: imperative, story-referenced — `TT-04: return 201 with Location from create project`.
- PR template (in the starter repo): *What / Why / How verified / AI assistance used?*
- PRs small enough to review in 10 minutes; reviewer cites `api-contract.md` or §8.4, not taste.

### 8.3 CI from Session 6 (stretch → default)
One GitHub Actions workflow: `dotnet build --warnaserror` + `dotnet test`. Warnings-as-errors in CI (not locally) — nullability warnings become merge blockers exactly where it's cheap. Watching a red X turn green on their own PR teaches more about professional development than an hour of lecture.

### 8.4 Definition of Done (printed; the PO enforces it)
A story is Done when: behavior matches AC → contract table updated if touched → tests green locally *and* in CI (from S6) → PR reviewed by one person → no compiler warnings → AI assistance recorded if meaningful.

### 8.5 Observability-lite (S5, 15 minutes)
Structured logging with the built-in `ILogger` — one rule: **log events, not prose**: `_logger.LogWarning("Invalid transition {From}->{To} for task {TaskId}", ...)`. Show once how `traceId` in the Problem Details body matches the log line — request-to-log correlation is the single observability habit worth installing this early. OpenTelemetry: named as the industry standard, deferred.

### 8.6 Two rituals that outlast the internship
- **"Read the diff before you push"** — self-review catches 30% of review comments for free.
- **"Reproduce before you fix"** — no bug fix without first writing the failing request/test (S6 seeded-defect exercise institutionalizes this).

### 8.7 What I deliberately did NOT add
Docker, caching, background jobs, API versioning machinery, rate limiting, health-check libraries, Redis. Each is real; none survives the 24-hour budget without evicting something on the graduation floor. All are named in the S8 "what's next" map so trainees know they exist and where they fit.

---

## 9. Seed Data and Fixtures

Provided in the instructor repo (used from S3):

- `seed-dev.sql` / EF seeding: 3 projects, 12 tasks in mixed statuses — small enough to eyeball in every demo.
- `seed-perf.sql`: 100 projects × 500 tasks (50k rows) — exists *only* for the §5.3 index demo; never the default.
- `TaskTracker.Api.http`: every contract request with expected status codes as comments, sectioned per sprint — doubles as manual regression suite and demo script for Session 8.

---

## 10. Release Checklist (Session 8, per repo)

- [ ] `git clone` → README commands → running API in ≤ 5 commands on a machine that isn't yours
- [ ] `dotnet build --warnaserror` clean; `dotnet test` green
- [ ] All §6-contract requests in the `.http` file return the documented codes
- [ ] No secrets in the repo history (connection string is local-file SQLite; config via `appsettings` + user-secrets pattern shown in S7)
- [ ] OpenAPI UI reflects the real contract (spot-check 3 endpoints)
- [ ] Problem Details on every failure path; no stack traces in any response body
- [ ] Migrations apply from zero: delete DB file → `dotnet ef database update` → seed → smoke test
- [ ] Board: all committed stories in Done; anything else explicitly returned to Backlog (honesty over theater)

---

## 11. Goal Traceability

| Instructor goal | Where it lands |
|---|---|
| 1. Backend types incl. serverless | §1 map (S1) + S3/S8 touchpoints — mental model, deliberately not implemented |
| 2. ASP.NET Core Web API mastery | §4, §6, §7 — every required capability exercised in one coherent codebase |
| 3. Real company workflow | §2 — internship *runs as* 4 sprints with stories, board, DoD, PO acceptance; §8.2-8.4 the surrounding discipline |
| 4. DB design → index/query optimization | §5 — schema-by-hand before ORM, reviewed migrations, measured index demo with `EXPLAIN QUERY PLAN`, N+1 counted live; deeper tuning honestly routed to the post-path |
| 5. Senior experience | §8 standards + every "deliberate choice" narration hook; the restraint list in §8.7 is itself the senior lesson |
