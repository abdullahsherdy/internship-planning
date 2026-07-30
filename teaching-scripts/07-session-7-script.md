# Session 7 Teaching Script - Security, Authentication, and AI-Assisted Engineering

**Status: DRAFT — finalize 24h before delivery after reading Session 6 exit tickets.**
**Sprint 4 kickoff ("It ships") — story TT-13. Tracks diverge more than any other session — run the split deliberately.**
**Session outcome:** Core+ trainees enforce one ownership rule with the auth starter and prove it with a test; Foundation trainees find and fix real security issues in their own API; *everyone* rejects at least one AI suggestion with evidence.

---

## Before the Session (Instructor Prep)

- [ ] Tags `session-7-start` / `session-7-done`; **auth starter branch verified on a clean machine this week** (login endpoint issuing JWTs, two seeded users, `[Authorize]` wired — sanitized per plan.md §10).
- [ ] Threat-model worksheet for Foundation printed/posted (below, §Pairs).
- [ ] Three **planted vulnerabilities** in a `s7-audit` branch for the live demo: connection string with fake password committed in `appsettings.json`, an over-posting-vulnerable endpoint accepting the entity type, a log line dumping the full request body.
- [ ] An AI-generated "secure auth" snippet prepared that contains at least one real flaw (e.g., JWT with `none` alg accepted, or password comparison via `==`) for the rejection exercise.
- [ ] Known-issues: token not sent (`Authorization: Bearer` header syntax), 401 vs 403 confusion, clock skew on token expiry.

## 0:00-0:15 — Standup: Quiz + Sprint 4 Kickoff

1. What does a green integration test prove that clicking the `.http` file doesn't? *(repeatable, complete, permanent verification of the wiring)*
2. The debugging method, three steps. *(reproduce, locate, fix+lock)*
3. Why did bug B (swallowed exception) survive the test suite? *(the negative case wasn't tested — suites only see what you ask)*
4. From pre-work: authentication vs authorization, one sentence each. *(who you are / what you may do)*
5. From pre-work: why do we store password *hashes*, never passwords? *(breach of the DB must not yield credentials; hashing is one-way)*

**Sprint 4 kickoff:** "Last sprint: 'It ships.' TT-13 today — ownership. TT-14/15 Thursday — docs and release. Today has a second agenda: this is the AI deep-dive session. You've used the verify workflow six times; today we weaponize it — you'll perform a security review *with* AI and catch it being confidently wrong at least once. That catch is today's checkpoint."

## 0:15-0:45 — Concept Block: Who Are You, and What May You Do?

### Concept 1: Authentication vs authorization (Problem → Solution, 10 min)

**Problem framing:** "Right now, anyone on the network can `DELETE /api/projects/1`. Yours, mine, anyone's. Two separate questions are unanswered: *who is asking?* and *are they allowed?*"

- **Authentication** — "proving identity. Password checked once at login; carrying the proof afterward is the token's job. A **JWT** is a signed note from the server to itself: 'I checked; this is user 42; here are their claims; signed, me.' Show a decoded JWT on screen (jwt.io with a starter token): header/payload/signature. **The payload is readable by anyone** — Base64 is not encryption; the signature only proves it wasn't *altered*. Never put secrets in claims."
- **Authorization** — "what the identity may do. Two flavors: role ('admins can') and **ownership** ('you can edit *your* projects') — ownership is today's build, and it's the flavor juniors get wrong most, because it must be checked *per resource, in the query*, not per endpoint."
- 401 vs 403, once and forever: "401 = I don't know you (or your proof expired). 403 = I know exactly who you are, and no."

### Concept 2: The five ways juniors get burned (12 min — the planted-vulns demo)

Open `s7-audit` and *hunt live*, problem-first — "three real bugs are in this branch; find them with me":

1. **Secrets in the repo** — the connection string with a password in `appsettings.json`, *in Git history forever*. "Rotation is the only cure once pushed. Prevention: user-secrets locally, environment/vault in prod — S8 shows the wiring."
2. **Over-posting** — the endpoint binding the *entity*: send `{"name":"x","id":999}` or an unexpected `isAdmin`-style field. "The DTO-only rule you've followed since Session 1 was never style — it's an allow-list at the boundary. Today it becomes a security control you can name."
3. **Leaky logs** — the full-body log line. "Logs outlive databases and get shipped to third parties. Log *events and ids*, never payloads with personal data." (S5's rule, now with teeth.)
4. **Injection** — "why haven't we worried about SQL injection? Because EF Core parameterizes everything. Show the query log: values arrive as parameters, not string-glued SQL. The rule survives EF: **never concatenate user input into a query** — the one place EF lets you (`FromSqlRaw` with interpolation misused), don't."
5. **Broken authorization** — "the #1 API vulnerability in the wild (OWASP API Top 10): the check that isn't there. Which is why TT-13 exists."

### Concept 3: AI-assisted engineering — the deep dive (8 min)

> "Six sessions of Explain→Plan→Generate→Verify→Reflect. Here's the *why* behind the ritual, in three facts. One: AI optimizes for *plausible*, not *true* — it will name packages that don't exist and APIs from three versions ago, in perfect grammar. Two: AI security advice is trained on the average of the internet, and the average of the internet is insecure. Three: AI is genuinely excellent at *volume* — edge cases, review questions, explanations — which is exactly the work that's expensive for you. Conclusion: AI proposes, evidence disposes. `dotnet build`, `dotnet test`, the query log, and official docs are evidence. Confidence — yours or its — is not."

**The verification checklist for today's review** (post it): Does it compile? Do tests stay green? Does the claimed API exist in the official docs *for our version*? Does it violate the contract, the DoD, or any rule from Concept 2? Can I explain every line?

**Transition:** "Tracks split for the build. Core+: ownership. Foundation: you're auditing your own API with the worksheet — and your work is not the junior version; finding real holes is the security job."

## 0:45-1:20 — Live Coding: The Auth Starter + One Ownership Rule (TT-13)

*(Core-track demo; Foundation follows along conceptually — their build block differs.)*

1. **Tour the starter, don't build it** (10 min): login endpoint → issues JWT; `AddAuthentication().AddJwtBearer(...)` in Program.cs; `[Authorize]` attribute. "You are *users* of this component today, implementers later if you take the stretch. Being able to *integrate* auth correctly is the graduation skill; implementing it is a specialization." Login as seeded user A in the `.http` file, copy the token, call a protected endpoint with and without the header — `200` vs `401` live.
2. **Add ownership** (15 min): migration adds `OwnerId` to `Project` ("read it aloud — S3 ritual holds") → `POST` stamps the owner from the token's claims (`User.FindFirstValue(ClaimTypes.NameIdentifier)`) — "**never from the request body** — that's over-posting inviting itself back" → mutations filter by owner:
   ```csharp
   var project = await db.Projects
       .FirstOrDefaultAsync(p => p.Id == id && p.OwnerId == userId, ct);
   if (project is null) return NotFound();   // deliberate: 404, not 403
   ```
   **⚠ The designed debate (this session's scripted "error"):** "I just returned `404` for *someone else's* project — not `403`. Anyone object?" Let them argue. Resolution: "403 confirms the resource exists — an information leak. 404 tells strangers nothing. Both are defensible in industry; *choosing consciously* is the skill. Contract says 403 — so now we either change the code or change the contract, and the contract is frozen, which means a **team decision**, which we now have, live." *(Update contract to 404-for-foreign with a dated note — they witness a real contract-change process.)*
3. **Prove it with a test:** integration test — user A creates, user B's token attempts `DELETE` → asserted `404`, then A's token → `204`. "Ownership without a test is a promise; with a test it's a property."
4. **AI practice — the centerpiece rejection:** paste the prepared flawed AI auth snippet. Run the verification checklist against it *out loud* until the flaw surfaces. "Write down what evidence killed it — that sentence is your checkpoint today."

## 1:20-1:30 — Break

## 1:30-2:25 — Guided Build (tracks diverge — separate breakout streams)

**Core + Stretch stream:** integrate the starter into *their* repo → ownership on Project mutations per the (amended) contract → the two-user integration test → AI security review of their own repo using the checklist, minimum one accepted finding fixed and one rejected finding documented.

**Foundation stream (threat-model worksheet — equally rigorous, differently scoped):**

| Question | They check | Fix expected |
|---|---|---|
| What's in my Git history? | `git log -p appsettings.json` | move any secret-ish config to user-secrets; document rotation need |
| Can a request write fields I didn't offer? | POST with extra/unexpected JSON fields to every endpoint | confirm DTO allow-listing; tighten any entity binding |
| What do my logs say about a request? | trigger each failure path, read the console | remove any payload/PII logging |
| What does my API tell an attacker? | read every error response body | no stack traces, no internal paths, ProblemDetails only |
| Where would auth go? | write (not build) a 5-line plan: which endpoints, 401 vs 403 where | reviewed by a stretch trainee |

**Stretch extra:** implement login→JWT issuance themselves against the starter's shape, or policy-based authorization (`[Authorize(Policy = "ProjectOwner")]` with a requirement handler). Yousef: compare with Express middleware auth in the mapping sheet — final version.

Rotation questions: "Show me where the owner id comes from — and where it must never come from." / "401 or 403 here, and why?" / "Which AI finding did you reject, and what killed it?"

## 2:25-2:45 — Independent Checkpoint

**One deliverable, all tracks:** the **AI review record** — (1) one AI suggestion you *accepted*, with the evidence that verified it; (2) one you *rejected*, with the evidence that killed it; (3) 2-3 sentences: how would you use AI at a job where the codebase is confidential? *(expected: no pasting proprietary code into public tools — the rule from plan.md §7, recalled unprompted)*

Pass = the rejection is real and the evidence is evidence (build/test/docs/behavior), not vibes.

## 2:45-3:00 — Wrap

Board: TT-13 → Done (Core+) / threat-model artifacts logged (Foundation). Cold-calls: authn vs authz; 401 vs 403 vs our 404 decision *and why the contract change needed a team decision*; the two-source rule for owner id; one planted vuln and its fix.

Homework: complete the AI review record's highest-value verified fix in their repo + (Core) ownership test green in CI. Exit ticket. Announce: "Thursday: release. README a stranger can follow, OpenAPI that tells the truth, the checklist, and your four-minute demo. Rehearse it once at home — four minutes is shorter than you think. Demo order posts tomorrow."

## Post-Session

- [ ] Tag `session-7-live`; push.
- [ ] Post the S8 demo schedule (20 × 5 min, per plan.md — order by track: Foundation early-middle, never first; a strong Core trainee opens).
- [ ] Release checklist + demo template sent with the S8 pre-work.
- [ ] Schedule the individual explanation interviews (5-7 min each) — Foundation first, per plan_v2 §8.
