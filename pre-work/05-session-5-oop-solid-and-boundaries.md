# Before Session 5: OOP, SOLID, and Service Boundaries

**Required time:** 45 minutes  
**Submit:** At least 12 hours before Session 5

## Why You Are Studying This

Architecture is not the number of folders in a solution. It is the placement of responsibilities and dependencies. Session 5 introduces a service only because the Task Tracker now has a business rule that deserves a clear home.

That rule is Sprint 3's story **TT-10** — the task status workflow. Statuses are `Todo`, `InProgress`, and `Done`; some moves are allowed (`Todo→InProgress`, `InProgress→Done`, `InProgress→Todo`, `Done→InProgress`) and some are forbidden (`Todo→Done` — work cannot be finished before it starts). Session 5 also delivers **TT-11**: every failure returns a standard Problem Details body — no naked `500`s anywhere in the API from this session on.

## Learning Outcomes

You should be able to:

- Explain encapsulation, abstraction, interfaces, and composition.
- Identify mixed responsibilities in a controller.
- Apply SOLID as design questions rather than memorized definitions.
- Explain when an additional service or interface adds value.

## Part 1: OOP Study - 15 Minutes

Read:

https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/oop

Focus on:

- Objects combine state and behavior.
- Encapsulation protects valid state.
- Interfaces define capabilities or contracts.
- Composition lets one object use another object.
- Inheritance is not the default solution for code reuse.

## Part 2: Read the Scenario - 10 Minutes

Suppose a controller action:

1. Reads the task from EF Core.
2. Checks whether the requested status transition is allowed.
3. Changes the task.
4. Saves it.
5. Sends an email.
6. Builds the HTTP response.

Answer:

- Which work belongs to the HTTP boundary?
- Which work is a business rule?
- Which work is persistence?
- Which work is an external side effect?
- Which part should be easiest to unit test?

## Part 3: SOLID as Review Questions - 10 Minutes

Use these questions:

- **SRP:** Does this class have more than one reason to change?
- **OCP:** Can expected variation be added without repeatedly editing a large conditional?
- **LSP:** Can an implementation replace its abstraction without surprising the caller?
- **ISP:** Is a consumer forced to depend on methods it does not need?
- **DIP:** Does policy depend on a replaceable capability instead of a concrete external detail?

For each statement, write `Agree`, `Disagree`, or `It depends`, then explain:

1. Every class should have an interface.
2. Every controller must use a repository.
3. Smaller classes are always better.
4. Business rules should be testable without starting the web server.
5. SOLID means using five design patterns.

## Part 4: Boundary Exercise - 10 Minutes

Design a method for changing task status.

Write:

- Method name.
- Inputs.
- Possible success result.
- Expected failures.
- Which dependency it needs.
- Whether it needs an interface now, and why.

Example shape:

```csharp
Task<ChangeTaskStatusResult> ChangeStatusAsync(
    int taskId,
    TaskStatus newStatus,
    CancellationToken cancellationToken);
```

Do not implement it yet.

## Check Yourself

1. What is an invariant?
2. Why should a controller remain focused on HTTP concerns?
3. When does an interface add useful separation?
4. Why can a generic repository be unnecessary over EF Core?
5. Is duplication always worse than an incorrect abstraction?

## Submit

- Your scenario responsibility analysis.
- Five SOLID statement answers.
- Your proposed method contract.
- One design decision you are uncertain about.

## Foundation Support

Use this responsibility table:

| Concern | Typical owner |
|---|---|
| HTTP request/response | Controller |
| Use-case coordination | Application service |
| Data query/save | DbContext/data access |
| Entity state rule | Entity or domain/application policy |
| Email/file/external API | Dedicated external service |

The table is guidance, not a law. Explain exceptions.

## Stretch

Compare these designs:

1. Controller directly uses `DbContext`.
2. Controller uses a focused application service.
3. Controller uses a service, generic repository, and Unit of Work wrapper.

State what each additional layer buys and costs in this small project.

## Blocked?

Submit the responsibility you cannot place and the alternatives you considered. Design questions can have more than one defensible answer.

