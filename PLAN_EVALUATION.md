# Evaluation of the Original Plan

## Executive Assessment

The original plan has a strong delivery shape but an unrealistic technical ceiling. Its cumulative project, pre-work, peer support, and session rhythm are good. Its content density would cause beginners to imitate code without understanding it and force the instructor to rush the most important backend concepts.

The revision keeps the useful structure and changes the learning contract from "cover many .NET topics" to "prove a small set of backend capabilities."

## Keep

1. One project built incrementally.
2. Pre-work before every session.
3. Foundation, core, and stretch paths.
4. Portfolio evidence and final demo.
5. Office hours and peer review.
6. A concrete artifact in every session.

## Critical Issues

### 1. The promise exceeds 24 hours

"Junior-ready" or "highly qualified" cannot be guaranteed, especially for five trainees with no .NET background. Promise a validated backend foundation and an individual continuation path.

### 2. The plan optimizes for topic coverage

The original core includes C#, HTTP, controllers, middleware, DI, two EF sessions, AutoMapper, Repository, Unit of Work, FluentValidation, Identity, JWT, roles, policies, Serilog, OpenAPI, versioning, secrets, xUnit, IIS/Azure, and Docker. Coverage is not competence.

### 3. SQL is only pre-work

Database design is a core backend skill. Teach keys, relationships, constraints, joins, and transactions before EF Core hides them.

### 4. Patterns appear before a need

EF Core already provides repository and Unit of Work behavior. Generic wrappers can create pass-through layers and hide useful query capabilities. AutoMapper and MediatR add indirection before trainees can reason about boundaries.

Teach thin controllers, DTO projection, and one focused service. Keep other patterns as comparisons or stretch work.

### 5. Authentication scope is too large

Identity, JWT creation, roles, ownership, refresh-token rotation, and revocation can consume several sessions. Security is required, but authentication implementation should use a prepared starter and stay outside the minimum graduation floor.

### 6. Testing is late and too small

One unit test in Session 7 makes testing look decorative. Add tests when the first business rule appears and include API integration behavior.

### 7. AI use is undefined

AI should not mean code generation. Trainees need a repeated workflow for problem definition, small prompts, review, compilation, tests, documentation checks, and rejection of bad suggestions.

### 8. Assessment does not prove ownership

Attendance, commits, and a demo can be satisfied with copied code. Add repository checkpoints, negative cases, and a short individual explanation.

### 9. The project is oversized

Users, Projects, Tasks, Assignments, many-to-many relationships, roles, and deployment create too many failure points. Projects and Tasks are sufficient for CRUD, relationships, validation, querying, testing, and architecture.

### 10. Deployment is provider-dependent

Free tiers and platform procedures change. Grade release readiness and reproducible setup. Keep public deployment optional unless infrastructure is guaranteed.

## Main Changes

| Original | Revised |
|---|---|
| .NET 8 | .NET 10 LTS for a new 2026 cohort, unless company standard requires .NET 8 |
| SQL Server/LocalDB required | SQLite default; SQL Server optional/company-required |
| Four-entity project | Project and TaskItem core |
| Repository + Unit of Work required | Direct EF Core plus focused service boundary |
| AutoMapper required | Explicit DTO projection |
| MediatR/CQRS mid-course stretch | Later stretch after core completion |
| Identity/JWT required for all | Security required; auth implementation target/stretch |
| Testing introduced in Session 7 | Unit and integration testing in Session 6 |
| AI not defined | AI verification workflow in every session |
| Attendance-oriented certificate | Evidence-based rubric and three outcomes |

## Success Measure

The internship succeeds when a beginner independently implements and explains one database-backed endpoint with validation, correct HTTP behavior, DTO mapping, async EF Core access, a test, and verified AI assistance. Experienced trainees should complete the wider core API and one production-oriented stretch feature.

