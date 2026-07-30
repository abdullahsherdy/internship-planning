# Session 2 Delivery Methodology — How to Run the Room

Companion to `02-session-2-detailed-runbook.md` (the minute-by-minute script) and `02-session-2-script.md` (the canonical draft). This file is about *mechanics*: organizing the session, moving between stages, running practice, and checking understanding.

---

## 1. The Operating Rhythm (fixes "how do I move between stages")

Every segment follows the same 4-beat loop. Once internalized, transitions stop being awkward because the loop *creates* them:

| Beat | What you do | Example (validation) |
|------|-------------|----------------------|
| 1. **Problem** | Show pain, never announce a topic | "Send this request — name is 5,000 emoji. It saved. Is that okay?" |
| 2. **Solution** | Minimum concept that kills the pain. 5–8 min talking, max | `[Required]`, `[StringLength]`, `[ApiController]` auto-400 |
| 3. **Prove it** | Run it live. In an HTTP session the proof is always the **raw response pane** | Send invalid body, read the Problem Details aloud |
| 4. **Bridge question** | End with a question whose answer *is* the next topic | "So who hands the controller its store? That's DI." |

**Rule: never say "now we'll learn X."** Say "here's a problem — watch it hurt," then let the concept arrive as the rescue.

**Rule: the bridge question IS the transition.** The runbook has every bridge written verbatim. Read them aloud word-for-word. You never have to "move on"; the room moves itself.

### Timing discipline

- Put the block timestamps on a sticky note next to your monitor.
- If a concept block overruns by 5+ minutes, **cut from live coding** (PUT/DELETE compresses to 5 min), **never from guided pairs**. Pairs time is where learning actually happens.
- If live coding overruns, drop the second scripted-error debug narration and just fix it — but never drop the naive-`Ok()` → `CreatedAtAction` sequence (the session's money shot).

---

## 2. How to Practice With Them (guided pairs, 1:30–2:25)

1. **Checklist on screen the whole time.** They implement against `api-contract.md`, not against memory of what you typed. This is the whole point of the contract freeze.
2. **Rotate on a timer, not on raised hands.** 5–6 minutes per pair, visit everyone once before anyone gets a second visit. Stuck trainees often don't raise hands; the ones who do are usually fine.
3. **Never touch their keyboard.** Point at the line, ask a question, walk away. If you type, you learn; they watch.
4. **Triage rule:**
   - Stuck < 2 min → let them struggle (productive).
   - Stuck 2–10 min → one hint, then come back.
   - Stuck > 10 min → pair them with a neighbor who solved it — not with you.
5. **Stretch trainees are reviewers, not co-instructors.** They point at the line and ask a question. They never type on someone else's machine.

---

## 3. How to Check Understanding

"Any questions?" measures nothing. Use these five techniques — the runbook marks where each one fires:

| # | Technique | How | Why it works |
|---|-----------|-----|--------------|
| 1 | **Predict-before-run** | Before hitting Send: "What status code will come back?" Cold-call one person, get a commitment, THEN run it | Wrong predictions are gold: "You expected 200, we got 400 — what ran before our code?" |
| 2 | **Make it fail** | Not "does your 404 work?" but "show me your 404 path — now *make it happen*" | Producing the failure proves understanding; describing it doesn't |
| 3 | **Point at the line** | "Point at the line where validation runs" (trick — it's the framework, before their code) | Locating behavior in code is a far stronger signal than defining terms |
| 4 | **Written trace** | Checkpoint Q3: 3–5 sentences tracing a request end to end | Written traces expose direction-confusion ("controller sends the request") that nodding hides |
| 5 | **Warm-call the shy** | During pairs, tell a quiet trainee: "In the wrap-up I'll ask you why PUT returns 204 — get ready" | They get a public win without ambush |

**Cold-call protocol:** name first, then question ("Sara — a POST retried twice: safe or not?"). Wait 5 full seconds. Wrong answer → "close — who can build on that?" Never answer your own cold-call.

---

## 4. Session-2-Specific Non-Negotiables

- **The money shot:** naive `Ok(project)` → challenge it → `CreatedAtAction` → Location header visible in the raw pane. Do NOT skip the naive version to save time. Wrong-then-right is worth more than three correct examples.
- **Idempotency runs twice:** once as a table in the concept block, once live (same PUT twice = same state; same POST twice = two projects). The live rerun is what sticks.
- **End on pain:** restart the API, data gone. One sentence, no lecture — it sells Session 3.
- **The contract freeze is a ceremony, not an announcement.** Display the file, say the words, make it feel like a production event.
