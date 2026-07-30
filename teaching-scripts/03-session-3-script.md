# Session 3 Teaching Script - SQL and Data Modeling Before EF Core

**Status: DRAFT — finalize 24h before delivery after reading Session 2 exit tickets.**
**Sprint 2 kickoff ("It remembers") — story TT-06.**
**Session outcome:** Projects persist across restarts via EF Core + SQLite; every trainee has drawn the schema by hand, read a migration file aloud, and can name two things the ORM is hiding.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-3-start` / `session-3-done`; foundation branch `s3-foundation` (DbContext written, migration not yet created).
- [ ] SQLite viewer ready (DB Browser for SQLite, or VS Code SQLite extension) — trainees install it via pre-work; have the fallback (`sqlite3` CLI) tested.
- [ ] A **broken migration** file prepared for the AI exercise: one that renames `Name` by drop-and-add (data loss) instead of rename.
- [ ] Checkpoint #1 results in hand: confirmed track list announced individually (not publicly ranked).
- [ ] Known-issues: `dotnet-ef` tool not installed globally, migration created in wrong directory, "no such table" (migration not applied), file path/connection string issues on Windows.

## 0:00-0:15 — Standup: Quiz + Sprint 2 Kickoff

Quiz:

1. POST twice = two projects, PUT twice = one state. What's the word and why does it matter? *(idempotency; retries)*
2. Which status code and header does a successful create return? *(201 + Location)*
3. Where does validation of `[Required]` happen — before or inside your action method? *(before)*
4. From pre-work: what does a **primary key** guarantee? *(unique, non-null identity of a row)*
5. From pre-work: what does a **foreign key** *prevent*? *(orphan rows — a task pointing at a project that doesn't exist)*

**Sprint 2 kickoff (2 min):** "Sprint 1 delivered 'It responds' — CRUD with a real contract. Sprint 2 is **'It remembers'**: TT-06, projects survive restart, and next session TT-07/08, tasks with filtering. You've watched your data die twice. Today we fix it — but *not* by learning a framework first. We learn the database first, because EF Core is a translator, and you can't supervise a translator whose target language you can't read."

## 0:15-0:45 — Concept Block: The Database Before the ORM

### Concept 1: Tables, keys, constraints (Problem → Solution) — 12 min

**Problem framing:** "Here's my Task Tracker data in one big JSON file: every task carries its project's full name and description. Project gets renamed — how many places must change? A typo makes two spellings — which is right?" Let them find the sickness: **duplication means contradiction is possible.**

**Solution — normalize live, drawing the schema by hand (this drawing is the session artifact):**

```
projects: id (PK), name (NOT NULL), description (NULL), created_at_utc (NOT NULL)
task_items: id (PK), project_id (FK → projects.id, NOT NULL), title, status, due_date, created_at_utc
```

- "Each fact lives once; tasks *point at* their project. The pointer column is a **foreign key** — and the database *enforces* it. Try to insert a task with `project_id = 999` — the DB refuses. Constraints are validation that cannot be bypassed, not even by a bug, not even by a different app touching the same DB."
- Nullability in schema = `string?` in C#: "same idea, same question — can this be absent? — answered in two type systems that must agree."
- **The delete question (make them decide):** "Delete project 1. It has 12 tasks. What should happen?" Take votes: refuse / orphan / cascade. "All three are legitimate — what's *illegitimate* is not choosing. We choose cascade, and we'll write a test proving it, because cascade is convenient right up until someone deletes the wrong project."

**Check:** "Which constraint stops two projects named exactly the same?" *(unique — stretch adds it today)*

**Transition:** "Schema is the nouns. SQL is the verbs."

### Concept 2: SQL — the verbs (10 min, live in the SQLite viewer)

Open a pre-seeded SQLite file. Type, run, narrate — trainees follow in their viewer:

```sql
SELECT name, created_at_utc FROM projects WHERE id = 1;
INSERT INTO projects (name, created_at_utc) VALUES ('From SQL!', datetime('now'));
UPDATE projects SET description = 'edited in raw SQL' WHERE id = 1;
SELECT p.name, t.title FROM projects p JOIN task_items t ON t.project_id = p.id;  -- the JOIN moment
DELETE FROM task_items WHERE id = 3;
```

- On the JOIN: "This is the payoff of pointing instead of copying — the database reassembles the picture on demand, from single sources of truth."
- **Transactions in one demo:** `BEGIN; DELETE FROM task_items; ROLLBACK;` — count rows before/after. "All-or-nothing. Session 4's `SaveChangesAsync` wraps your changes in exactly this."

**Transition:** "You can now read and write this database by hand. So why use an ORM at all — and what's the fine print?"

### Concept 3: What an ORM solves and what it hides (5 min)

Two columns on the whiteboard:

| EF Core solves | EF Core hides |
|---|---|
| SQL strings scattered in C# (typo = runtime bomb) | The actual SQL it generates (can be terrible) |
| Manual row→object mapping | When queries execute (S4: deferred execution) |
| Schema drift (migrations version it like Git) | The cost of what you ask for (N+1 — S4's demo) |

> "Rule for this team: **you may only use the ORM for things you could do by hand slowly.** Today you proved you can. And everything it hides, we will drag into the light next session with a query log."

## 0:45-1:20 — Live Coding: EF Core + First Migration (TT-06)

1. **Install** (narrate NuGet doing its job): `Microsoft.EntityFrameworkCore.Sqlite`, `Microsoft.EntityFrameworkCore.Design`; `dotnet tool install -g dotnet-ef`.
2. **DbContext** — write `AppDbContext` per blueprint §5.2 (Project only today; TaskItem arrives S4). Map every fluent line back to the hand-drawn schema: "`IsRequired` = NOT NULL. `HasMaxLength(100)` = the constraint. The C# and the schema are two views of one design."
3. **Register + connection string** — `AddDbContext` with `UseSqlite`. **⚠ Scripted deliberate error:** "forget" this registration, run, hit the endpoint → runtime DI exception (`Unable to resolve service for type 'AppDbContext'`). "Read it with me — DI errors look scary and say exactly what's missing. The container is telling you: you asked for something nobody registered." Fix, rerun.
4. **The migration ritual (the core of the session):**
   ```bash
   dotnet ef migrations add InitialCreate
   ```
   **Do not apply it. Open it. Read it aloud, whole file.** "`CreateTable`, the columns, the PK... This file is *generated code about your data* — and generated code gets reviewed, always, because the generator doesn't know your intentions. Only after reading:"
   ```bash
   dotnet ef database update
   ```
   Open the `.db` file in the viewer — there's the table, physically. "Migrations are Git for your schema: versioned, ordered, reviewable."
5. **AI practice (session theme — review a migration for damage):** show the prepared **broken migration** (rename via drop+add). Ask the AI: "what happens to existing data if this runs?" Verify its claim *against the migration operations yourself*, then state the rule: "a migration review asks one question first — **does any operation destroy data?** Drop, and some alters, do."
6. **Swap the store:** replace `InMemoryProjectStore` with `AppDbContext` in `ProjectsController` — narrate how small the diff is ("Session 2's DI sales pitch, delivered"). Methods go async: `await db.Projects.FirstOrDefaultAsync(...)`, `await db.SaveChangesAsync(ct)` — "the one-sentence async promise from S1 comes due next session; today, follow the pattern."
7. **The payoff (make it theatrical):** POST a project. **Stop the process. Count to three. Start it.** GET — *it's there.* "Three sessions of dying data, fixed. TT-06 done."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Pairs

Checklist: add EF Core + SQLite to their repo → DbContext with fluent config matching the contract limits → create migration → **read it aloud to your partner before applying** (pairs attest to this) → apply, inspect in viewer → swap Project CRUD to the DbContext → prove restart survival with a screenshot pair (POST before / GET after restart).

- **Foundation** (`s3-foundation`): DbContext given; they do migration ritual + swap only. Hint sheet: exact CLI commands + the three most common errors and their meanings.
- **Core:** full checklist from scratch.
- **Stretch:** unique index on `Name` via a *second* migration (they experience additive migrations) + handle the violation: catch `DbUpdateException`, return `409` per contract. Written: one sentence on why the DB-level constraint must exist even though the API also checks. *(Answer: the API isn't the only possible writer.)*

Rotation questions: "Show me NOT NULL in three places — schema, C#, migration." / "Delete the .db file and rebuild it from migrations alone." / "What SQL do you think that `FirstOrDefaultAsync` ran? Now find out." *(query logging teaser)*

## 2:25-2:45 — Independent Checkpoint

1. Add a new column `Priority` (nullable int) to `Project` — model, migration created, **migration file read**, applied, visible in the viewer.
2. Screenshot: the migration file + the column in the DB viewer.
3. Written, 3-5 sentences: "Explain to a junior what a migration is and why we read it before applying, using today's rename-disaster example."

## 2:45-3:00 — Wrap

Cold-calls: what a FK prevents; the cascade decision and its risk; the two-column ORM table from memory; why the migration gets read.

Homework: Project CRUD fully persisted + the reviewed migration in a PR (referencing TT-06). Exit ticket. Announce: "Next session your API grows its second table — and we catch the ORM hiding things, with a query log and a 50,000-row database."

## Post-Session

- [ ] Tag `session-3-live`; push.
- [ ] Anyone who didn't reach the restart-survival proof gets the recovery-branch conversation *now* (per plan_v2 §5 recovery rule — S4 is the graduation-floor core).
- [ ] Exit tickets → S4 opener; seed `seed-perf.sql` demo data into your demo repo for the index demonstration.
