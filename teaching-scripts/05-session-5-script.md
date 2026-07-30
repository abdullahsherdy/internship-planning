# Session 5 Teaching Script - OOP, SOLID, Service Boundaries, and Errors

**Status: DRAFT — finalize 24h before delivery after reading Session 4 exit tickets.**
**Sprint 3 kickoff ("It's trustworthy") — stories TT-10, TT-11.**
**Session outcome:** The status-transition rule lives in `TaskStatusService` behind an interface, invalid transitions return predictable Problem Details, all failure paths are centralized, and every trainee can *name the reason* the service exists.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-5-start` / `session-5-done`; foundation branch `s5-foundation` (service class given, wiring left to them).
- [ ] The state-machine diagram from blueprint §6 ready to draw.
- [ ] A deliberately over-engineered "bad example" snippet prepared for the AI exercise (a generic repository wrapping DbContext for no reason).
- [ ] Known-issues: DI lifetime confusion (singleton vs scoped), enum parse in PATCH body, ProblemDetails middleware order.

## 0:00-0:15 — Standup: Quiz + Sprint 3 Kickoff

1. When does a LINQ chain actually run SQL? *(at materialization — `ToListAsync` etc.)*
2. What did the query plan say before vs after the index? *(SCAN → SEARCH)*
3. Why does projection (`Select`) belong inside the query? *(only needed columns; entities don't leak)*
4. From pre-work: encapsulation in one sentence. *(an object protects its own rules/state)*
5. From pre-work: name one SOLID letter and what it means in plain words.

**Sprint 3 kickoff:** "The API works and remembers. Sprint 3 makes it *trustworthy*: TT-10 — task status follows a workflow, garbage transitions refused. TT-11 — every failure, expected or not, returns one predictable shape and leaves a log line. Today is also the day the architecture earns its first new layer — and I'll make you tell *me* why."

## 0:15-0:45 — Concept Block: Where Should Code Live?

### Concept 1: The rule arrives — and the controller is the wrong home (Problem → Solution, 12 min)

**Problem framing (the whole session hangs on this):**

> "New requirement from the PO — me: a task can't jump from Todo straight to Done. Work can't finish before it starts. Simple rule. Now — *where does the `if` go?*"

Sketch option A live: the `if` inside `PatchStatus` in the controller. Then attack it with them:

- "Next month: a bulk-update endpoint. Same rule — copy the `if`? Now two truths that can drift." *(DRY: knowledge duplication)*
- "How do I test this rule today? Boot the web server, seed a DB, send HTTP — to check an `if`?" *(testability)*
- "The controller's job is HTTP: parse, dispatch, respond with codes. Deciding *workflow legality* is a different job." *(Single Responsibility — name it now)*

**Solution:** "Move the rule to a small class whose only job is answering: is this transition legal? That's a **service**. The controller stays thin: translate HTTP → ask the service → translate answer → HTTP."

**The honesty beat (anti-pattern vaccine):** "Notice what we did NOT do: no service until a *rule* existed. `GetAll` needs no service — a pass-through service is ceremony. Layers must pay rent. Session 3-4 code direct to DbContext stays exactly as it is."

### Concept 2: SOLID — through what we just did, not definitions (8 min)

Walk the letters *pointing at the design*, fast:

- **S** — controller does HTTP, service does the rule. Two reasons to change, two homes.
- **O** — "the transition table is data; adding `Cancelled` extends behavior without editing logic — you'll prove this in stretch."
- **L** — one sentence + promise: "anything claiming to be an `ITaskStatusService` must honor the same promises; the test suite next session *is* that contract."
- **I** — "our interface has one method. Fat interfaces force fake implementations; keep them small."
- **D** — "the controller depends on `ITaskStatusService`, not the concrete class — S2's DI plumbing finally shows its real reason: substitution. Next session a test substitutes... nothing actually — the service is pure. But the DbContext-swap in S3 was this principle live."

> "SOLID is not a checklist to recite; it's five names for the same instinct — code that changes together lives together, code that changes separately stays separable. When someone quotes SOLID to justify complexity, ask them what concrete change it protects. That question is Session 5's souvenir."

### Concept 3: The error taxonomy (8 min)

Draw three boxes:

| Kind | Example | Response | Log level |
|---|---|---|---|
| Invalid input | blank name, bad enum | `400` + field errors | none/Debug |
| Expected domain failure | Todo→Done, missing id | `400`/`404`/`409` + ProblemDetails reason | Information/Warning |
| Unexpected exception | NullReference, DB down | `500` ProblemDetails, **no stack trace in body** | Error, full detail *in the log* |

> "The client gets honesty without internals; the log gets internals without exception. And expected failures are **not exceptions** — a refused transition is the system working correctly. That's why the service returns a `TransitionResult`, not a throw. Exceptions are for the third box only."

**Transition:** "Build it: the rule, the service, the wiring, the middleware."

## 0:45-1:20 — Live Coding: TT-10 and TT-11

1. **State machine on screen** (blueprint §6 diagram) — narrate each edge; "Done→InProgress allowed: reopening is real life."
2. **Type `ITaskStatusService` + `TaskStatusService`** exactly per blueprint §6 — narrate: transition table as a `HashSet` of tuples ("the rule is *data*"); `TransitionResult` record ("expected failure as a return value — box two, not box three"); zero framework usings in the file ("`Domain/` stays clean — if this file needs ASP.NET, we've mislocated something").
3. **Wire it:** `AddScoped<ITaskStatusService, TaskStatusService>`; PATCH endpoint: parse enum (`400` on garbage) → load task (`404`) → `TryTransition` → on fail `Problem(statusCode: 400, detail: result.Reason)` → on success save + return updated DTO. Demo the full happy path and the Todo→Done refusal — **read the ProblemDetails reason aloud**: "the API explains itself."
4. **⚠ Scripted deliberate error (DI lifetime):** register the service as... actually inject `AppDbContext` into a `AddSingleton` registered helper "for convenience" → runtime exception: *cannot consume scoped service from singleton*. "The container just saved us from sharing one DB connection across all users forever. Lifetimes: singleton = one forever, scoped = one per request, transient = one per ask. Rule of thumb: **scoped unless you can argue otherwise**." Fix to scoped.
5. **TT-11 — centralized handling:** `AddProblemDetails()` + `UseExceptionHandler()`; throw a test exception in a scratch endpoint → client sees clean `500` ProblemDetails, console shows full stack + traceId. Match the `traceId` in body and log **on screen** — "that id is how you find *this* request among a million in production."
6. **Structured logging (15-min observability-lite, blueprint §8.5):** `_logger.LogWarning("Invalid transition {From}->{To} for task {TaskId}", ...)` — "events with fields, not prose. Grep-able, dashboard-able. Never log secrets or full request bodies."
7. **AI practice (session theme — reject unnecessary abstraction):** paste the prepared generic-repository snippet; ask AI "should we adopt this?" — most AIs equivocate or endorse. Dissect its answer against the pay-rent rule: "what concrete change does this wrapper protect? None we have. **Rejected, with reasons.** This is the checkpoint skill for Session 7 — disagreeing with the machine, with evidence."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Pairs

Checklist: service + interface in `Domain/` → wired via DI (scoped) → PATCH endpoint per contract (`200` updated task / `400` reason / `404`) → exception middleware on → one forced unexpected exception showing clean 500 + logged stack → warning log on refused transitions.

- **Foundation** (`s5-foundation`): service given; they wire DI, build the PATCH endpoint from the S2 pattern sheet, and demo both failure boxes.
- **Core:** full checklist; plus refactor any rule-ish `if` that crept into their controllers earlier.
- **Stretch:** add `Cancelled` status end-to-end (enum + table rows + migration for the CHECK constraint + tests-ready) — measure the diff size: "small diff = the O in SOLID, proven." **Or** the written comparison: direct DbContext vs repository wrapper, one page, must name a concrete change each approach helps or hurts.

Rotation questions: "Why does this service exist? One sentence." / "Show me box two vs box three in your code." / "Why scoped?" / "What would make you *add* a second service tomorrow?" *(a second rule — not a pattern)*

## 2:25-2:45 — Independent Checkpoint

1. Add one rule to the service: a task with a `DueDate` in the past cannot move to `Done` (deliberately debatable — any consistent implementation accepted).
2. Demo: the refusal response + its log line.
3. Written, 3-5 sentences: "Which class did you change, which classes did you NOT have to change, and what does that tell you about the boundary?"

## 2:45-3:00 — Wrap

Board: TT-10, TT-11 → Done. Cold-calls: the three error boxes; why the service returns a result instead of throwing; the pay-rent rule; scoped-vs-singleton.

Homework: refactor one feature of their own + a paragraph naming *which responsibility moved and why* (this paragraph is rubric evidence for "Design and SOLID reasoning"). Exit ticket. Announce: "Next session, the rule you built gets *proven* — every edge of that state machine becomes a test, and `dotnet test` becomes your new definition of confidence. Testing pre-work lands tomorrow; it's the most important pack of the course."

## Post-Session

- [ ] Tag `session-5-live`; push.
- [ ] Prepare the **seeded-defect branch** for S6 (an off-by-one in pagination + a swallowed exception — two bugs, one findable by log, one by test).
- [ ] Exit tickets → S6 opener.
