# Session 2 Teaching Script - HTTP, REST, Contracts, and In-Memory CRUD

**Status: DRAFT — finalize 24h before delivery after reading Session 1 exit tickets.**
**Sprint 1, second half — stories TT-03, TT-04, TT-05.**
**Session outcome:** Every trainee completes Project CRUD against in-memory data with correct status codes (`200/201/204/400/404`), structured validation errors, and can justify each code choice. The API contract is **frozen** at the end of this session.

---

## Before the Session (Instructor Prep)

- [ ] Repo tags `session-2-start` (= session-1-done) and `session-2-done` ready.
- [ ] `api-contract.md` (from plan_v2 §6) in the starter repo — today's ceremony freezes it.
- [ ] S1 exit tickets read; the top "still fuzzy" item gets the first 5 concept minutes.
- [ ] S1 checkpoint follow-ups: office-hours trainees contacted; direction-confusion cases ("controller sends the request") get a 1-question warm-up in the quiz.
- [ ] Foundation starter branch `s2-foundation` (controller skeletons with method signatures, bodies empty).
- [ ] Known-issues additions: `[FromBody]` confusion, PUT returning 200-with-body vs 204, route template typos.

## 0:00-0:15 — Standup: Quiz + Blockers

Quiz (from S1 + pre-work pack 02):

1. A request arrives at the API. Name the two things routing uses to pick the method that runs. *(path + HTTP method)*
2. What status code says "you asked for something that does not exist"? *(404)*
3. Why did we return a `ProjectResponse` record instead of the `Project` class? *(contract ≠ storage shape)*
4. What is the *body* of an HTTP request? When does a GET have one? *(payload; conventionally never)*
5. From pre-work: which method is *idempotent* — POST or PUT — and what does that word mean? *(PUT; same request twice = same end state)*

Homework debrief (3 min): show one good `GET /api/projects/{id}` homework solution (anonymized) and one common mistake — returning `200` with `null` body for a missing id. "That's today's whole subject: the response *is* the product."

## 0:15-0:45 — Concept Block: The Contract Is the Product

### Concept 1: HTTP anatomy — read a real one (Problem → Solution)

**Problem:** "Yesterday you clicked 'Send Request' and JSON appeared. Magic is a debt. Let's read the actual messages." Open the `.http` raw response pane from S1.

Dissect live, labeling every part: request line (method, path, version) → headers ("metadata about the message — `Content-Type` says how to *read* the body") → blank line → body. Then the response: status line → headers → body.

> "Everything the client and server will ever say to each other fits in this envelope. There is no other channel. Every feature you ever ship is: choose method + path + body shape + status codes. That set of choices has a name — the **contract**."

**Check:** "The server wants to tell the client 'created, and here's where it lives.' Which parts of the envelope carry that?" *(status 201 + Location header)*

**Transition:** "So which method and path do we choose, and by what rule? That's REST."

### Concept 2: REST resources and the status-code vocabulary (10 min)

- "REST's big idea: URLs name **things** (nouns), methods are the **verbs**. `/api/projects` is a shelf; `/api/projects/7` is one box on it. `GET /api/getProjectById?id=7` is how it looks when nobody decided."
- Build the verb table *with them* (cold-call): GET=read, POST=add to shelf, PUT=replace box, DELETE=remove box.
- **Idempotency, problem-first:** "Your mobile app times out and retries. The request ran twice. For which verbs is that safe?" Walk the table: GET yes, PUT yes (same replacement), DELETE yes (already gone), POST **no** — two boxes. "This is why POST creates and PUT replaces. Not style — retry-safety."
- Status codes as a decision tree (draw): worked? → had a body to return? `200` : `204`; created something? `201`+Location. Client's fault? → bad input `400`, no such thing `404`, conflict `409`. Our fault? `500`. "Seven codes cover this whole internship. The skill is *choosing consciously*."

**Transition:** "The last concept: how does a JSON body become a C# object in your method's parameters — and what stops garbage from getting in?"

### Concept 3: Model binding, validation, and DI (10 min)

- **Binding:** "You already used it: `Get(int id)` — the framework read `{id}` from the route. Today's version: `Create(CreateProjectRequest request)` — the framework reads the JSON body, builds the record, hands it over. Route → parameters, query → parameters, body → one complex object."
- **Validation, problem-first:** "What if `name` is an empty string 5,000 characters of emoji? Rule: **all input is hostile until validated**, and validation lives on the server — client-side checks are courtesy, not security." Show `[Required]`, `[StringLength]` on the DTO; `[ApiController]` auto-runs them and returns a `400` Problem Details — "there's the S1 faith debt repaid: *that's* one of the things `[ApiController]` was doing."
- **DI in one diagram:** "Our controller needs a place to keep projects. It could `new` one up — but then every controller has its *own* list, and later its own database connection. Instead: register the thing once (`builder.Services.AddSingleton<...>`), and ask for it in the constructor. The framework hands it in. Why bother? Swap-ability — in Session 3 the in-memory store becomes a database and the *controller barely changes*. That is the whole sales pitch of DI; the deep version comes in Session 5."

**Transition:** "Concepts done: envelope, nouns-and-verbs, codes, binding, validation, DI. Now we implement TT-03, 04, 05 — and every choice we make, we'll point at the contract."

## 0:45-1:20 — Live Coding: Project CRUD (TT-03/04/05)

Refactor first (5 min): extract the static list into `InMemoryProjectStore`, register as singleton, inject into the controller. Narrate the DI payoff explicitly.

**POST (TT-04), problem→solution sequence:**

1. Write `CreateProjectRequest(string Name, string? Description)` with `[Required]`, `[StringLength(100)]` on `Name` (via property syntax on the record).
2. Naive version returning `Ok(project)` — then challenge: "Contract says 201 + Location. Why does the client care?" *(so it can fetch/poll the new resource without guessing the id)*
3. Fix with `CreatedAtAction(nameof(GetById), new { id = project.Id }, response)` — send it, show the `Location` header in the raw pane. **This is the session's money shot.**
4. Send invalid body (`"name": ""`) — read the entire Problem Details response aloud, field by field: "machine-readable, field-level, standard shape. You will never invent a custom error JSON in this course."

**⚠ Scripted deliberate error:** in `GetById`, write route `[HttpGet("{projectId}")]` but parameter `int id`. Request → `id` is `0` → wrong 404 behavior. Debug live with a breakpoint ("the debugger shows `id = 0` — where did my 7 go?"). **AI practice (session theme — critique a contract):** paste the route + signature, ask the AI *what's inconsistent*; verify its answer against the docs page for route templates; fix; retest.

**PUT + DELETE (TT-05), fast:** PUT returns `204` — "we replaced it; the client already knows what it sent." DELETE `204`; missing id `404`. **Idempotency demo:** send the same PUT twice (same state, same 204), same POST twice (two projects!) — "there's the table from the concept block, running."

**Payoff pain:** restart the API. All created projects gone — again. "Second time you've watched this. Thursday we make it stop."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Pairs

Checklist: implement TT-03/04/05 exactly per `api-contract.md` — POST with validation + `201`+Location; GET by id `200/404`; PUT `204/400/404`; DELETE `204/404`; all requests in the `.http` file; every wrong-input case demonstrated.

- **Foundation** (`s2-foundation` branch): controller skeletons given; they fill bodies. Hint sheet maps each AC to the helper (`CreatedAtAction`, `NotFound()`, `NoContent()`).
- **Core:** from their own S1 repo, no scaffold.
- **Stretch:** duplicate-name check returning `409` + a written 3-sentence justification of why `409` and not `400` (TT-04 stretch AC). Yousef + confirmed stretch: also first **peer review** — review one Core pair's PR against the contract using your checklist.

Rotation questions: "Show me your 404 path — now make it happen." / "Why 204 and not 200 here?" / "Point at the line where validation runs." *(trick — it's the framework, before their code)*

## 2:25-2:45 — Independent Checkpoint

1. Add a `[StringLength(500)]` limit to `Description`, prove with a failing request.
2. Screenshot a full create→read sequence: POST `201` (Location visible) → GET on that Location `200`.
3. Written, 3-5 sentences: "A client sends POST with an empty name. Trace what happens and why the client sees what it sees."

Pass = correct codes + the trace mentions validation happening *before* their method body.

## 2:45-3:00 — Wrap: Contract Freeze + Sprint 1 Review

**Contract-freeze ceremony (3 min):** display `api-contract.md`. "As of now this document is *frozen*. Changing it requires a team discussion — like production, where a contract change breaks real clients. Your reviews cite this file, not opinions."

Cold-calls: idempotent verbs and why POST isn't; when 201 vs 200 vs 204; what `[ApiController]` did for us today.

**Sprint 1 review framing:** "Sprint 1 committed TT-01 through TT-05. Board check —" *(move cards live)* "— homework closes the sprint: finish Project CRUD, open a **pull request** referencing story IDs. That PR is repo checkpoint #1 — the first evidence gate."

Exit ticket (standard 4 questions) + homework: complete CRUD, PR opened, one deliberately failing request documented in the PR description ("show me your API refusing bad input — a feature is also what it *rejects*").

## Post-Session

- [ ] Tag `session-2-live`; push.
- [ ] Review PRs as checkpoint #1 within 48h; track-confirmation decisions per plan_v2 §8 (this gate confirms/moves provisional tracks).
- [ ] Exit tickets → S3 opener; update known-issues sheet.
- [ ] Send S3 pre-work (SQL + EF Core) 48h ahead; it references the frozen contract.
