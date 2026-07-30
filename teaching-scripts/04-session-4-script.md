# Session 4 Teaching Script - Relationships, LINQ, DTO Projection, and Async I/O

**Status: DRAFT — finalize 24h before delivery after reading Session 3 exit tickets.**
**Sprint 2, second half — stories TT-07, TT-08 (+TT-09 stretch). Repo checkpoint #2 follows this session.**
**Session outcome:** TaskItem exists with a real one-to-many; nested task endpoints work with status filtering and pagination via DTO projection; every trainee has *counted* an N+1 and *watched* an index change a query plan.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-4-start` / `session-4-done`; foundation branch `s4-foundation` (TaskItem entity + migration given; endpoints skeletal).
- [ ] `seed-perf.sql` (100 projects × 500 tasks) tested — the index demo (blueprint §5.3) must run in under 3 minutes.
- [ ] EF query logging pre-configured snippet ready (`LogTo(Console.WriteLine, LogLevel.Information)` or `"Microsoft.EntityFrameworkCore.Database.Command": "Information"`).
- [ ] Known-issues: enum binding case sensitivity, `DateOnly` JSON format, cascade surprise ("my tasks vanished"), pagination off-by-one.

## 0:00-0:15 — Standup: Quiz + Blockers

1. What does a migration file contain, and what do we do before applying it? *(schema-change operations; read it)*
2. A task row has `project_id = 999` but no project 999 exists. What stops this? *(FK constraint)*
3. `BEGIN ... ROLLBACK` — what did we prove? *(transactions: all-or-nothing)*
4. From pre-work: what's the difference between `IEnumerable` and `IQueryable` in one sentence? *(in-memory sequence vs composable not-yet-run query)*
5. From pre-work: `projects.Where(...)` — has any SQL run on this line? *(no — deferred execution)*

## 0:15-0:45 — Concept Block: Asking the Database Good Questions

### Concept 1: Navigation properties — the relationship in C# (7 min)

**Problem:** "In SQL, task→project is a JOIN you write each time. In C#, wouldn't you rather write `task.Project.Name`?" Show `TaskItem` from blueprint §4.1: `ProjectId` (the FK — the truth) + `Project` (the navigation — the convenience) + `List<TaskItem> Tasks` on the other side.

> "Navigation properties are the ORM's biggest gift and its biggest trap in one feature: write `p.Tasks` and EF Core *can* fetch them for you — the question that separates juniors from seniors is *when* and *how many queries* that costs. Hold that thought for the demo."

### Concept 2: LINQ and deferred execution (Problem → Solution) — 10 min

**Problem:** "50,000 tasks. I want page one of project 42's in-progress tasks — ten rows. The worst possible plan: fetch all 50,000 into C#, then filter. How do I make sure the *database* does the work?"

Live in a scratch endpoint with **query logging on** (turn it on now, leave it on all session — "today the ORM works with the lights on"):

```csharp
var q = db.Tasks.Where(t => t.ProjectId == 42);        // log: nothing. No SQL ran.
q = q.Where(t => t.Status == TaskStatus.InProgress);    // still nothing. We're COMPOSING.
var list = await q.ToListAsync(ct);                     // NOW one SQL query — with both filters in WHERE
```

> "`IQueryable` is a question under construction. `ToListAsync` is pressing Enter. Everything you chain before Enter becomes SQL; the database does the work. That's the whole model."

**⚠ Scripted deliberate error (the classic):** insert `.ToList()` mid-chain — `db.Tasks.ToList().Where(...)`. Query log shows `SELECT *` with **no WHERE**. "One method call moved the filter from the database to my process — 50,000 rows over the wire to keep 10. The code *works*. It's just wrong. This is why the query log is open." **AI practice (session theme):** paste both versions, ask AI to explain the difference and *predict the SQL of each*; verify predictions against the actual log.

### Concept 3: Projection, AsNoTracking, and async-for-real (8 min)

- **Projection:** "`Select(t => new TaskResponse(...))` inside the query = the SQL selects *only those columns*, and entities never leak to the contract — one line, two wins." (S1's DTO habit, now with a performance reason.)
- **AsNoTracking:** "EF watches every entity it loads in case you edit it. For read-only queries that bookkeeping is pure waste — `AsNoTracking()` says 'just reading, don't watch.' Rule: reads get it, writes don't."
- **Async, debt repaid (S1's one-sentence promise):** "Your API has a limited crew of workers (threads). A DB query is *waiting*, not working. Synchronous = the worker stands at the oven doing nothing while 40 requests queue. `await` = the worker hands off and serves others; when the DB answers, someone picks it up. That's why every I/O call in this codebase is `await ...Async(ct)` — and `ct`, the CancellationToken, lets a disconnected client's work stop instead of finishing for nobody."

**Transition:** "Compose, project, don't track, await. Build TT-07 and TT-08 with all four."

## 0:45-1:20 — Live Coding: Tasks, Filtering, Pagination — then the Two Demos

**Part 1 — TT-07 (10 min):** Add `TaskItem` + `TaskStatus` enum (blueprint §4.1), fluent config incl. cascade + **the composite index** (put it in now; it pays off in Part 3), migration → *read* → apply. `TasksController`: `POST /api/projects/{projectId}/tasks` (404 if project missing — "check the parent exists; the FK would refuse anyway, but a clean 404 beats a 500"), nested GET with projection per blueprint §7.2 pattern.

**Part 2 — TT-08 (10 min):** status filter (`string?` → `Enum.TryParse` → `400` on garbage — "allow-list thinking: parse, don't trust") + pagination envelope `PagedResponse<T>`: `CountAsync` then `Skip/Take`, both visible in the query log as SQL (`LIMIT`/`OFFSET`). "Page size capped at 50 — an API without a cap invites someone to ask for everything."

**Part 3 — the two performance demos (12 min — the session's centerpiece):**

**Demo A: count the N+1.** Endpoint listing projects with task counts the naive way (loop over projects, touch `p.Tasks.Count`). Run against seeded data with the log open — **have trainees count the queries scrolling past** (101). Fix with projection (`Select(p => new { p.Name, Count = p.Tasks.Count() })`) → **one** query with a subquery. "Same output. 101 vs 1. The ORM did exactly what we asked both times — the skill is asking well. You just watched the most common performance bug in industry."

**Demo B: ask the query plan** (blueprint §5.3, scripted there):
1. Load `seed-perf.sql` (50k rows). Run the hot query in the SQLite viewer with `EXPLAIN QUERY PLAN` **with the index dropped**: → `SCAN task_items`.
2. "SCAN = reads every row. Fine at 50k on SQLite; an outage at 50M under load."
3. Re-add `IX_task_items_project_id_status` (via the migration from Part 1) → `SEARCH ... USING INDEX`.
4. Mental model, verbatim: "An index is a sorted copy of chosen columns — it trades write cost and storage for read speed. And the database *tells you* whether it used one. Never guess; ask the plan."
5. Composite-order intuition — phone book: "sorted by last-name-then-first finds 'Ahmed, *'; sorted by first name doesn't. That's why `(project_id, status)` and not the reverse — show the plan difference."

**Honesty beat:** "Real query tuning — SQL Server plans, statistics, isolation levels — is a career, and it's on your continuation path. What you now own is the *method*: measure with the log, ask the plan, then decide."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Pairs

Checklist: TaskItem + migration (read aloud to partner) → TT-07 endpoints with 404-on-missing-project → TT-08 filter + pagination envelope exactly per contract → query logging ON and one screenshot of the SQL your list endpoint runs → reproduce the N+1 and its fix in your own repo (both query counts recorded).

- **Foundation** (`s4-foundation`): entity + migration given; they build the GET-with-projection endpoint from a worked example and run both demos guided.
- **Core:** full checklist.
- **Stretch (TT-09):** allow-list sorting (`?sortBy=dueDate|createdAtUtc|title`, anything else → `400`) — switch expression, no dynamic LINQ strings. Plus: run `EXPLAIN QUERY PLAN` on their sorted query and write two sentences on whether the index helped and why/why not.

Rotation questions: "Where in this chain does SQL actually run?" / "Show me the SQL your filter produced." / "Why is `AsNoTracking` here but not on your POST?" / "What does `ct` do if I close the browser mid-request?"

## 2:25-2:45 — Independent Checkpoint

1. Add a `?dueBefore=2026-09-01` filter to the nested task list (compose one more `Where`).
2. Screenshot the query log line proving the date filter is in the SQL `WHERE`, not in memory.
3. Written, 3-5 sentences: "Explain N+1 to a teammate using today's numbers, and state how you'd detect it in a codebase you've never seen." *(looking for: query logging / counting queries per request)*

This checkpoint + this week's PR = **repo checkpoint #2** — the graduation-floor core gate.

## 2:45-3:00 — Wrap: Sprint 2 Review

Board: TT-06/07/08 to Done (or honestly back to Backlog). Cold-calls: deferred execution in one sentence; the phone-book index answer; what projection buys twice; async in the restaurant metaphor.

Homework: finish task create/list per contract + one filtered request example in the PR + the N+1 before/after query counts in the PR description. Exit ticket includes: **"What question would you ask the query plan at your next job?"**

Announce Sprint 3 ("It's trustworthy"): "The API works. Next: the first *business rule* — and with it, the first real design decision about where code should live. Pre-work is OOP and SOLID; it lands tomorrow."

## Post-Session

- [ ] Tag `session-4-live`; push.
- [ ] Checkpoint #2 triage within 48h — this is the recovery-branch decision point (plan_v2 §5): anyone without persisted CRUD + a working filtered query moves to the graduation-floor slice now.
- [ ] Exit tickets → S5 opener.
