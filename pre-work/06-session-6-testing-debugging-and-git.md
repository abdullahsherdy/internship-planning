# Before Session 6: Testing, Debugging, and Git Discipline

**Required time:** 45 minutes  
**Submit:** At least 12 hours before Session 6

## Why You Are Studying This

A backend feature is not complete because it worked once in Swagger. Tests provide repeatable evidence, while debugging is the process of gathering evidence when actual behavior differs from expected behavior.

Session 6 closes Sprint 3 with **TT-12**: the status-transition rule is proven by unit tests, and the API contract is proven by integration tests over real HTTP and a real SQLite database. From this session, the team's Definition of Done includes green tests — and a story is not Done without them.

## Learning Outcomes

You should be able to:

- Distinguish unit and integration tests.
- Write an Arrange, Act, Assert test description.
- Identify happy, boundary, and negative cases.
- Describe a useful bug report and a focused Git commit.

## Part 1: Testing Study - 15 Minutes

Read:

1. Unit testing C# with `dotnet test` and xUnit:
   https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-xunit
2. ASP.NET Core integration tests:
   https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-10.0

Focus on:

- A unit test checks a small piece of logic in isolation.
- An integration test checks that multiple real parts work together.
- `WebApplicationFactory` starts the API for test requests.
- A test should be deterministic and independent.

Do not try to read every configuration option.

## Part 2: Arrange, Act, Assert - 10 Minutes

Rule:

> A task can move from `Todo` to `InProgress`, then to `Done`. A task cannot move directly from `Todo` to `Done`.

Write three test cases:

1. One allowed transition.
2. One rejected transition.
3. One boundary or unusual input.

For each case write:

- **Arrange:** starting state and inputs.
- **Act:** operation.
- **Assert:** observable result.

## Part 3: Integration Cases - 10 Minutes

Write expected method, request, status, and important response data for:

1. Getting an existing project.
2. Getting a missing project.
3. Creating a valid project.
4. Creating a project with an empty name.

Then answer:

- Which of these should use a real HTTP request in a test?
- Why must test data be isolated between tests?

## Part 4: Debugging and Git - 10 Minutes

A useful bug report includes:

- Expected behavior.
- Actual behavior.
- Reproduction steps.
- Request/input.
- Status/error/stack trace.
- Environment and relevant version.

A useful commit:

- Has one coherent purpose.
- Builds and passes relevant tests.
- Uses an imperative message explaining the behavior change, prefixed with the user story it serves — for example `TT-04: return 201 with Location from create project`.
- Does not include secrets, generated noise, or unrelated edits.

Rewrite these commit messages (assume each relates to creating a project, story TT-04):

- `fix`
- `changes`
- `final final`

## Check Yourself

1. What can a unit test prove that an API integration test does not isolate?
2. What can an integration test catch that a unit test may miss?
3. Why should tests not depend on execution order?
4. Why is reproducing a bug more valuable than guessing?
5. What makes a commit easy to review?

## Submit

- Three unit-test descriptions.
- Four endpoint test cases.
- Answers about HTTP testing and data isolation.
- Three improved commit messages.

## Foundation Support

Use this test naming shape:

```text
MethodName_StateUnderTest_ExpectedBehavior
```

Example:

```text
ChangeStatus_TaskIsDone_ReturnsInvalidTransition
```

Names should describe behavior, not implementation details.

## Stretch

Design an integration-test data strategy using one of:

- A separate SQLite database per test.
- A reset database per test class.
- A transaction that is rolled back.

Explain its isolation, speed, and complexity tradeoffs. The project uses a fresh SQLite database file per test run (not the EF InMemory provider) so tests exercise real migrations, constraints, and cascades — after your analysis, say whether you agree with that choice.

## Blocked?

Submit the rule, your proposed input, and what you do not know how to assert. Do not wait until you can write complete test code.
