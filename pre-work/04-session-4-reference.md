# Session 4 Reference: C#, LINQ, and EF Core Foundations

> **Abdullah Sherdy** — Software Engineer & .NET Backend Instructor\
> [abdullahsherdy.tech](https://abdullahsherdy.tech) · [YouTube](https://youtube.com/@abdullah.sherdy) · [LinkedIn](https://linkedin.com/in/abdullah-sherdy)

This is the **complete study reference** that goes with the Session 4 pre-work pack. The pack itself stays at 45 minutes; 
this document is for reading before Session 4 and keeping open during the project work that follows.
Everything here uses the Task Tracker entities (`Project`, `TaskItem`) so examples match the code you already have.

**Read it top to bottom once, then use it as a lookup while coding.**

**How the parts connect:** delegates make lambdas possible → lambdas make LINQ possible → LINQ + expression trees make EF Core queries possible → loading strategies decide how many SQL queries EF Core actually runs. That is the order below.

---

## Part A — C# Foundations

### A1. Value Types vs Reference Types

**Definition:** A value type (`int`, `bool`, `DateTime`, `struct`, `enum`) stores its data directly; copying it copies the data. A reference type (`class`, `string`, arrays, `record class`) stores a reference; copying it copies the reference, so two variables can point at the same object.

```csharp
int a = 5;
int b = a;      // b is a copy; changing b never changes a

var p1 = new Project { Name = "API" };
var p2 = p1;    // same object
p2.Name = "Changed";
Console.WriteLine(p1.Name); // "Changed" — p1 and p2 are the same Project
```

**Use case in our project:** entities are classes (reference types) on purpose — EF Core's change tracker holds a reference to the same object you edit, which is how `SaveChangesAsync` knows what changed.

**Pitfall:** passing an entity around and mutating it in two places mutates the *same* object. If you want an independent copy, you must create one.

### A2. Nullable Reference Types (`?`, `= null!`, `string.Empty`)

**Definition:** With `<Nullable>enable</Nullable>` (on in our project), the compiler tracks whether a reference can be `null`. `string` means "never null"; `string?` means "may be null".

```csharp
public sealed class TaskItem
{
    public string Title { get; set; } = string.Empty; // never null — initialized
    public string? Description { get; set; }          // null is a valid value
    public Project Project { get; set; } = null!;     // navigation: EF fills this in later
}
```

**Why `= null!` on navigations:** the compiler cannot know EF Core will populate `Project` when you `Include` it. `null!` says "I promise this will be set before use." It is a promise, not a guarantee — if you forget to `Include`, it *is* null at runtime.

**Use case:** DTO validation. `string?` on an optional field documents the contract; the compiler then forces you to handle the null path.

### A3. Records vs Classes

**Definition:** a `record` is a reference type with value-based equality, built-in `ToString`, and concise "positional" syntax. Records are ideal for **immutable data carriers**; classes are ideal for objects with identity and mutable state.

```csharp
// DTO: a record — just data, compared by content
public sealed record TaskResponse(int Id, string Title, string Status, string ProjectName);

// Entity: a class — has identity (the Id), mutated by the change tracker
public sealed class TaskItem { /* ... */ }
```

```csharp
var r1 = new TaskResponse(1, "Fix bug", "Todo", "API");
var r2 = new TaskResponse(1, "Fix bug", "Todo", "API");
Console.WriteLine(r1 == r2); // True — records compare by content
```

**Rule in our project:** DTOs (`Contracts/`) are records; entities (`Domain/`) are classes. Never the other way round.

**`with` expressions:** copy a record changing one property — `var renamed = r1 with { Title = "New" };`

### A4. Delegates

**Definition:** a delegate is a **type that holds a reference to a method**. It lets you pass behavior as data — the foundation of everything LINQ does.

```csharp
// Declaring your own delegate type (rare in modern code, but this is what's underneath)
public delegate bool TaskFilter(TaskItem task);

TaskFilter isTodo = task => task.Status == "Todo";
bool result = isTodo(someTask); // invoke like a method
```

**The three built-in generic delegates** — you will almost never declare your own; use these:

| Delegate | Shape | Meaning | Example |
|---|---|---|---|
| `Func<T, TResult>` | takes `T`, returns `TResult` | "transform / compute" | `Func<TaskItem, string> getTitle = t => t.Title;` |
| `Action<T>` | takes `T`, returns nothing | "do something" | `Action<string> log = msg => Console.WriteLine(msg);` |
| `Predicate<T>` | takes `T`, returns `bool` | "test" (older APIs; `Func<T,bool>` preferred) | `Predicate<TaskItem> p = t => t.Id > 0;` |

**Use case:** `Where` is literally declared as `Where(Func<TaskItem, bool> predicate)`. When you write `.Where(t => t.Status == "Todo")`, you are creating a `Func<TaskItem, bool>` and handing it to `Where`. Delegates are why LINQ can exist.

**Multicast:** a delegate can hold several methods (`log += OtherLogger;`) — this is how C# events work. You will not need multicast in the Task Tracker; know the term exists.

### A5. Lambda Expressions

**Definition:** a lambda is inline, anonymous method syntax that produces a delegate (or an expression tree — see A6).

```csharp
t => t.Status == "Todo"                 // one parameter, expression body
(t, index) => $"{index}: {t.Title}"     // two parameters
t => { var s = t.Status; return s == "Done"; } // statement body (braces + return)
() => DateTime.UtcNow                   // no parameters
```

**Closures:** a lambda can capture variables from the surrounding method:

```csharp
string requestedStatus = "Todo";                       // local variable
var filtered = tasks.Where(t => t.Status == requestedStatus); // captured inside the lambda
```

**Pitfall:** the lambda captures the *variable*, not its value at creation time. If `requestedStatus` changes before the query runs (deferred execution — Part B), the query uses the new value.

### A6. Expression Trees (why EF Core can translate your lambda to SQL)

**Definition:** `Expression<Func<T, bool>>` is not a compiled method — it is a **data structure describing the code** ("property Status, equals, constant 'Todo'"). EF Core walks that structure and writes SQL from it.

```csharp
Func<TaskItem, bool> compiled = t => t.Status == "Todo";       // runnable code
Expression<Func<TaskItem, bool>> tree = t => t.Status == "Todo"; // description of code
```

Same lambda text, completely different thing. `IEnumerable<T>.Where` takes the first (runs in memory); `IQueryable<T>.Where` takes the second (translates to SQL). You never build expression trees by hand in this project — but this is the answer to "how does my C# become SQL?"

**Pitfall:** anything EF Core cannot translate (calling your own helper method inside a `Where`, for example) throws at runtime: *"could not be translated."* Fix: move that logic before/after the query, or express it in translatable operators.

### A7. Extension Methods

**Definition:** a static method that *appears* to be an instance method on another type, declared with `this` on the first parameter. All LINQ operators are extension methods on `IEnumerable<T>` / `IQueryable<T>`.

```csharp
public static class TaskItemExtensions
{
    public static bool IsOverdue(this TaskItem task, DateTime now)
        => task.DueDate is not null && task.DueDate < now && task.Status != "Done";
}

// usage — reads like a built-in member:
if (task.IsOverdue(DateTime.UtcNow)) { /* ... */ }
```

**Use case:** `Where`, `Select`, `OrderBy`, `ToListAsync` — none of them are defined *on* your collection type. They are extensions brought in by `using System.Linq;` and `using Microsoft.EntityFrameworkCore;`. This is why a missing `using` makes `ToListAsync` "not exist."

### A8. Generics

**Definition:** generics let one type or method work for many element types with full type safety — `List<T>`, `Task<T>`, `IEnumerable<T>`, `PagedResponse<T>`.

```csharp
public sealed record PagedResponse<T>(
    IReadOnlyList<T> Items, int Page, int PageSize, int TotalCount);

// One definition, reused for every list endpoint:
PagedResponse<TaskResponse> tasksPage = ...;
PagedResponse<ProjectResponse> projectsPage = ...;
```

**Generic methods** infer `T` from usage: `tasks.Select(t => t.Title)` infers `Select<TaskItem, string>`.

**Constraints** (recognize, don't memorize): `where T : class`, `where T : new()` restrict what `T` can be. You will see them in library signatures.

**Reminder from our decisions:** generics are fine for *data shapes* like `PagedResponse<T>`. We deliberately do **not** build a generic `Repository<T>` — one interface + one class per aggregate (ADR-004 as amended).

### A9. Interfaces

**Definition:** an interface declares capability without implementation. A class that implements it can be swapped for any other implementation.

```csharp
public interface ITaskRepository
{
    Task<TaskItem?> GetByIdAsync(int id, CancellationToken ct);
    Task AddAsync(TaskItem task, CancellationToken ct);
}
```

**Use case:** controllers depend on `ITaskRepository`, not the concrete class. In Session 6 tests will substitute a test implementation — that swap is only possible because the dependency is an interface registered in DI (`builder.Services.AddScoped<ITaskRepository, TaskRepository>();`).

### A10. `IEnumerable<T>`, iterators, and `yield return`

**Definition:** `IEnumerable<T>` is "a sequence you can loop over." `foreach` works on anything implementing it. `yield return` builds one lazily:

```csharp
static IEnumerable<int> Numbers()
{
    Console.WriteLine("first");
    yield return 1;
    Console.WriteLine("second");
    yield return 2;
}

var seq = Numbers();      // NOTHING printed yet
foreach (var n in seq) {} // now "first", "second" print — code runs as you iterate
```

**Why this matters:** this laziness is the same *deferred execution* behavior LINQ has (Part B). Understanding `yield` explains why a LINQ query is a *description*, not a *result*.

### A11. `async` / `await`, `Task<T>`, and cancellation

**Definition:** `async`/`await` lets a method pause at an I/O operation (database call, HTTP call) **without blocking the thread**. `Task<T>` is "a `T` that will exist later."

```csharp
public async Task<TaskItem?> GetByIdAsync(int id, CancellationToken ct)
{
    return await _dbContext.Tasks
        .FirstOrDefaultAsync(t => t.Id == id, ct);
}
```

What actually happens: the thread that started the request is **released** while SQLite works; when the result arrives, execution resumes. Under load, that freed thread serves other requests — this is why every EF Core call in our API is async.

**The rules that matter:**

1. **Async all the way up.** If a method awaits, its caller should await it too, up to the controller action (`public async Task<IActionResult> ...`).
2. **Never `.Result` or `.Wait()`** on a Task in ASP.NET Core — you block a thread at best and deadlock at worst. If you feel the need, the method signature above you should become async instead.
3. **`async` without `await` is a warning, not a feature.** If nothing is awaited, remove `async` and return the Task directly.
4. **Forward the `CancellationToken`.** ASP.NET Core hands your action a token that fires when the client disconnects. Passing it to `ToListAsync(ct)` lets the database stop work nobody will read.

```csharp
[HttpGet]
public async Task<IActionResult> GetTasks(int projectId, CancellationToken ct)
{
    var items = await _repository.GetForProjectAsync(projectId, ct);
    return Ok(items);
}
```

**`Task` vs `Task<T>`:** `Task` = "finishes later, returns nothing" (like async `void`… but never use `async void` outside event handlers). `Task<T>` = "finishes later with a `T`."

### A12. Pattern matching and null-handling operators (quick reference)

You will see these constantly in modern C#:

```csharp
if (task.DueDate is null) { }            // null check (preferred over == null)
if (task.DueDate is not null) { }
var name = project?.Name;                 // null-conditional: null if project is null
var title = input ?? "Untitled";          // null-coalescing: fallback value
existing.Title = dto.Title ?? existing.Title; // "update only if provided"
if (result is TaskItem t) { UseIt(t); }   // type pattern with capture
var label = task.Status switch            // switch expression
{
    "Todo" => "Not started",
    "InProgress" => "Working",
    "Done" => "Finished",
    _ => "Unknown"
};
```

---

## Part B — LINQ In Depth

### B1. What LINQ is

**Definition:** Language Integrated Query — a set of extension methods (`Where`, `Select`, …) that work on any `IEnumerable<T>` (in-memory) or `IQueryable<T>` (translatable to SQL). Two syntaxes exist; we use **method syntax** everywhere:

```csharp
// method syntax (use this)
var titles = tasks.Where(t => t.Status == "Todo").Select(t => t.Title);

// query syntax (recognize it; don't write it in this project)
var titles2 = from t in tasks where t.Status == "Todo" select t.Title;
```

### B2. The core operators

| Operator | Does | Returns |
|---|---|---|
| `Where(t => ...)` | filter — keep matching elements | sequence |
| `Select(t => ...)` | projection — transform each element | sequence |
| `OrderBy` / `OrderByDescending` / `ThenBy` | sort | sequence |
| `Skip(n)` / `Take(n)` | pagination window | sequence |
| `FirstOrDefault(t => ...)` | first match or `null`/default | single element |
| `SingleOrDefault(t => ...)` | the *only* match (throws if more than one) | single element |
| `Any(t => ...)` | "does at least one match?" | `bool` |
| `Count(t => ...)` | how many match | `int` |
| `All(t => ...)` | "do all match?" | `bool` |
| `ToList()` / `ToListAsync(ct)` | **execute now**, materialize results | `List<T>` |
| `GroupBy(t => ...)` | group by a key | groups |
| `Distinct()` | remove duplicates | sequence |
| `Sum` / `Min` / `Max` / `Average` | aggregate | number |

**Filtering vs projection** (a Check Yourself question): `Where` decides **which rows**; `Select` decides **which columns / what shape**. The contract's paged task list uses both plus `Skip`/`Take`:

```csharp
var query = db.Tasks.Where(t => t.ProjectId == projectId);
if (status is not null) query = query.Where(t => t.Status == status);

var totalCount = await query.CountAsync(ct);
var items = await query
    .OrderBy(t => t.Id)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(t => new TaskResponse(t.Id, t.Title, t.Status, t.Project.Name))
    .ToListAsync(ct);

return new PagedResponse<TaskResponse>(items, page, pageSize, totalCount);
```

Note the pattern: **build the query conditionally, count it, then page it.** One query object, two executions (COUNT + page SELECT).

### B3. Deferred execution

**Definition:** most LINQ operators do **not run** when written — they build a description. Execution happens when you iterate (`foreach`), materialize (`ToList`, `ToListAsync`), or reduce to a single value (`Count`, `First`, `Any`).

```csharp
var query = tasks.Where(t => t.Status == "Todo"); // nothing has run
tasks.Add(newTodoTask);
var list = query.ToList(); // runs NOW — includes newTodoTask
```

**Deferred:** `Where`, `Select`, `OrderBy`, `Skip`, `Take`, `GroupBy`.
**Immediate:** `ToList()`, `ToArray()`, `Count()`, `First…`, `Single…`, `Any()`, `Sum()`.

**Pitfall — multiple enumeration:** every enumeration re-runs the query. On `IQueryable` that means **another database round trip**:

```csharp
var query = db.Tasks.Where(t => t.ProjectId == id); // not executed
if (query.Any())              // query 1 to the database
{
    var list = query.ToList(); // query 2 to the database
}
// better: materialize once, then check list.Count
```

### B4. `IEnumerable<T>` vs `IQueryable<T>` — where the work happens

**Definition:** both look identical to call, but:

- `IQueryable<T>` — operators take **expression trees**; the provider (EF Core) translates the whole chain to **SQL**. Filtering happens **in the database**.
- `IEnumerable<T>` — operators take **compiled delegates**; everything runs **in application memory**.

The moment you cross from `IQueryable` to `IEnumerable`, everything after runs in memory:

```csharp
// GOOD — filter and page translated to SQL; database returns 10 rows
var page = await db.Tasks
    .Where(t => t.ProjectId == projectId)
    .Skip(0).Take(10)
    .ToListAsync(ct);

// BAD — ToList() executes "SELECT all tasks"; Where/Take then run in memory
var page2 = db.Tasks
    .ToList()                              // pulls the ENTIRE table
    .Where(t => t.ProjectId == projectId)  // now just LINQ-to-Objects
    .Take(10)
    .ToList();
```

With 50,000 rows, version 2 transfers 50,000 rows to filter down to 10. This is the single most common performance bug in EF Core code, and Session 4 measures it live.

**Rule:** keep the query `IQueryable` until the final `ToListAsync` / `CountAsync` / `FirstOrDefaultAsync`. Repository methods should return materialized results (`List<T>`), never leak `IQueryable` (ADR-004 amendment).

### B5. Projection with `Select` — the preferred loading strategy

Projection creates exactly the shape you need, in SQL:

```csharp
var items = await db.Tasks
    .Where(t => t.ProjectId == projectId)
    .Select(t => new TaskResponse(t.Id, t.Title, t.Status, t.Project.Name))
    .ToListAsync(ct);
```

Generated SQL selects only 4 columns and **joins Projects automatically** because the projection touched `t.Project.Name` — no `Include` needed, no full entities loaded, no change tracking. For read endpoints, projection beats every loading strategy in Part C. Learn Part C anyway: you must know what the alternatives do to recognize their cost.

---

## Part C — EF Core In Depth

### C1. DbContext: what it actually is

**Definition:** `DbContext` is a **unit-of-work session** with the database: it opens connections, translates LINQ to SQL, **tracks changes** to loaded entities, and writes them back on `SaveChangesAsync`.

- **Lifetime:** one per HTTP request (`AddDbContext` registers it *scoped*). Never share one across requests; never make it a singleton.
- `DbSet<TaskItem> Tasks` is the queryable entry point per entity — "the table, as C# objects."

### C2. Change tracking and entity states

Every entity a query returns (without `AsNoTracking`) is registered in the change tracker with a state:

| State | Meaning | How it got there | On `SaveChangesAsync` |
|---|---|---|---|
| `Unchanged` | matches database | loaded by a query | nothing |
| `Added` | new | `db.Tasks.Add(entity)` | `INSERT` |
| `Modified` | property changed | you set a property on a tracked entity | `UPDATE` (changed columns only) |
| `Deleted` | to be removed | `db.Tasks.Remove(entity)` | `DELETE` |
| `Detached` | not tracked | `AsNoTracking`, or a `new` entity not yet added | nothing |

This is why an update in EF Core has no "Update" call in the obvious sense:

```csharp
var task = await db.Tasks.FirstOrDefaultAsync(t => t.Id == id, ct); // tracked
if (task is null) return NotFound();
task.Status = "Done";              // tracker notices the change
await db.SaveChangesAsync(ct);     // UPDATE Tasks SET Status = 'Done' WHERE Id = @id
```

**`AsNoTracking()`:** for read-only queries, skip tracker registration — less memory, faster, and it signals intent:

```csharp
var items = await db.Tasks.AsNoTracking()
    .Where(t => t.ProjectId == projectId)
    .ToListAsync(ct);
```

**Rule:** reads that will never be saved → `AsNoTracking()` (or projection with `Select`, which never tracks anyway). Load-then-modify flows → tracked (default).

### C3. Relationships and navigation properties

Our model has one relationship: **Project 1 → many TaskItems.**

```csharp
public sealed class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<TaskItem> Tasks { get; set; } = [];   // collection navigation
}

public sealed class TaskItem
{
    public int Id { get; set; }
    public int ProjectId { get; set; }                 // foreign key
    public Project Project { get; set; } = null!;      // reference navigation
    // ...
}
```

- **Foreign key** (`ProjectId`) — the actual column in the database.
- **Navigation property** (`Project`, `Tasks`) — the C# convenience for walking the relationship. It is only populated if you ask EF Core to load it (Part C4) — otherwise it is `null` / empty. **A null navigation does not mean "no related data exists"; it means "not loaded."**

EF Core infers this relationship by convention (`ProjectId` matches `Project.Id`). Explicit configuration when needed lives in `OnModelCreating`:

```csharp
modelBuilder.Entity<TaskItem>()
    .HasOne(t => t.Project)
    .WithMany(p => p.Tasks)
    .HasForeignKey(t => t.ProjectId)
    .OnDelete(DeleteBehavior.Cascade); // deleting a Project deletes its tasks
```

### C4. Loading related data: eager, lazy, explicit — and projection

The central question: *when you load a `TaskItem`, how does its `Project` get loaded?* Four answers.

#### 1. Eager loading — `Include` / `ThenInclude`

**Definition:** load related data **in the same query**, up front, by telling EF Core exactly which navigations you need.

```csharp
var tasks = await db.Tasks
    .Include(t => t.Project)              // JOIN Projects in the same SQL
    .Where(t => t.Status == "Todo")
    .ToListAsync(ct);

Console.WriteLine(tasks[0].Project.Name); // populated — safe
```

`ThenInclude` goes one level deeper (`.Include(p => p.Tasks).ThenInclude(t => t.Something)` — we have no third level, but recognize the syntax).

**Use cases:**
- You need the **full related entities** (not just a column or two) — e.g., a load-then-modify flow that touches both sides.
- Predictable: one query (or a known number with `AsSplitQuery`), decided at compile time.

**Costs / pitfalls:**
- Includes **every column** of the related entity even if you need one.
- Wide `Include` chains produce large JOINs with duplicated parent data ("cartesian explosion" with multiple collection includes — mitigated by `.AsSplitQuery()`, which runs one query per include instead of one giant join).
- Forgetting `Include` and touching the navigation → `NullReferenceException` (with lazy loading off, which is our setup).

#### 2. Lazy loading — load on first touch

**Definition:** related data is loaded **automatically, on demand**, the first time code reads a navigation property. Each first touch fires a **separate SQL query**, invisibly.

EF Core does **not** do this by default. Enabling it requires the `Microsoft.EntityFrameworkCore.Proxies` package, `.UseLazyLoadingProxies()`, and making every navigation `virtual` (so EF can subclass your entity and intercept property access):

```csharp
// setup (NOT in our project — for understanding only)
options.UseSqlite(cs).UseLazyLoadingProxies();
public virtual Project Project { get; set; } = null!;

// then this "just works" — but hides a query:
var tasks = await db.Tasks.ToListAsync(ct);   // query 1: tasks
foreach (var t in tasks)
    Console.WriteLine(t.Project.Name);        // one MORE query PER task
```

**That loop is the N+1 problem:** 1 query for the list + N queries for N navigations = 101 queries for 100 tasks. The code looks innocent; the database melts. Session 4 counts these queries live.

**Legitimate use cases (why the feature exists):**
- Long-lived desktop apps where you genuinely can't predict which navigations a user will open.
- Rapid prototyping where correctness matters and performance doesn't yet.

**Why we do not use it:**
- It hides database access inside property getters — you can't see the cost in the code.
- N+1 by default in any loop.
- Queries fire outside async (`t.Project` is a property — it blocks synchronously).
- **Decision for this project: lazy loading stays off.** If a navigation is null, the fix is `Include` or projection — never proxies.

#### 3. Explicit loading — `Entry(...).Load()`

**Definition:** related data is loaded on demand, but **you write the load call yourself** — visible and deliberate, unlike lazy loading.

```csharp
var project = await db.Projects.FirstAsync(p => p.Id == id, ct); // tasks NOT loaded

await db.Entry(project)
    .Collection(p => p.Tasks)      // for a collection navigation
    .LoadAsync(ct);                // second query, but explicit and awaited

await db.Entry(task)
    .Reference(t => t.Project)     // for a reference navigation
    .LoadAsync(ct);
```

You can even filter the load: `db.Entry(project).Collection(p => p.Tasks).Query().Where(t => t.Status == "Todo").ToListAsync(ct)`.

**Use cases:**
- You *conditionally* need related data ("only load tasks if the report flag is set") and don't want to pay the JOIN when the condition is false.
- Rare in web APIs — in practice a second targeted query or projection is usually cleaner.

**vs lazy loading:** same "load later" idea, but explicit loading is *visible, async, and intentional* — nothing fires behind your back.

#### 4. Projection (`Select`) — usually the real answer

Already covered in B5, listed here because it belongs in the comparison: for **read endpoints**, project into a DTO and let EF Core generate the exact JOIN and column list. No entities, no tracking, no over-fetching, no N+1.

#### Decision table

| You need… | Use |
|---|---|
| A response DTO (any read endpoint) | **Projection** (`Select`) |
| Full related entities to modify | **Eager** (`Include`) on a tracked query |
| Related data only in a rare branch | **Explicit** (`Entry(...).LoadAsync`) |
| Automatic loading on property touch | **Lazy** — not in this project; know why not |

**Quick self-test:** "list tasks with their project name" → projection. "Change a task's status" → tracked load, no related data needed at all. "Delete a project and show which tasks died" → eager `Include(p => p.Tasks)`.

### C5. The N+1 problem, precisely

**Definition:** executing 1 query for a parent list, then N additional queries (one per row) for related data — usually caused by lazy loading or by querying inside a loop.

```csharp
// N+1 WITHOUT lazy loading — the loop version:
var projects = await db.Projects.ToListAsync(ct);          // 1 query
foreach (var p in projects)
{
    var count = await db.Tasks.CountAsync(t => t.ProjectId == p.Id, ct); // N queries
}

// Fixed with one grouped query:
var counts = await db.Tasks
    .GroupBy(t => t.ProjectId)
    .Select(g => new { ProjectId = g.Key, Count = g.Count() })
    .ToListAsync(ct);                                        // 1 query
```

**How to detect it:** EF Core logs every SQL command. In development, watch the console while hitting an endpoint — if one request prints a wall of near-identical `SELECT`s, you have N+1. Session 4 does exactly this measurement.

**Rules of thumb:** never `await` a query inside a `foreach` over query results; never touch navigations in a loop without having `Include`d or projected them.

### C6. Migrations (recap from Session 3, one level deeper)

- `dotnet ef migrations add <Name>` — compares your model to the last **model snapshot** and generates `Up()`/`Down()` code for the difference.
- `dotnet ef database update` — applies pending migrations; EF records them in the `__EFMigrationsHistory` table so each runs once.
- **Read the generated migration before applying it.** It is code-reviewable C# — a wrong model change shows up here first (e.g., a column drop you didn't intend).
- Never edit an applied migration; add a new one.
- `dotnet ef migrations remove` safely deletes the **last unapplied** migration.

### C7. Indexes (for the Session 4 live measurement)

**Definition:** an index is a sorted lookup structure on one or more columns, letting the database find matching rows without scanning the whole table.

```csharp
modelBuilder.Entity<TaskItem>()
    .HasIndex(t => new { t.ProjectId, t.Status }); // composite index matching our filter
```

- Foreign key columns get indexes by convention in EF Core.
- Our hot query filters by `ProjectId` + `Status` — a composite index on both serves it directly.
- Cost: indexes speed up reads but slow down writes slightly (each `INSERT`/`UPDATE` maintains them) and take space. Index the columns you filter/sort by; don't index everything.
- Session 4 compares the 50,000-row query plan with and without the index — expect a table scan to become an index seek.

### C8. `SaveChangesAsync`, transactions, and concurrency (awareness level)

- `SaveChangesAsync` wraps **all** pending changes in a single transaction: all succeed or all roll back. For our CRUD, this is all the transaction handling you need.
- One `SaveChangesAsync` per logical operation, at the end — not after every `Add`.
- Concurrency conflicts (two users editing the same row) are handled with concurrency tokens (`[Timestamp]` / `IsRowVersion`). **Out of scope** for the Task Tracker — recognize the term.

### C9. Common EF Core exceptions and what they mean

| Exception / symptom | Usual cause | Fix |
|---|---|---|
| `NullReferenceException` on a navigation | forgot `Include` / projection (lazy loading off) | `Include` it or project the needed columns |
| `InvalidOperationException: ...could not be translated` | untranslatable C# inside a `Where`/`Select` on `IQueryable` | move logic out of the query or use translatable operators |
| `DbUpdateException` (FK constraint) | inserting a `TaskItem` with a `ProjectId` that doesn't exist | validate the project exists first → return 404 per contract |
| Second operation started on this context | sharing one `DbContext` across parallel operations / requests | one scoped context per request; don't run parallel queries on one context |
| Migration fails: "pending model changes" | model edited without adding a migration | `dotnet ef migrations add <Name>` |

---

## Part D — Tie It Together: One Annotated Endpoint

Everything above, in ~20 lines (TT-08 shape):

```csharp
[HttpGet("/api/projects/{projectId}/tasks")]
public async Task<IActionResult> GetTasks(          // A11: async all the way up
    int projectId,
    [FromQuery] string? status,                     // A2: nullable = optional filter
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    CancellationToken ct = default)                 // A11: forwarded below
{
    pageSize = Math.Clamp(pageSize, 1, 50);         // contract: pageSize capped at 50

    if (!await _db.Projects.AnyAsync(p => p.Id == projectId, ct)) // C9: FK guard → 404
        return NotFound();

    var query = _db.Tasks.Where(t => t.ProjectId == projectId);  // B3: deferred, still SQL
    if (status is not null)
        query = query.Where(t => t.Status == status);            // A5: lambda → B4: IQueryable

    var totalCount = await query.CountAsync(ct);                 // execution 1
    var items = await query
        .OrderBy(t => t.Id)
        .Skip((page - 1) * pageSize).Take(pageSize)              // B2: pagination window
        .Select(t => new TaskResponse(                           // B5/C4: projection —
            t.Id, t.Title, t.Status, t.Project.Name))            //   no Include, no N+1
        .ToListAsync(ct);                                        // execution 2

    return Ok(new PagedResponse<TaskResponse>(items, page, pageSize, totalCount)); // A8: generics
}
```

---

## Self-Check (answer without looking)

1. What is a delegate, and which built-in delegate type does `Where` accept?
2. What does a lambda *capture* from its surrounding method?
3. `Func<T,bool>` vs `Expression<Func<T,bool>>` — which one can EF Core turn into SQL, and why?
4. Name the deferred/immediate split: which of `Where`, `ToList`, `OrderBy`, `Count`, `Select` execute the query?
5. What happens to everything written *after* `.ToList()` in a query chain?
6. Define eager, lazy, and explicit loading in one sentence each.
7. Why is lazy loading off in this project? What is the N+1 problem?
8. When is `Include` the right choice over projection?
9. What does `AsNoTracking` do and when should you use it?
10. Why must `CancellationToken` be forwarded to `ToListAsync`?
11. A navigation property is `null`. Does that mean no related data exists?
12. Why does the paged endpoint run exactly two SQL queries?

If any answer is shaky, re-read that section — every one of these appears in Session 4 or in the project build after it.

---

*Prepared by* **Abdullah Sherdy** *— Software Engineer & .NET Backend Instructor*

Found this useful? I publish more .NET and backend engineering content:

- **Website:** [abdullahsherdy.tech](https://abdullahsherdy.tech) — articles, projects, contact, and Private Courses Registeration.
- **YouTube:** [@abdullah.sherdy](https://youtube.com/@abdullah.sherdy) — video walkthroughs and tutorials
- **LinkedIn:** [abdullah-sherdy](https://linkedin.com/in/abdullah-sherdy) — connect and follow my work

*Questions about this material? Reach out on any channel above.*
