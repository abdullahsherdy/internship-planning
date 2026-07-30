# Session 2 Detailed Runbook — HTTP, REST, Contracts, In-Memory CRUD

**Follow-along delivery script. Say / Do / Ask format.**
Expands `02-session-2-script.md` (canonical draft — content decisions live there). Methodology rationale in `02-session-2-methodology.md`.
**Sprint 1, second half — stories TT-03, TT-04, TT-05.**
**Session outcome:** every trainee completes Project CRUD against in-memory data with correct status codes (200/201/204/400/404), structured validation errors, and can justify each code. Contract frozen at end.

Legend: **SAY** = speak (near-verbatim, adapt naturally) · **DO** = action on screen · **ASK** = check for understanding — wait 5 seconds, cold-call by name, never answer your own question.

---

## Prep (day before — from the draft checklist)

- [ ] Read S1 exit tickets; the top "still fuzzy" item replaces the first 5 concept minutes.
- [ ] Tags `session-2-start` and `session-2-done` ready; `api-contract.md` in starter repo.
- [ ] Foundation branch `s2-foundation` (controller skeletons, empty bodies) pushed.
- [ ] `.http` file prepared with: valid POST, empty-name POST, GET by id, GET missing id, PUT, DELETE.
- [ ] Sticky note on monitor: `0:15 concepts | 0:45 code | 1:20 break | 1:30 pairs | 2:25 checkpoint | 2:45 wrap`.
- [ ] Pick 3 names now for cold-calls (one per track) so you don't default to the same volunteers.

---

## 0:00–0:15 — Standup: Quiz + Homework Debrief

**SAY:** "Standup. Five questions, one minute each, then blockers. Answer before you're sure — wrong answers are how we find what to re-teach."

**ASK** (cold-call a different name per question):

1. "A request arrives at the API. Name the two things routing uses to pick the method that runs." *(path + HTTP method)*
2. "What status code says 'you asked for something that does not exist'?" *(404)*
3. "Why did we return a `ProjectResponse` record instead of the `Project` class?" *(contract ≠ storage shape)*
4. "What is the *body* of an HTTP request? When does a GET have one?" *(payload; conventionally never)*
5. "From pre-work: which is idempotent — POST or PUT — and what does that word mean?" *(PUT; same request twice = same end state)*

If Q5 gets blank stares, don't fix it now — **SAY:** "Park that. In 30 minutes you'll answer it yourself."

**DO:** show one good anonymized `GET /api/projects/{id}` homework solution, then the common mistake — `200` with `null` body for a missing id.

**SAY:** "This is today's whole subject in one bug: the response *is* the product. The client got 'success, here's nothing.' Today we learn to say exactly what we mean."

**Blockers round (2 min):** "Anyone blocked on environment or homework? Not 'confused' — *blocked*. Confusions we fix in the session; blockers we fix now or you pair up."

---

## 0:15–0:45 — Concept Block: The Contract Is the Product

*(If exit tickets flagged a fuzzy S1 item, spend the first 5 min re-teaching it with a live demo, then compress Concept 1 by 3–4 min.)*

### Concept 1 (0:15–0:25): HTTP anatomy — read a real one

**SAY (problem):** "Yesterday you clicked Send and JSON appeared. Magic is a debt — today we pay it. Let's read the actual messages."

**DO:** open the `.http` raw response pane from S1. Dissect live, labeling with the cursor:

- Request line: method, path, version — "the *what* and *where*."
- Headers — "metadata about the message. `Content-Type` tells the server how to *read* the body."
- Blank line, then body.
- Response: status line → headers → body.

**SAY (the anchor line — deliver slowly):** "Everything the client and server will ever say to each other fits in this envelope. There is no other channel. Every feature you ever ship is four choices: method, path, body shape, status codes. That set of choices has a name — the **contract**."

**ASK:** "The server wants to tell the client 'created — and here's where it lives.' Which parts of the envelope carry that?" *(status 201 + Location header)* — plant this; it pays off in live coding.

**BRIDGE — SAY:** "So which method and path do we choose — and by what rule? That's REST."

### Concept 2 (0:25–0:35): REST resources + the status-code vocabulary

**SAY:** "REST's big idea: URLs name **things** — nouns. Methods are the **verbs**. `/api/projects` is a shelf. `/api/projects/7` is one box on that shelf. And `GET /api/getProjectById?id=7` is what it looks like when nobody decided."

**DO:** build the verb table on the whiteboard *with them* — cold-call each row:

**ASK:** "GET on the shelf means…?" *(read)* "POST?" *(add a box)* "PUT on box 7?" *(replace the box)* "DELETE?" *(remove it)*

**SAY (idempotency, problem-first):** "Your mobile app sends a request. Timeout. It retries. The request actually ran *twice*. For which verbs is that safe?"

**DO:** walk the table: GET ✔, PUT ✔ (same replacement), DELETE ✔ (already gone), POST ✘ — **two boxes**.

**SAY:** "That's why POST creates and PUT replaces. It's not style — it's retry-safety. And whoever parked on quiz question 5: there's your answer." *(cold-call that person to restate it)*

**DO:** draw the status-code decision tree:

```
worked? ──yes──> body to return? ──yes──> 200
        │                        └─no──> 204
        │        created something? ───> 201 + Location
        └─no──> client's fault? ─ bad input 400 / missing 404 / conflict 409
                our fault? ─────────────> 500
```

**SAY:** "Seven codes cover this entire internship. The skill isn't memorizing them — it's *choosing consciously* every single time."

**BRIDGE — SAY:** "Last concept: a JSON body arrives. How does it become a C# object in your method's parameters — and what stops garbage from getting in?"

### Concept 3 (0:35–0:45): Model binding, validation, DI

**SAY (binding):** "You already used binding: `Get(int id)` — the framework read `{id}` from the route. Today's version: `Create(CreateProjectRequest request)` — the framework reads the JSON body, builds the record, hands it to you. Route → simple parameters. Body → one complex object."

**SAY (validation, problem-first):** "What if `name` is empty? Or 5,000 characters of emoji? Rule: **all input is hostile until validated** — and validation lives on the *server*. Client-side checks are courtesy, not security."

**DO:** show `[Required]` and `[StringLength]` on the DTO on a slide/snippet (you'll type them for real in live coding).

**SAY:** "And `[ApiController]` runs them automatically and returns a 400 with a standard error shape — Problem Details. Remember Session 1, when I said 'trust me, `[ApiController]` does things'? Faith debt, partially repaid."

**SAY (DI, one diagram):** "Our controller needs a place to keep projects. It could `new` up a list — but then every controller has its *own* list, and later its own database connection. Instead: register the thing **once** — `builder.Services.AddSingleton<...>` — and *ask* for it in the constructor. The framework hands it in. Why bother? Swap-ability. Thursday, the in-memory store becomes a database and the controller *barely changes*. That's the whole sales pitch of DI. The deep version comes in Session 5."

**BRIDGE — SAY:** "Concepts done: envelope, nouns-and-verbs, seven codes, binding, validation, DI. Now we build TT-03, 04, 05 — and every choice we make, we point at the contract."

---

## 0:45–1:20 — Live Coding: Project CRUD (TT-03/04/05)

*(Predict-before-run on EVERY request: ask the room for the status code, get a committed answer, then hit Send.)*

### Refactor first (0:45–0:50)

**DO:** extract the static list into `InMemoryProjectStore`; register `AddSingleton<InMemoryProjectStore>()`; inject via constructor.

**SAY (narrate the payoff):** "Notice what the controller knows now: *someone gives me a store*. It doesn't know or care which one. Hold that thought until Thursday."

### POST — TT-04 (0:50–1:05)

1. **DO:** write `CreateProjectRequest` with `Name` `[Required]` `[StringLength(100)]`, `Description` nullable.
2. **DO:** write the naive version ending in `return Ok(project);` — **ASK (predict):** "I send a valid POST — what code comes back?" Send it. 200.
   **SAY (challenge):** "It works. But open `api-contract.md` — contract says **201 + Location**. Why would a client care about the difference?" *(so it can fetch/poll the new resource without guessing the id)*
3. **DO:** replace with `CreatedAtAction(nameof(GetById), new { id = project.Id }, response);` — send, then **point at the `Location` header in the raw pane**.
   **SAY:** "There it is. The server just told the client where the new thing lives. This one line is the session." *(THE MONEY SHOT — do not rush, do not skip the naive step.)*
4. **DO:** send `{"name": ""}` — **ASK (predict):** "Code?" *(400)* Read the entire Problem Details body aloud, field by field.
   **SAY:** "Machine-readable. Field-level. Standard shape. You will never invent a custom error JSON in this course."
   **ASK (the trick):** "Point at the line in *our* code where that validation ran." *(nowhere — the framework ran it before our method)*

### Scripted deliberate error (1:05–1:12)

**DO:** in `GetById`, write route `[HttpGet("{projectId}")]` but keep parameter `int id`. Send `GET /api/projects/7`.

**SAY:** "404. But project 7 exists — I just created it. Debug time." Set a breakpoint, show `id = 0`. **ASK:** "Where did my 7 go?"

**AI practice (session theme — critique a contract):**
**DO:** paste the route attribute + method signature into the AI. **SAY:** "I'm not asking it to fix my code — I'm asking *what's inconsistent between these two lines*." Read the answer, **verify against the route-template docs page**, fix (`{id}`), retest.
**SAY:** "That's the workflow: the AI critiques, the docs verify, *you* decide."

### PUT + DELETE — TT-05, fast (1:12–1:18)

**DO:** implement PUT → `204` on success, `400`/`404` on failure. **ASK (predict)** before each send.
**SAY:** "Why 204 and not 200 with the body? We *replaced* it — the client already knows what it sent."
**DO:** DELETE → `204`; missing id → `404`.

**Idempotency live rerun — DO:** send the same PUT twice *(same state, same 204)*; same POST twice *(two projects!)*.
**SAY:** "There's the table from the concept block, running."

### Payoff pain (1:18–1:20)

**DO:** restart the API. GET the list — empty.
**SAY:** "Second time you've watched everything vanish. Thursday we make it stop. That's the entire agenda: databases." *(One sentence. No lecture. Break.)*

---

## 1:20–1:30 — Break

Use it: check on any trainee who looked lost during predicts. Quietly warm-call one shy trainee: "In the wrap-up I'll ask you why PUT returns 204 — get ready."

---

## 1:30–2:25 — Guided Pairs

**DO:** put this checklist on screen and leave it there:

> Implement TT-03/04/05 **exactly per `api-contract.md`**:
> - [ ] POST: validation, `201` + Location
> - [ ] GET by id: `200` / `404`
> - [ ] PUT: `204` / `400` / `404`
> - [ ] DELETE: `204` / `404`
> - [ ] All requests in your `.http` file
> - [ ] Every wrong-input case demonstrated (make it fail on purpose)

**Track setup (2 min):**
- **Foundation:** checkout `s2-foundation` — skeletons given, fill the bodies; hint sheet maps each AC to the helper (`CreatedAtAction`, `NotFound()`, `NoContent()`).
- **Core:** own S1 repo, no scaffold.
- **Stretch:** duplicate-name check returning `409` + written 3-sentence justification of why `409`, not `400`. Confirmed stretch also do their first **peer review**: one Core pair's work against the contract — point at the line, ask a question, **never type**.

**Rotation (rules in the methodology file: timer not hands, never touch keyboards, 2/10-minute triage). Rotation questions — use verbatim:**

- "Show me your 404 path — now *make it happen*."
- "Why 204 and not 200 here?"
- "Point at the line where validation runs." *(trick — the framework, before their code)*
- "Send your PUT twice. What changed the second time?" *(nothing — that's the point)*

**Timeline sanity check at 2:00:** every pair should have POST + GET working. Any pair without a working POST → pair them with a finished pair for the last 20 minutes.

---

## 2:25–2:45 — Independent Checkpoint (solo, no pairs, no AI)

**DO:** display the three tasks:

1. Add `[StringLength(500)]` to `Description` — prove it with a failing request (screenshot the 400).
2. Screenshot a full create→read sequence: POST `201` with Location visible → GET on that Location → `200`.
3. Written, 3–5 sentences: "A client sends POST with an empty name. Trace what happens and why the client sees what it sees."

**Pass bar:** correct codes AND the trace mentions validation happening *before* their method body. A trace that says "my code checks the name" = direction confusion → office-hours list.

**DO during checkpoint:** walk the room silently, note who finishes in 10 min (track-up candidates) and who hasn't started task 2 by 2:35 (track-support candidates). Feed both into the checkpoint-#1 track decisions.

---

## 2:45–3:00 — Wrap: Contract Freeze + Sprint 1 Review

### Contract-freeze ceremony (3 min — make it feel like an event)

**DO:** display `api-contract.md` full screen.

**SAY:** "As of this moment, this document is **frozen**. Changing it requires a team discussion — exactly like production, where a contract change breaks real clients. From now on, your reviews cite this file, not opinions. 'The contract says 204' ends the argument."

### Cold-calls (4 min)

- "Which verbs are idempotent, and why isn't POST?" *(ask your warm-called trainee the PUT/204 question here)*
- "When 201 vs 200 vs 204?"
- "What did `[ApiController]` do for us today?"

### Sprint 1 review framing (4 min)

**SAY:** "Sprint 1 committed TT-01 through TT-05. Board check —" **DO:** move the cards live. **SAY:** "Homework closes the sprint: finish Project CRUD and open a **pull request** referencing the story IDs. That PR is repo checkpoint #1 — the first evidence gate."

### Exit ticket + homework (3 min)

Standard 4 exit-ticket questions. Homework: complete CRUD, PR opened, and **one deliberately failing request documented in the PR description**.

**SAY (closing line):** "Show me your API refusing bad input. A feature is also what it *rejects*."

---

## Post-Session (within 48h)

- [ ] Tag `session-2-live`; push.
- [ ] Review PRs as checkpoint #1; track confirmations/moves per plan_v2 §8.
- [ ] Exit tickets → S3 opener; update known-issues sheet (`[FromBody]` confusion, PUT 200-vs-204, route typos + anything new today).
- [ ] Send S3 pre-work (SQL + EF Core) 48h ahead — it references the frozen contract.
