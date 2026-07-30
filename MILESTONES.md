# Internship Milestones - The Big Picture

Companion to `plan.md`. One page that answers: *where should everything stand at every point in time?* Three parallel tracks run through the internship — the **project**, the **trainees' proven skills**, and the **instructor's delivery assets**. A session is "done" only when all three tracks hit their milestone.

## The One-Sentence Arc

> An empty folder becomes a tested, documented, database-backed REST API — and a mixed cohort becomes people who can each build and **explain** one such endpoint alone.

```
S1        S2         S3          S4           S5          S6         S7          S8
process → contract → persistence → real queries → boundaries → evidence → security → release
(it runs) (it's correct) (it survives) (it scales)  (it's designed) (it's proven) (it's safe) (it ships)
```

Everything before Session 5 is "make it work." Sessions 5–6 are "make it right." Sessions 7–8 are "make it trustworthy and ship it."

---

## Milestone Table

**Gate 0 — before Session 1 (hard gate):** every trainee has `dotnet --version` proof, a sent health request, and a baseline diagnostic result. Tracks assigned from demonstrated ability. *No trainee enters Session 1 unverified — environment debugging never happens live.*

| # | Session | Project state at end (API milestone) | Skill proven (trainee milestone) | Evidence collected |
|---|---------|--------------------------------------|----------------------------------|--------------------|
| 1 | Mental model + first endpoint | Runs locally; `GET /api/health`, `GET /api/projects` from in-memory list via DTO record; `.http` file | Traces request → port → route → method → JSON in own words; uses breakpoint | Checkpoint screenshot + 3-5 written sentences |
| 2 | HTTP, REST, contracts | Full Project CRUD in-memory; `201 CreatedAtAction`, validation errors, correct 200/204/400/404 | Chooses correct method + status code and says why; explains DTO vs entity | **Repo checkpoint #1** (PR with CRUD) |
| 3 | SQL + EF Core | Data survives restart: SQLite, `DbContext`, first migration reviewed-then-applied; Project persistence swapped in | Draws the schema; reads a migration before applying; explains what the ORM hides | Persisted CRUD + reviewed migration in PR |
| 4 | Relationships, LINQ, async | TaskItem + 1-to-many; nested task endpoints; DTO projection with `Select`; status filter + pagination; async/`CancellationToken` throughout | Explains `IQueryable` vs `IEnumerable` and why projection avoids over-fetching | **Repo checkpoint #2** (relationship + filtered query) |
| 5 | OOP, SOLID, boundaries | First business rule (status transition) in a focused service behind an interface; ProblemDetails + centralized exception handling + structured logging | Justifies *why this service exists* — names the responsibility that moved | Refactor PR with written reasoning |
| 6 | Testing + delivery discipline | Unit test on the rule; 2 integration tests (`WebApplicationFactory`, one negative); a seeded bug found via failing test; `dotnet build` + `dotnet test` green | Writes Arrange-Act-Assert; debugs with logs + breakpoint + test, not guesswork | **Repo checkpoint #3** (green test run) |
| 7 | Security + AI engineering | One ownership rule enforced (core: auth starter; foundation: threat-model fixes); AI security review performed and verified | Rejects one AI suggestion **with evidence**; distinguishes authn vs authz | AI review record with verified findings |
| 8 | Release + demo | Release checklist passed; OpenAPI + reproducible README; optional deploy | Delivers 4-min demo: architecture, one request, one failure, one test, one lesson | Final rubric + demo + reflection |

**Post-Session 8 (final week):** 5-7 min individual explanation interview per trainee → certificate decision (Completed / Distinction / Participated) per the plan.md rubric (70/100 floor, no zero in HTTP/data/validation/explanation).

---

## The Three Assessment Gates (don't let these slip)

| Gate | After | Proves | If a trainee misses it |
|---|---|---|---|
| Checkpoint #1 | S2 | Can express a contract (CRUD + status codes) | Office hours before S3 — S3 builds on this API |
| Checkpoint #2 | S4 | Can persist and query real data | Recovery branch + pair support; this is the graduation-floor core |
| Checkpoint #3 | S6 | Can prove behavior with tests | Must clear before S8; untested code can't pass the demo rubric |

Rule of thumb: **a trainee two checkpoints behind cannot recover inside the 24 hours** — move them to the recovery branch and target the graduation floor only (the single explained endpoint), not the full API.

---

## Concept Debt Ledger ("on faith today, explained later")

Every session borrows a little understanding; every debt has a scheduled repayment. Track it — unrepaid debt is how trainees end up imitating code.

| Borrowed in | Concept taken on faith | Repaid in |
|---|---|---|
| S1 | `[ApiController]`, model binding (`{id}` homework), `async` mention | S2 (binding/conventions), S4 (async) |
| S2 | DI container "magic" (`AddScoped` just works) | S5 (dependency direction, why interfaces) |
| S3 | What EF Core generates under the hood | S4 (LINQ → SQL translation), S6 (testing against it) |
| S4 | Pagination correctness at scale | Post-internship path (indexes, query plans) |
| S7 | Token internals (starter-provided auth) | Stretch / post-internship path |

---

## Instructor Asset Milestones

| Ready by | Asset |
|---|---|
| Gate 0 | Tagged instructor repo (tag per session), trainee starter + reference branches, known-issues sheet, rubric + PR checklist, baseline diagnostic |
| S1 −48h | Pre-work pack 01 sent (packs always go out 48h before; submissions due −12h) |
| Each session −24h | Teaching script finalized (`teaching-scripts/NN-*.md`), live-code script rehearsed, exit ticket + quiz loaded |
| S3 | Recovery branch live (first realistic drop-off point) |
| S6 | Seeded-defect branch for the debugging exercise |
| S7 −1 week | Sanitized auth starter tested end-to-end |
| S8 −48h | Release checklist + demo template + demo schedule (20 × 5 min ≈ 100 min) |

**Script-writing milestone for this workspace:** one teaching script per session, written from the template in `teaching-scripts/01-session-1-script.md`, each finalized after reading the *previous* session's exit tickets (scripts adapt to the cohort; don't batch-write all eight far in advance — draft early, finalize −24h).

---

## Definition of Success (from PLAN_EVALUATION.md)

The internship succeeds when a **beginner** independently implements and explains one database-backed endpoint with validation, correct HTTP behavior, DTO mapping, async EF Core access, and a test — and **experienced trainees** complete the wider core API plus one production-oriented stretch feature. Everything in this file exists to hit that sentence.
