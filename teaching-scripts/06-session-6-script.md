# Session 6 Teaching Script - Testing, Debugging, and Delivery Discipline

**Status: DRAFT — finalize 24h before delivery after reading Session 5 exit tickets.**
**Sprint 3, second half — story TT-12. Repo checkpoint #3 follows this session.**
**Session outcome:** `dotnet build` and `dotnet test` pass on every repo; the transition rule is exhaustively unit-tested; one GET and one invalid POST are integration-tested over real HTTP; a seeded defect has been found test-first.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-6-start` / `session-6-done`; foundation branch `s6-foundation` (test project wired, one example test of each kind).
- [ ] **Seeded-defect branch** `s6-bughunt` pushed: bug A = pagination off-by-one (`Skip(page * pageSize)`), bug B = swallowed exception in PATCH (`catch { return Ok(); }` — the horror is the point).
- [ ] CI workflow YAML snippet ready for stretch (build `--warnaserror` + test).
- [ ] Known-issues: test project can't see `Program` (missing `public partial class Program`), SQLite file locks between test runs, xUnit not discovering tests (wrong SDK/project type).

## 0:00-0:15 — Standup: Quiz + Blockers

1. The three error boxes — name them and their status codes. *(invalid input 400 / expected domain 400·404·409 / unexpected 500)*
2. Why does `TryTransition` return a result instead of throwing? *(expected failure ≠ exception)*
3. One sentence: why does `TaskStatusService` exist? *(the rule needed one owner, testable without HTTP/DB)*
4. From pre-work: what do the three A's stand for? *(Arrange, Act, Assert)*
5. From pre-work: what can an integration test prove that a unit test cannot? *(the pieces work together — routing, serialization, DB, middleware)*

## 0:15-0:45 — Concept Block: What Does a Test Actually Prove?

### Concept 1: The confidence problem (Problem → Solution, 10 min)

**Problem framing:**

> "Right now, how do you *know* your API works? You clicked through the `.http` file. Honest answers: you know it worked *once*, *on your machine*, *for the cases you remembered to click*, *as of the last time you clicked*. Tomorrow you refactor the service — do you re-click all twenty requests? Will you remember the Done→InProgress edge? At 2 a.m.? That's the product a test buys: **your manual check, written down, running in seconds, forever.**"

- "A test is not extra work after the work. It's the same verification you already do, made permanent."
- The two kinds we write, mapped to what they prove:

| Kind | Proves | Speed | Our target |
|---|---|---|---|
| Unit | One rule, in isolation — *the logic is right* | ms | every edge of the state machine |
| Integration | The assembled system over real HTTP — *the wiring is right* | ~1s | one happy GET, one invalid POST |

- "Why not unit-test the controller with a mocked DbContext? Because then we test our mock's imagination, not EF Core's behavior. Our integration tests hit a **real SQLite file with real migrations** — constraints, cascades, serialization all get exercised. Substitute *sparingly*; our service is pure, so it needs no mocks at all — that purity was last session's design paying this session's rent."

### Concept 2: Anatomy of a good test (8 min)

Live-read one test (from the foundation branch): **Arrange** (build inputs) / **Act** (one call) / **Assert** (check the outcome, not the internals). Rules, stated once:

- "Test *behavior through the public surface*, never private internals — refactoring must not break tests if behavior held." *(Liskov's promise from S5, now enforced by tooling)*
- "One logical assertion per test name; the name is a sentence: `Todo_to_Done_is_rejected`."
- "Happy path, boundary, negative — every feature gets all three questions asked."
- "Deterministic or delete it: no shared state, no time bombs (`DateTime.Now` in asserts), no test order dependency."

### Concept 3: Debugging as method, not vibes (8 min)

> "Second half of today you hunt two bugs I planted. Before you touch code, the method — three steps, always the same: **1) Reproduce** — a failing request or better, a failing test, because a bug you can't reproduce is a rumor. **2) Locate** — logs to find the neighborhood, breakpoint to find the house. **3) Fix and lock** — the failing test from step 1 goes green and stays in the suite as the bug's tombstone."
>
> "The anti-method you'll be tempted by: change something, re-run, squint. That's not debugging, that's gambling with extra steps."

Sprint tie-in: "This is also where **delivery discipline** lands: small branches, commits that reference stories, PRs reviewed against the contract and the Definition of Done — from today, *tests green* joins the DoD. No green, no merge."

**Transition:** "Let's make the state machine unbreakable."

## 0:45-1:20 — Live Coding: TT-12

1. **Test project:** `dotnet new xunit -o tests/TaskTracker.Tests`, add to solution, reference the API project. Show `public partial class Program { }` in Program.cs — "this line is why the factory can see our app."
2. **Unit — the transition matrix as data (blueprint §7.3):**
   ```csharp
   [Theory]
   [InlineData(TaskStatus.Todo, TaskStatus.InProgress, true)]
   [InlineData(TaskStatus.InProgress, TaskStatus.Done, true)]
   [InlineData(TaskStatus.InProgress, TaskStatus.Todo, true)]
   [InlineData(TaskStatus.Done, TaskStatus.InProgress, true)]
   [InlineData(TaskStatus.Todo, TaskStatus.Done, false)]        // the business rule
   [InlineData(TaskStatus.Done, TaskStatus.Done, false)]        // no-op rejected
   public void Transition_rules_are_enforced(TaskStatus from, TaskStatus to, bool allowed)
   {
       var result = new TaskStatusService().TryTransition(from, to);
       Assert.Equal(allowed, result.Allowed);
   }
   ```
   "`[Theory]` + data = the whole rule table verified in one screen. When stretch adds `Cancelled`, they add rows — the test *is* the spec now."
3. **Run `dotnet test`** — savor the green. Then **break the service on purpose** (allow Todo→Done), re-run, watch it fail: "a test suite that can't fail is decoration. Always watch a new test fail once." Revert.
4. **Integration — `ApiFactory`** per blueprint §7.3 (fresh SQLite file per run, real migrations). Two tests: `GET /api/projects` → `200` + envelope shape; `POST` blank name → `400` + `content-type: application/problem+json`. Narrate: "this test boots the *entire* app in-process — routing, validation, middleware, EF, the file on disk. When it's green, the wiring is proven."
5. **⚠ Live bug hunt (the method, demonstrated):** switch to `s6-bughunt`, run the suite — pagination test fails. Reproduce (the failing test) → locate (log shows `LIMIT 10 OFFSET 10` for page 1 → breakpoint on the Skip line) → fix → green → "the test stays forever; this bug can never return unseen." Then bug B: nothing fails, but the PATCH swallows errors — "the scariest bug is the one your suite can't see. What test was *missing*?" *(the invalid-transition integration case)* Write it, watch it fail, fix, green.
6. **AI practice (session theme — edge cases, filtered):** ask AI for edge cases for the pagination endpoint. Triage its list live: `page=0` valid concern → test exists; `pageSize=-5` → add; "concurrent page drift" → real but out of scope, note for stretch; anything hallucinated → rejected aloud. "AI is a brainstorm partner; *you* own the test suite."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Pairs

Checklist: test project wired → transition matrix as `[Theory]` (all edges incl. forbidden + no-op) → break-the-service drill (watch one test fail, revert) → `ApiFactory` + the two integration tests → pull `s6-bughunt`, find both bugs *method-first* (failing test before fix, both documented in the PR).

- **Foundation** (`s6-foundation`): example tests given; they extend the matrix and write one integration test from the worked example; bug hunt guided with the "neighborhood" hint sheet.
- **Core:** full checklist.
- **Stretch:** GitHub Actions workflow — build `--warnaserror` + test on PR; red X → green check on a real PR is the deliverable. Plus one deliberate flaky-test discussion: find the `DateTime.UtcNow` assert risk in their own suite.

Rotation questions: "Show me a test failing." / "What does this test prove — logic or wiring?" / "Why no mock here?" / "Where's the tombstone test for bug A?"

## 2:25-2:45 — Independent Checkpoint

1. Write one *new* negative integration test: `PATCH` with a nonsense status string → `400`.
2. Run the full suite; screenshot the green run **including test count**.
3. Written, 3-5 sentences: "Yesterday you 'knew' your API worked. What do you know *now*, and what exactly is the difference?"

This + the bug-hunt PR = **repo checkpoint #3**. Gate rule: no green suite by S8 = cannot pass the demo rubric (say it plainly, kindly, now — two sessions of runway remain).

## 2:45-3:00 — Wrap: Sprint 3 Review

Board: TT-10/11/12 → Done. Cold-calls: what unit vs integration each prove; the three-step debugging method; why we watched a test fail; what joined the DoD today.

Homework: one more negative integration test of their choosing + resolve one peer-review comment on their open PR (the review economy from plan_v2 — stretch trainees' reviews land here). Exit ticket. Announce Sprint 4 ("It ships"): "The API is trustworthy. Next: who is *allowed* to use it — security, auth, and the session where you get to catch the AI being confidently wrong."

## Post-Session

- [ ] Tag `session-6-live`; push.
- [ ] Checkpoint #3 triage within 48h; recovery-track trainees get the single-endpoint test plan (one unit + one integration on their slice).
- [ ] Verify the **auth starter** end-to-end on a clean machine — S7 depends on it (plan_v2 risk register).
- [ ] Exit tickets → S7 opener.
