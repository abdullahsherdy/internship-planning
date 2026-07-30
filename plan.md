# .NET Backend Internship - Revised Delivery Plan

**Client:** Netpoints  
**Format:** Online, 8 sessions x 3 hours = 24 hours, twice per week  
**Cohort:** 20 trainees with mixed experience  
**Primary stack:** .NET 10 LTS, C#, ASP.NET Core Web API with controllers, EF Core, SQLite/SQL Server, xUnit, Git/GitHub  
**Project:** Task Tracker REST API

---

## 1. Honest Goal

Twenty-four hours cannot graduate a highly qualified backend engineer. 
It can create a strong foundation, correct bad habits early, and prove that each trainee can build and explain a small backend system.

### Graduation floor: required from every trainee

By the end, each trainee must be able to:

1. Explain an HTTP request from client to API to database and back.
2. Use core C#: types, classes, interfaces, collections, LINQ, exceptions, nullability, and async/await.
3. Build and debug an ASP.NET Core endpoint.
4. Design a small relational model with keys, relationships, and constraints.
5. Use EF Core migrations and async CRUD operations.
6. Use request/response DTOs instead of exposing database entities.
7. Validate input and return correct status codes and Problem Details.
8. Use dependency injection and explain why a service exists.
9. Write at least one unit test and one API integration test.
10. Use Git with meaningful commits and a reproducible README.
11. Use AI while verifying, testing, and explaining its output.

### Target outcome: expected from active trainees

- Complete Projects and Tasks CRUD.
- Add one relationship, filtering, pagination, validation, and global error handling.
- Document the API with OpenAPI and local setup instructions.
- Add tests for one business rule and API success/failure behavior.
- Publish a portfolio repository and deliver a short technical demo.

### Stretch outcome: advanced trainees

- Authentication and ownership authorization.
- Sorting, optimistic concurrency, idempotency, or richer filtering.
- CI build/test workflow and deployment.
- Architecture comparison or one CQRS feature after the core works.

The certificate should state completion of a ".NET Backend Foundations Internship", not imply professional mastery.

---

## 2. Cohort Strategy

The interview file contains 20 trainees:

- 3 advanced trainees with shipped backend or stronger .NET experience.
- 6 intermediate trainees with practical .NET exposure.
- 6 trainees with theoretical or very basic experience.
- 5 beginners with no .NET experience.

Teach one shared core path and differentiate the depth of practice.

| Track | Expected work | Support model |
|---|---|---|
| Foundation | Complete the required endpoint and guided homework | Starter branch, hints, office hours |
| Core | Complete the required feature independently | Normal homework and review |
| Stretch | Add one production concern and review a peer PR | Stretch backlog and review checklist |

Advanced trainees are reviewers, not unpaid teaching assistants. Rotate pairs so beginners still develop independent problem-solving skills.

Run a 45-minute baseline diagnostic before Session 1. Adjust groups from demonstrated ability, not only self-reported experience.

---

## 3. Teaching Principles

1. **Concept before framework:** explain HTTP, relational data, validation, and boundaries before framework syntax.
2. **One vertical slice:** every session changes the same application and ends with observable behavior.
3. **Working software before architecture:** start with one small API. Extract a service when business logic creates a reason.
4. **No pattern collecting:** generic repository, Unit of Work wrappers, AutoMapper, MediatR, CQRS, and microservices are not core requirements.
5. **Retrieval practice:** start with a no-notes recap and finish with an exit ticket.
6. **Frequent feedback:** review small pull requests instead of one large final submission.
7. **Explainable AI:** generated code is acceptable only when the trainee can explain, run, test, and revise it.
8. **Backend over technology memorization:** connect C# and ASP.NET features to system behavior and tradeoffs.

---

## 4. Project Scope

### Core domain

**Project**

- `Id`
- `Name`
- `Description`
- `CreatedAtUtc`

**TaskItem**

- `Id`
- `ProjectId`
- `Title`
- `Description`
- `Status`
- `DueDate`
- `CreatedAtUtc`

### Required behavior

- `GET /api/projects`
- `GET /api/projects/{id}`
- `POST /api/projects`
- `PUT /api/projects/{id}`
- `DELETE /api/projects/{id}`
- `GET /api/projects/{projectId}/tasks`
- `POST /api/projects/{projectId}/tasks`
- `PATCH /api/tasks/{id}/status`
- Filter tasks by status.
- Paginate at least one collection.
- Return validation errors, `404`, and `201 Created` correctly.

### Scope controls

- Start with one API project and one test project.
- Use controllers because they expose request boundaries and common enterprise .NET structure clearly.
- Use SQLite for the instructor starter and automated tests. Use SQL Server only if Netpoints requires it and setup is verified before Session 1.
- Do not add Users, Assignments, roles, refresh tokens, or deployment until the core API is complete.
- Authentication is a target/stretch feature and cannot block graduation.

---

## 5. Session Format

- **0:00-0:15:** retrieval quiz, previous checkpoint, blockers
- **0:15-0:45:** concept model with diagrams/examples
- **0:45-1:20:** instructor live coding with debugging narration
- **1:20-1:30:** break
- **1:30-2:25:** guided implementation in pairs
- **2:25-2:45:** independent checkpoint
- **2:45-3:00:** review, exit ticket, next pre-work

Require a submitted artifact before trainees leave. Do not reserve the final 30 minutes for unstructured Q&A every session.

---

## 6. Eight-Session Syllabus

### Session 1 - Backend Mental Model, C#, and the First Endpoint

**Concepts**

- Backend responsibilities; client, server, process, port, HTTP, application, and database.
- .NET SDK/runtime, solution, project, compilation, and NuGet.
- C# types, methods, classes, records, collections, nullability, exceptions, and async basics.
- Compiler errors and debugger basics.

**Build**

- Create the solution and controller-based API.
- Implement `GET /api/health` and `GET /api/projects`.
- Send requests through an `.http` file or Postman.

**Checkpoint:** Change an endpoint, set a breakpoint, send a request, and explain the response.

**Homework:** Add `GET /api/projects/{id}` with in-memory data and README run instructions.

**Stretch:** Add query-string filtering.

### Session 2 - HTTP, REST, Contracts, and In-Memory CRUD

**Concepts**

- Method, path, query, headers, body, status, JSON, and content type.
- Resource routes and idempotency.
- Model binding, DTOs, server-side validation, and dependency injection.
- `200`, `201`, `204`, `400`, `404`, `409`, and `500`.

**Build**

- Implement Project POST, PUT, and DELETE against an in-memory service.
- Return `CreatedAtAction` and structured validation errors.

**Checkpoint:** A create/read sequence with correct status codes.

**Homework:** Complete Project CRUD and submit a pull request.

**Stretch:** Handle duplicate names and justify `409 Conflict`.

### Session 3 - SQL and Data Modeling Before EF Core

**Concepts**

- Tables, primary/foreign keys, nullability, constraints, indexes, and one-to-many modeling.
- `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `JOIN`, and transactions.
- What an ORM solves and what it hides.

**Build**

- Draw the Project/Task schema.
- Configure EF Core, `DbContext`, entities, and mappings.
- Create and inspect the migration before applying it.
- Replace Project in-memory persistence.

**Checkpoint:** POST persists data and GET returns it after restarting the API.

**Homework:** Persist Project CRUD and include the reviewed migration.

**Stretch:** Add a unique Project name constraint and map its failure.

### Session 4 - Relationships, LINQ, DTO Projection, and Async I/O

**Concepts**

- Relationships and navigation properties.
- `IEnumerable` versus `IQueryable`, deferred execution, and LINQ composition.
- `Select`, `AsNoTracking`, cancellation, and N+1 awareness.
- API contracts versus persistence entities.

**Build**

- Add TaskItem and its Project relationship.
- Implement nested task endpoints using direct DTO projection.
- Add status filtering and simple pagination.

**Checkpoint:** Query one project's tasks without returning EF entities.

**Homework:** Finish Task create/list behavior and a filtered request example.

**Stretch:** Add sorting through an allow-list.

### Session 5 - OOP, SOLID, Service Boundaries, and Errors

**Concepts**

- Encapsulation, invariants, interfaces, composition, and polymorphism.
- SOLID through concrete examples, not definitions alone.
- Thin controllers, application services, and dependency direction.
- Validation failures, expected domain failures, unexpected exceptions, and safe logging.

**Build**

- Add a task status transition rule.
- Move the rule into a focused service with an interface where testing/substitution has value.
- Add centralized exception handling, Problem Details, and structured logging.

**Checkpoint:** An invalid transition returns a predictable response and log entry.

**Homework:** Refactor one feature and explain which responsibility moved and why.

**Stretch:** Compare direct `DbContext` use with a repository and justify any added boundary.

### Session 6 - Testing, Debugging, and Delivery Discipline

**Concepts**

- What unit and integration tests prove.
- Arrange, Act, Assert; happy path, boundary, and negative cases.
- Substitution without over-mocking.
- `WebApplicationFactory`, isolated data, and deterministic tests.
- Branches, small commits, pull requests, and code review.

**Build**

- Unit test the status transition rule.
- Integration test one GET and one invalid POST.
- Debug one seeded defect using logs, a breakpoint, and a failing test.

**Checkpoint:** `dotnet build` and `dotnet test` pass.

**Homework:** Add one negative integration test and resolve one peer-review comment.

**Stretch:** Add a GitHub Actions build/test workflow.

### Session 7 - Security, Authentication, and AI-Assisted Engineering

**Concepts**

- Authentication versus authorization.
- Password hashing, tokens, claims, ownership, secrets, and least privilege.
- Broken authorization, over-posting, injection, leaked secrets, and unsafe logs.
- AI context, prompting, hallucination, stale APIs, insecure suggestions, and verification.

**Build**

- Core group: use a supplied auth starter and enforce one ownership rule.
- Foundation group: threat-model the API and fix input, secret, or logging issues.
- Use AI to propose tests and review code, then verify every accepted finding.

**Checkpoint:** Explain one rejected AI suggestion and the evidence used to reject it.

**Homework:** Complete an AI review record and resolve its highest-value verified issue.

**Stretch:** Implement authentication independently or add policy-based authorization.

### Session 8 - Hardening, Documentation, Demo, and Next Steps

**Concepts**

- Environment configuration, secrets, health checks, logging, release readiness, and deployment flow.
- Definition of done and continued learning.

**Build**

- Run the release checklist.
- Improve OpenAPI metadata and README setup.
- Optionally deploy to the company-approved target.

**Demo**

- Four minutes: architecture, one request, one failure, one test, one lesson.
- One minute transition/feedback.
- Twenty trainees require about 100 minutes.

**Final checkpoint:** Repository, rubric, test result, API demo, and individual reflection.

---

## 7. AI Usage Curriculum

AI is used in every session, not isolated in one lecture.

### Workflow: Explain, Plan, Generate, Verify, Reflect

1. **Explain:** state the problem in your own words.
2. **Plan:** ask for options or a small plan before code.
3. **Generate:** request a small change with project constraints.
4. **Verify:** compile, test, inspect behavior, and check official docs when needed.
5. **Reflect:** record what was accepted, changed, or rejected and why.

### Rules

- Never submit code you cannot explain at the required level.
- Never paste secrets, personal data, or confidential code into public AI tools.
- Never ask AI to produce the whole final project.
- Prefer small diffs, test ideas, explanations, and review questions.
- Treat package names, APIs, versions, security advice, and performance claims as unverified.
- `dotnet build`, `dotnet test`, runtime behavior, and official docs are evidence; confidence is not evidence.
- Record meaningful assistance in `AI-NOTES.md` or the pull request.

| Session | AI practice |
|---|---|
| 1 | Explain a compiler error, then verify the fix |
| 2 | Critique an API contract and status codes |
| 3 | Review a schema/migration for constraints or accidental drops |
| 4 | Explain a LINQ query and predict execution |
| 5 | Review SOLID claims and reject unnecessary abstractions |
| 6 | Generate edge-case ideas, then implement only valid tests |
| 7 | Perform a security review using a verification checklist |
| 8 | Improve README/demo structure without inventing behavior |

---

## 8. Pre-Work Architecture

Every pack uses:

1. Why this matters
2. Outcomes
3. Timebox
4. Must do
5. Check yourself
6. Submit before session
7. Foundation support
8. Stretch
9. Blocked?

Required work is 30-45 minutes, uses one resource per concept, and produces one small artifact. Send it 48 hours before the session; submission is due 12 hours before. Begin the session with a five-question retrieval check.

The actual send-ready packs are indexed in `pre-work/README.md`. They include the setup gate and one preparation file for each of Sessions 1-8.

---

## 9. Assessment and Graduation

Attendance is necessary but is not evidence of skill.

### Evidence

- Baseline diagnostic.
- Session exit tickets.
- Repository checkpoints after Sessions 2, 4, and 6.
- Final project rubric and demo.
- Individual explanation interview of 5-7 minutes during the final week or office hours.

### Rubric

| Area | Weight | Minimum evidence |
|---|---:|---|
| HTTP and API contract | 15 | Correct routes, methods, and status codes |
| C# and code clarity | 15 | Understandable code, nullability, async usage |
| Data modeling and EF Core | 20 | Relationship, migration, constraints, async queries |
| Validation and errors | 10 | Invalid input and missing resource behavior |
| Design and SOLID reasoning | 10 | Responsibilities separated for a stated reason |
| Tests and debugging | 15 | One unit and two integration scenarios |
| Git and documentation | 5 | Meaningful history and reproducible README |
| Explanation and AI verification | 10 | Defends code and shows verified AI use |

### Graduation rule

- At least 70/100.
- No zero in HTTP, data, validation, or explanation.
- Project builds and the required endpoint is demonstrated.
- Individual checkpoints are the trainee's own work.

Certificate outcomes:

- **Completed:** met the graduation floor.
- **Completed with distinction:** 85+ and meaningful stretch work.
- **Participated:** attended but did not yet meet the technical floor.

---

## 10. Instructor Delivery System

Prepare before Session 1:

1. Tagged instructor repository with one tag per session.
2. Trainee starter branch and completed reference branch.
3. `.http` request files for all required endpoints.
4. Known-issues sheet for SDK, database, HTTPS, migrations, and ports.
5. Rubric and pull-request review checklist.
6. Recovery branch for trainees who miss a session.
7. Sanitized authentication starter for Session 7.
8. Release checklist and demo template.

Prepare for each session:

- Learning outcomes and one concept diagram.
- Live-code script with checkpoints and finished commit.
- Guided exercise and foundation hints.
- Core acceptance criteria and stretch task.
- Exit ticket and homework rubric.

---

## 11. Recommended Paths After the Internship

### Foundation path

1. C# fundamentals and debugging.
2. OOP and small console exercises.
3. HTTP and REST.
4. SQL and relational modeling.
5. ASP.NET Core CRUD.
6. EF Core and tests.

### Job-ready .NET backend path

1. Deeper C#, LINQ, async, exceptions, and memory basics.
2. ASP.NET Core middleware, configuration, validation, and security.
3. SQL query plans, indexing, transactions, and concurrency.
4. Authentication, authorization, and OWASP API risks.
5. Unit, integration, and contract testing.
6. Docker, CI/CD, deployment, logging, and monitoring.
7. Architecture patterns after maintaining a modular monolith.

### Advanced path

1. Compare controllers and Minimal APIs.
2. Domain modeling and modular boundaries.
3. CQRS where read/write needs genuinely differ.
4. Caching, queues, background jobs, idempotency, and resilience.
5. Profiling, load testing, and database optimization.
6. Distributed systems after mastering operational fundamentals.

---

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Environment is not ready | Setup proof and optional clinic before Session 1 |
| Pre-work is ignored | Artifact due before class and retrieval quiz |
| Advanced trainees disengage | Review ownership and CI/security/concurrency stretch work |
| Trainees copy instructor or AI | Individual change, explanation checkpoint, and AI notes |
| Architecture consumes the course | Delay abstractions and require a concrete reason |
| Database setup consumes live time | SQLite default; SQL Server only when pre-verified |
| Authentication blocks progress | Provide starter; keep auth outside graduation floor |
| Deployment provider fails | Grade release readiness; deployment remains optional |
| Demos exceed Session 8 | Strict four-minute format and pre-tested requests |
| A trainee misses a session | Recovery branch, recording, checklist, and review |

---

## 13. Decisions to Confirm With Netpoints

- Exact trainee count: interview file lists 20; original plan says about 22.
- Certificate outcome policy.
- Whether setup clinic and individual checks can happen outside the 24 hours.
- Required IDE and database.
- Whether .NET 10 LTS is acceptable.
- Delivery language and terminology policy.
- Approved AI tools and privacy rules.
- Deployment target and credits.
- Public or private repositories.

---

## 14. Technology Decision

Use .NET 10 LTS for a new internship running in 2026. As of July 24, 2026, .NET 10 is the active LTS release through November 14, 2028, while .NET 8 is in maintenance and reaches end of support on November 10, 2026.

If Netpoints standardizes on .NET 8, teach the same concepts on .NET 8 and explain the upgrade context. Do not mix SDK versions within the cohort.

Official lifecycle reference: https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core
