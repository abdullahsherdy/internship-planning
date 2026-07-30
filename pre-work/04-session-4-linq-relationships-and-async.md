# Before Session 4: LINQ, Relationships, DTOs, and Async

**Required time:** 45 minutes  
**Submit:** At least 12 hours before Session 4

## Why You Are Studying This

Session 4 queries related data. LINQ syntax is short, but incorrect assumptions about filtering, projection, database execution, or async I/O can produce slow or incorrect APIs.

Session 4 closes Sprint 2 with **TT-07** (create and list tasks inside a project) and **TT-08** (filter tasks by status and page through results). Paged list responses use the contract's fixed envelope — `{ "items": [...], "page": 1, "pageSize": 10, "totalCount": 42 }` with `pageSize` capped at 50 — so every trainee's list endpoint returns the same shape. The session also *measures* two performance ideas live: the N+1 query problem (you will count the queries) and what one index does to a 50,000-row query plan.

## Learning Outcomes

You should be able to:

- Read a LINQ pipeline using `Where`, `OrderBy`, and `Select`.
- Explain the difference between an entity and a response DTO.
- Describe deferred query execution at a basic level.
- Explain why database operations use async APIs and cancellation tokens.

## Part 1: LINQ Study - 15 Minutes

Read:

https://learn.microsoft.com/en-us/dotnet/csharp/linq/

Focus on:

- `Where`
- `Select`
- `OrderBy` / `OrderByDescending`
- `FirstOrDefault`
- `Any`

Given:

```csharp
var result = tasks
    .Where(task => task.Status == "Todo")
    .OrderBy(task => task.DueDate)
    .Select(task => new
    {
        task.Id,
        task.Title,
        task.DueDate
    });
```

Write one sentence describing what each operation does.

## Part 2: Entity Versus DTO - 10 Minutes

Database entity:

```csharp
public sealed class TaskItem
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public Project Project { get; set; } = null!;
}
```

Response DTO:

```csharp
public sealed record TaskResponse(
    int Id,
    string Title,
    string Status,
    string ProjectName);
```

Answer:

1. Why might the API return `TaskResponse` instead of `TaskItem`?
2. Which type is the public contract?
3. What problem could occur if every navigation property is serialized?
4. Why can projection be more efficient than loading full entities?

## Part 3: Async Study - 10 Minutes

Read the introduction and "Don't block, await instead":

https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/

Compare:

```csharp
var tasks = await dbContext.Tasks.ToListAsync(cancellationToken);
```

with:

```csharp
var tasks = dbContext.Tasks.ToListAsync().Result;
```

Explain why the first form is preferred in an ASP.NET Core application.

## Part 4: Query Exercise - 10 Minutes

Write a LINQ query that:

1. Starts with `tasks`.
2. Keeps only tasks for `projectId`.
3. Keeps only tasks whose status equals `requestedStatus`.
4. Orders by due date.
5. Returns only Id, Title, Status, and DueDate.

Pseudocode is acceptable if your C# syntax is incomplete.

## Check Yourself

1. What is the difference between filtering and projection?
2. When does an EF Core query normally execute?
3. Why use `AsNoTracking` for a read-only query?
4. Why should `CancellationToken` be forwarded?
5. Why should an EF entity not automatically become an API contract?
6. Why should `pageSize` have a maximum instead of accepting any number the client sends?

## Submit

- Your explanation of the sample pipeline.
- Four DTO answers.
- Async comparison answer.
- Your query exercise.

## Foundation Support

Practice LINQ against a normal in-memory `List<int>` first:

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
```

Filter even numbers, multiply each by ten, and order descending.

## Stretch

Explain the difference between `IEnumerable<T>` and `IQueryable<T>` in this project. Include one example of accidentally moving work from the database into application memory.

Also preview the Session 4 stretch story **TT-09** (sort tasks by an allow-listed field): why must `?sortBy=` accept only a fixed list of field names instead of any string the client sends?

## Blocked?

Submit the input collection, your attempted query, expected output, and actual output or compiler error.

