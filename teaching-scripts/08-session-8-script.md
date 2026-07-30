# Session 8 Teaching Script - Hardening, Documentation, Demo, and Next Steps

**Status: DRAFT — finalize 24h before delivery after reading Session 7 exit tickets.**
**Sprint 4 close — stories TT-14, TT-15. Demo day: ~100 minutes of the 180 belong to the trainees.**
**Session outcome:** Every repo passes the release checklist it can pass; every trainee delivers a four-minute demo (architecture, one request, one failure, one test, one lesson) and leaves with a personal continuation path.

**⚠ This session's structure is different:** short concept block, short hardening sprint, then demos dominate. Timekeeping is the instructor's *primary* job today — a visible countdown timer per demo, no exceptions, including for the strong ones.

---

## Before the Session (Instructor Prep)

- [ ] Demo schedule posted 48h ago; every trainee confirmed their slot; backup order for no-shows.
- [ ] Release checklist (blueprint §10) as a shared checklist doc, one row per trainee.
- [ ] Rubric sheets ready (plan.md §9) — score demos live, don't reconstruct from memory.
- [ ] The three continuation paths (plan.md §11) formatted as a one-page handout.
- [ ] A clean machine (or fresh VM/container) ready for the README-test theater in the live segment.
- [ ] Timer visible to all; a 1-minute-warning sound agreed.

## 0:00-0:12 — Standup: Final Quiz + Logistics

1. 401 vs 403 vs our foreign-owner 404 — decode all three. *(unknown identity / known + refused / refused without confirming existence)*
2. Where may the owner id come from, and where never? *(token claims / request body)*
3. Name two of the five burn patterns from Session 7. *(secrets in repo, over-posting, leaky logs, injection, missing authz)*
4. What makes a test suite trustworthy? *(it can fail; deterministic; covers negatives)*
5. The whole course in one line: trace a request from client to database and back. *(60 seconds, cold-call your strongest Foundation trainee — set them up to win in front of everyone)*

Logistics (2 min): demo order, timer rules, "rubric scoring is live; interviews this week are the second half of your grade — sign-up sheet is posted."

## 0:12-0:35 — Concept Block: What "Ready to Ship" Means

### Concept 1: Environments and configuration (Problem → Solution, 8 min)

**Problem:** "Your connection string points at `tasktracker.db` on *your* laptop. The company's server isn't your laptop. Hardcode a path per machine?"

**Solution — the configuration ladder, live in the repo:** `appsettings.json` (safe defaults, committed) → `appsettings.Development.json` (local overrides) → **user-secrets** (local secrets, *never* committed — demo `dotnet user-secrets set`) → **environment variables** (how real servers inject config; show one override live). "The code never changes between environments — only the configuration around it. That single sentence is what 'twelve-factor' means, and it's why S7's committed password was a five-alarm bug."

**Health checks callback:** "TT-01, Session 1, minute one — `GET /api/health`. Today it completes its destiny: load balancers and orchestrators call it to decide if your process gets traffic. Your first endpoint was production infrastructure all along."

### Concept 2: Documentation that tells the truth (7 min)

- **OpenAPI:** "Your controllers already generate a spec — but generated docs tell the truth only if the annotations do." Show one endpoint before/after `ProducesResponseType` metadata: suddenly the spec admits it can 404. "The spec is the contract, machine-readable. Client teams generate *their* code from it — lies here become their bugs."
- **The README law:** "Written for a stranger with nothing but the SDK. Five commands, clone-to-running. We test this today — *literally*."
- **Deployment (the map, honestly):** "The checklist you'll run is called *release readiness* — being deployable. Actual deployment is optional today (provider accounts, credits — see the risk table), but the map from Session 1 completes: our monolith would go to a PaaS as-is; the moment it needed per-request scaling and had no local state, a serverless split becomes *possible*. You now know what those words cost. That's the difference between today-you and Session-1-you."

### Concept 3: Definition of done, for a course (3 min)

> "The board doesn't lie today: what's Done is Done, what isn't goes back to Backlog *honestly* — shipping a true 80% beats claiming a false 100%, in this room and in every job you'll have. Your certificate reflects evidence, and evidence is what you're about to demo."

## 0:35-1:05 — Hardening Sprint (guided, all tracks in parallel)

Everyone runs the **release checklist** (blueprint §10) against their own repo, in order, checking rows off in the shared doc:

1. Clean-clone test — clone into a *new folder*, follow your own README verbatim, note every place you had to improvise → fix the README.
2. `dotnet build --warnaserror` + `dotnet test` — both green.
3. `.http` regression pass — every contract request returns its documented code.
4. Secrets sweep — `git log -p **/appsettings*` shows nothing hot; user-secrets in place.
5. Migrations-from-zero — delete DB file, `dotnet ef database update`, seed, smoke test.
6. OpenAPI spot-check — 3 endpoints admit their real status codes.
7. ProblemDetails audit — force one of each failure box; no stack traces anywhere.

**Instructor theater (5 min, mid-sprint):** pick one volunteer repo, clone it on the clean machine, follow the README **exactly, narrating every stumble deadpan**. Nothing teaches README empathy like watching a stranger obey your instructions literally.

- **Foundation:** checklist scoped to their slice (their endpoint, their test, their README). Full rows, smaller surface.
- **Stretch:** + CI badge green in the README; deploy to the approved target *if* pre-verified, else a written deploy plan (platform, config injection, migration step, health check URL).

## 1:05-1:15 — Break (demo tech-check: first three presenters test screen share now)

## 1:15-2:55 — Demo Day (~20 × 5 minutes: 4 demo + 1 transition)

**The format (posted, rehearsed via pre-work):**

| Minute | Segment | They show |
|---|---|---|
| 0-1 | Architecture | The diagram: request → controller → service/DbContext → SQLite → response. *Their* words, 60 seconds |
| 1-2 | One request | A working contract request end-to-end (most choose create → 201 + Location) |
| 2-3 | One failure | Their API *refusing* something, and why that refusal is a feature (validation, transition rule, or ownership) |
| 3-4 | One test | `dotnet test` green on screen + one sentence on what their favorite test proves |
| 4 | One lesson | "The thing I'll do differently in my next project is —" |

**Instructor protocol:** score the rubric live during each demo; one genuine specific compliment + at most one question per trainee ("Why 204 there?" — the question *is* part of the assessment; note the answer for the interview). Timer is law — cutting off a strong trainee at 4:00 politely is a gift to the nervous one presenting ninth. Between-demo transitions are where you reclaim drift; if running >8 min behind by demo 10, convert the final review segment to async written feedback.

**Failure grace, stated before demo #1:** "If your live request breaks, you debug it out loud for up to sixty seconds — and narrated debugging under pressure scores *better* than a smooth demo, because it's the realer skill." *(This defuses the fear and is true — reward it on the rubric's explanation row.)*

## 2:55-3:00 — Close: Next Steps and Honest Goodbyes

- **The arc, one last time:** "Eight sessions ago: an empty folder and the sentence 'a process on a port.' Today: twenty tested, documented, database-backed APIs and — more valuable — twenty people who can *explain* them. The map from Session 1 is yours now; everything on it is learnable the same way you learned this: one vertical slice at a time."
- **Continuation paths handout** (plan.md §11): "Three paths — foundation, job-ready, advanced. Your interview this week ends with me marking *your* recommended entry point on this page. That page is the real certificate."
- **Logistics:** interview slots (Foundation first), certificate criteria restated (evidence-based, three outcomes — no surprises), feedback form, and where the cohort channel lives after today.
- Last words: "Never ship code you can't explain. Never trust a confident machine — or a confident human — over a green test. Go build things."

## Post-Session (the internship isn't over for you)

- [ ] Complete rubric scoring same-day while demos are fresh; reconcile with checkpoint history.
- [ ] Run the 5-7 min explanation interviews across the week (Foundation → Core → Stretch); the interview validates or overrides demo impressions — *ownership of code is the thing being tested*.
- [ ] Certificate decisions per plan.md §9 (70/100 floor, no zero in HTTP/data/validation/explanation); draft the three lists, sleep on borderline cases once.
- [ ] Per-trainee continuation-path notes sent within one week (while motivation is hot).
- [ ] Instructor retro in `scratchpad/` → fold conclusions into plan_v2 for the next cohort: what each sprint actually cost, which scripts drifted from reality, which pre-work packs underperformed their exit tickets.
- [ ] Send Netpoints the completion report: outcomes per certificate tier, cohort evidence summary, and your recommendation for a follow-on program (the roster's Core middle is the natural audience).
