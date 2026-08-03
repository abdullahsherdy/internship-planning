# Session 3 Teaching Script - Project Creation, Database Design, EF Core, and Repositories

**Status: DRAFT — finalize 24h before delivery after reading Session 2 exit tickets.**
**Scope revision 2026-08-02 (rev 2 — full entity build):** Session 2 did not reach project creation. Session 3 now builds the **entire data layer in one session**: solution created live, full database design, **both entities (Project + TaskItem)**, EF Core with one reviewed migration, and a **simple concrete repository per aggregate** (amended from ADR-004; no generics, no Unit of Work). Later sessions deepen this codebase (projection/query internals S4, services S5, tests S6) — they do not add entities. Companion doc: `03-session-3-reference.md` (all commands, packages, and code-complete listings — teach from it).
**Sprint 2 kickoff ("It remembers") — stories TT-06/07/08 compressed.**
**Session outcome:** Every trainee has a running solution created from scratch, the hand-drawn two-table schema, both entities persisted via EF Core + SQLite behind `IProjectRepository`/`ITaskRepository`, the contract's Project CRUD + Task endpoints responding, one migration read aloud before applying, cascade delete proven in the viewer, and restart-survival proof.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-3-start` (empty solution scaffold) / `session-3-done`; foundation branch `s3-foundation` (solution + entities + DbContext + complete Tasks side given; `ProjectRepository`, DI wiring, and migration left to do).
- [ ] SQLite viewer ready (DB Browser for SQLite or VS Code SQLite extension); fallback `sqlite3` CLI tested.
- [ ] A **broken migration** prepared for the AI exercise: renames `Name` via drop-and-add (data loss) instead of `RenameColumn`.
- [ ] Verify on your machine: `dotnet --version` (net10), `dotnet ef --version`, and the full command sequence from the reference doc §1–2 runs clean.
- [ ] Known-issues sheet: `dotnet-ef` not installed → command not found; running commands from the solution folder instead of `src/TaskTracker.Api` → "no project found"; missing `Design` package → its exact error message; "no such table" → migration not applied; `.db` locked on Windows → close the viewer first.
- [ ] Checkpoint results in hand; track list confirmed individually (never publicly ranked).

## 0:00-0:10 — Standup: Quiz + Sprint 2 Kickoff

Quiz (previous session + pre-work; read the room, don't grade):

1. POST twice = two resources, PUT twice = one state. What's the word? *(idempotency)*
2. Which status code and header does a successful create return? *(201 + Location)*
3. What is dependency injection giving you, in one sentence? *(you ask for a contract; the container supplies the implementation)*
4. From pre-work: what does a **primary key** guarantee? *(unique, non-null row identity)*
5. From pre-work: what does a **foreign key** *prevent*? *(orphan rows — a task pointing at a project that doesn't exist)*

**Kickoff (2 min):** "Today is the biggest build day so far: we create the real solution from zero, design its database on paper before any framework touches it, and by the end your data survives a restart. Sprint 2 is **'It remembers'** — TT-06."

## 0:10-0:40 — Live Coding Part 1: Project Initial Create

Typed, not pasted. Trainees follow along on their machines.

1. **Scaffold:**
   ```bash
   dotnet new sln -n TaskTracker
   dotnet new webapi -o src/TaskTracker.Api --use-controllers
   dotnet sln add src/TaskTracker.Api
   ```
   Narrate the anatomy: `.sln` is the container, `.csproj` is the project, `--use-controllers` because we want explicit classes, not minimal-API magic, while learning.
2. Delete the WeatherForecast sample. Create the folder skeleton: `Controllers/`, `Contracts/`, `Domain/`, `Data/`, `Data/Repositories/` — draw the architecture diagram (reference doc §2) while the folders appear. **Folder rules, said once:** "Contracts cross the HTTP boundary; Domain never does; Data is everything persistence."
3. `HealthController` (5 minutes, from memory — this was homework territory): `GET /api/health` → status object. Run it, hit it from the `.http` file.
4. `Project` domain class + `ProjectResponse` record + `ProjectsController` with `GetAll` returning a **hard-coded in-memory list**. "Notice the pain we're about to fix: restart the API — *the data is whatever I typed in code*. Real data dies with the process. Hold that thought for 30 minutes."
5. Commit + push: "empty skeleton first, then one commit per capability — atomic commits are part of your grade evidence."

**Check:** "Point at the line where the route is decided." / "Why does `ProjectResponse` exist when `Project` has the same properties?" *(contract vs. storage shape)*

## 0:40-1:10 — Concept Block: Database Design Before the ORM

### Concept 1: Tables, keys, constraints (Problem → Solution) — 15 min

**Problem framing:** "Task Tracker data in one big JSON file: every task carries its project's full name and description. Rename the project — how many places change? A typo makes two spellings — which is right?" Let them find it: **duplication means contradiction is possible.**

**Solution — normalize live, drawing the full two-table schema by hand (the drawing is the session artifact — reference doc §3.1):**

```
projects:   id (PK), name (NOT NULL), description (NULL), created_at_utc (NOT NULL)
task_items: id (PK), project_id (FK → projects.id, NOT NULL), title, status, due_date, created_at_utc
```

- "Each fact lives once; tasks *point*. The pointer is a **foreign key**, and the database *enforces* it — insert `project_id = 999` and the DB refuses. Constraints are validation that cannot be bypassed, not even by a bug, not even by another app."
- Nullability in schema ≡ `string?` in C# — "same question, two type systems that must agree."
- **The delete question (make them vote):** "Delete a project with 12 tasks — refuse, orphan, or cascade?" All three are legitimate; *not choosing* is illegitimate. We choose cascade and will test it.
- Walk the decisions table (reference doc §3.2): int PKs, status as TEXT, `DueDate` as a date not a moment. "Every row of that table is a decision someone will ask you to defend in a review."

**Check:** "Which constraint stops two projects with the same name?" *(unique — today's stretch)*
**Transition:** "Schema is the nouns. SQL is the verbs — fifteen minutes of verbs, because you can't supervise a translator whose target language you can't read."

### Concept 2: SQL — the verbs (compressed, 10 min, live in the SQLite viewer)

Pre-seeded SQLite file; type, run, narrate:

```sql
SELECT name, created_at_utc FROM projects WHERE id = 1;
INSERT INTO projects (name, created_at_utc) VALUES ('From SQL!', datetime('now'));
UPDATE projects SET description = 'edited in raw SQL' WHERE id = 1;
SELECT p.name, t.title FROM projects p JOIN task_items t ON t.project_id = p.id;  -- the JOIN moment
BEGIN; DELETE FROM task_items; ROLLBACK;  -- count rows before/after: all-or-nothing
```

On the JOIN: "the payoff of pointing instead of copying." On the transaction: "Session 4's `SaveChangesAsync` wraps your changes in exactly this."

### Concept 3: What an ORM solves and what it hides (5 min)

| EF Core solves | EF Core hides |
|---|---|
| SQL strings in C# (typo = runtime bomb) | The SQL it generates (can be terrible) |
| Manual row→object mapping | When queries execute (S4: deferred execution) |
| Schema drift (migrations = Git for schema) | The cost of what you ask (N+1 — S4 demo) |

> "Team rule: **you may only use the ORM for things you could do by hand slowly.** You just did. Everything it hides gets dragged into the light next session with a query log."

## 1:10-1:20 — Break

## 1:20-2:15 — Live Coding Part 2: EF Core + Repositories + Both Entities (TT-06/07/08)

1. **Packages** (narrate NuGet — reference doc §1):
   ```bash
   dotnet add package Microsoft.EntityFrameworkCore.Sqlite
   dotnet add package Microsoft.EntityFrameworkCore.Design
   dotnet tool install --global dotnet-ef
   ```
   "`Sqlite` is the translator's dialect; `Design` is what the migration tool needs at design time; `dotnet-ef` is the tool itself. If a tutorial says `Microsoft.EntityFrameworkCore.Tools`, that's the Visual Studio console flavor — we standardize on the CLI so every machine works identically."
2. **All entities** (reference doc §4): `TaskStatus` enum, `Project`, `TaskItem` — the C# mirror of the hand drawing. Narrate `null!` on the required navigation once, and the `System.Threading.Tasks.TaskStatus` name-clash if anyone hits it.
3. **DbContext with both entities** (reference doc §6.1). Map every fluent line back to the drawing: "`IsRequired` = NOT NULL, `HasOne/WithMany/HasForeignKey` = the FK arrow, `OnDelete(Cascade)` = the vote you took ten minutes ago."
4. **Repositories — the promise and the how (reference doc §6.2–6.3):** write `IProjectRepository` + `ProjectRepository` slowly and fully narrated; then `ITaskRepository` + `TaskRepository` *fast*, as pattern repetition — "same anatomy, new noun."
   - "The interface is the *promise*; the class is the *how*. The controller sees only the promise. Session 6 payoff: tests hand the controller a fake promise, no database needed."
   - **Guardrails as law:** one concrete repository per aggregate — never `Repository<T>`, never Unit of Work ("`SaveChangesAsync` inside the repo *is* the unit of work"), never return `IQueryable` ("point at `GetPageForProjectAsync` — the query is composed AND executed inside; it never escapes").
   - Write the honesty TODO live in `GetPageAsync`: `// TODO(S4): project TaskCount instead of loading tasks` — "deliberately naive today; Session 4 measures why."
5. **Wire DI + connection string** (reference doc §8). **⚠ Scripted deliberate error:** "forget" `AddScoped<IProjectRepository, ProjectRepository>()`, run, hit an endpoint → `Unable to resolve service for type 'IProjectRepository'`. "Read it with me — the container says exactly what nobody registered." Fix, rerun. Mention the lifetime trap: a Singleton repo holding a Scoped DbContext — "AI generates this; now you can spot it."
6. **The migration ritual (core of the session):**
   ```bash
   dotnet ef migrations add InitialCreate
   ```
   **Do not apply. Open it. Read it aloud, whole file** — two `CreateTable`, the FK with `onDelete: CASCADE`, the composite index; every line maps to the drawing. Only then:
   ```bash
   dotnet ef database update
   ```
   Open the `.db` in the viewer — both tables physically exist. "Migrations are Git for your schema."
7. **AI practice (session theme — review a migration for damage):** show the prepared **broken migration** (rename via drop+add). Ask the AI: "what happens to existing data if this runs?" Verify its claim against the operations yourselves. Rule: "a migration review asks one question first — **does any operation destroy data?**"
8. **Controllers:** `ProjectsController` through `IProjectRepository` with the contract's paging (reference doc §7.1), narrated fully. Then `TasksController` (reference doc §7.2) *fast*, same anatomy: exists-check → 404, parse status → 400, repo, map, status code. Say what's deferred out loud: "transition rules (Done→Todo?) are Session 5's service; the not-in-the-past due date is S5 too."
9. **The payoffs (theatrical, in order):**
   - POST a project, POST two tasks into it. **Stop the process. Count to three. Start it.** GET — *everything's there.* "Data that survives."
   - `DELETE` the project → viewer: `SELECT COUNT(*) FROM Tasks;` → 0. "The database honored the decision you voted on. Session 6 turns this into an automated test."

## 2:15-2:45 — Guided Pairs

Timing note: the live-coding block ran long by design — pairs *finish* rather than rebuild. Checklist: complete anything not yet typed from the live session → both repositories wired in DI → migration created and **read aloud to your partner before applying** (pairs attest) → apply, inspect both tables in viewer → all contract endpoints answering in the `.http` file → cascade proof (delete a project, count its tasks in the viewer) → restart-survival screenshot pair (POST before / GET after restart).

- **Foundation** (`s3-foundation`): solution + entities + DbContext given; they write `ProjectRepository` from the interface, do the migration ritual, wire DI, and run the cascade + restart proofs. `TaskRepository`/`TasksController` given complete — they read it and annotate the anatomy. Hint sheet: exact CLI commands + the three most common errors with meanings.
- **Core:** full checklist; `TasksController` typed themselves following the Projects anatomy.
- **Stretch:** unique index on `Name` via a *second* migration (additive migrations, lived) + catch `DbUpdateException` → `409` per contract. Written: one sentence on why the DB constraint must exist even though the API validates. *(The API isn't the only possible writer.)*

Rotation questions: "Show me NOT NULL in three places — drawing, C#, migration." / "Delete the `.db` file and rebuild it from migrations alone." / "Why is the repository Scoped and not Singleton?" / "Point at where the `IQueryable` lives and dies." / "What SQL did `FirstOrDefaultAsync` run? Guess, then find out." *(query-logging teaser)*

**AI rule for the block:** AI may explain errors and review migrations — the workflow demonstrated. Any line AI writes, you explain token-by-token to your partner. I will ask.

## 2:45-2:55 — Independent Checkpoint

1. Add a nullable `Priority` (int?) column to `Project`: model → migration created → **migration file read** → applied → visible in viewer.
2. Screenshot: migration file + column in the DB viewer.
3. Written, 3-5 sentences: "Explain to a junior what a migration is and why we read it before applying, using today's rename-disaster example."

Pass / needs-follow-up only. Anyone who edits the `.db` by hand instead of migrating gets the office-hours invite.

## 2:55-3:00 — Wrap

Cold-calls: what a FK prevents; the cascade decision and its risk; the two-column ORM table from memory; why the migration gets read; what the controller knows about EF Core now. *(Nothing — it knows two promises.)*

Homework: every contract endpoint working against the database, PR referencing TT-06/07/08 with the reviewed migration. Exit ticket. Announce: "The API is structurally complete. Next session we open the hood: a query log shows what EF Core actually ran, the `Include`-for-count TODO gets fixed with projection and *measured*, and 50,000 rows meet an index."

## Post-Session

- [ ] Tag `session-3-live`; push.
- [ ] Anyone without restart-survival proof gets the recovery-branch conversation *now* (plan_v2 §5 — S4 is the graduation-floor core).
- [ ] Exit tickets → S4 opener; seed `seed-perf.sql` demo data for the S4 index demonstration.
- [ ] **Doc debt:** propagate the S3 scope change (project creation moved here; repository amendment to ADR-004) into plan.md, plan_v2.md, project-blueprint.md, MILESTONES.md, and pre-work/03 — currently only recorded in this script and `03-session-3-reference.md`.
