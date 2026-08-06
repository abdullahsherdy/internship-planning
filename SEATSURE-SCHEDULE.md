# SeatSure — Delivery Schedule (Sessions 4–8)

**Project:** SeatSure — real-time event ticketing & reservation API  
**Contact hours:** 5 sessions × 3h = 15h  
**Stack:** .NET 10 LTS, ASP.NET Core (controllers), EF Core + SQLite, JWT Bearer, SignalR, xUnit  
**Tracks:** Core (everyone must reach) · Stretch (optional, same repo, no separate scope)  
**Source of truth:** `project-blueprint-v3-seatsure.md`

---

## Instructor Prep Checklist (complete before Session 4)

- [ ] Pin concurrency-token approach: RowVersion (`byte[]`) vs manual `int Version` column — do a 15-min SQLite spike privately, not live (blueprint §10, Risk 3)
- [ ] Pin password hashing: ASP.NET Core Identity hasher vs `BCrypt.Net` — choose before Session 4 and use consistently
- [ ] Build the instructor reference repo to blueprint spec (starter branches per session depend on this)
- [ ] Create starter branch for each session (S4–S8) — mandatory; no Foundation track as a safety net this time
- [ ] Rewrite teaching scripts S4–S8 for SeatSure (current scripts are Task Tracker)
- [ ] Review pre-work packs S4–S8 for Task Tracker references and update
- [ ] Update `README.md` to reflect SeatSure as the active project

---

## Session Schedule

### Session 4 — [DATE TBD]

**Pre-work pack out:** `pre-work/04-session-4-*` — 48h before session  
**Submissions due:** 12h before session

**Core scope (everyone):**
- New repo + solution structure — simplify to fewer projects if full layering isn't justified yet; blueprint §8 note applies
- `User` + `Event` entities, EF Core + SQLite setup, first migration
- JWT auth: `POST /api/auth/register` (`201` / `400` / `409`), `POST /api/auth/login` (`200 {token, expiresAtUtc}` / `401`)
- `EventsController`: `POST /api/events` (Organizer, `201`), `GET /api/events` (paginated), `GET /api/events/{id}`
- DTO `record` types from minute one — entities never cross the controller boundary

**Stretch scope:**
- Refresh tokens
- Email-format + password-strength validation beyond defaults

**Session checkpoint:** Organizer registers, logs in, creates an event, event appears in paginated list. JWT working end-to-end.

**Key teaching moments:**
- "Why DTOs from day one?" — data boundary: entities carry EF internals (change tracking, navigation properties) that don't belong in JSON
- Three levels of access: `[Authorize]` (logged in?) · `[Authorize(Roles="Organizer")]` (what role?) · ownership check (is this yours?) — Session 5 adds the third
- Thin controllers: business logic does not go here

---

### Session 5 — [DATE TBD]

**Pre-work pack out:** `pre-work/05-session-5-*` — 48h before session  
**Submissions due:** 12h before session

**Core scope (everyone):**
- `TicketType` entity + FK to `Event`, migration
- `TicketTypesController`: `POST /api/events/{eventId}/ticket-types` (owning Organizer, `201`), `GET /api/events/{eventId}/ticket-types` (`200`)
- Ownership check pattern introduced — explicit code, not attribute-based: "is this event owned by the authenticated organizer?"
- `POST /api/events/{id}/publish` (Organizer + owner check, `200` / `404` / `403`)

**Stretch scope:**
- Multiple ticket-type tiers with `SalesStartUtc` / `SalesEndUtc` sale windows

**Session checkpoint:** Organizer can add ticket types to their own event; attempting to add to another organizer's event returns `403`.

**Key teaching moment:** Authentication vs authorization vs ownership — three different questions. `[Authorize]` says "are you logged in?"; the role says "what kind of user?"; the ownership check says "is this resource yours?" Every real-world API needs all three, and only the third requires code.

---

### Session 6 — [DATE TBD]

**Pre-work pack out:** `pre-work/06-session-6-*` — 48h before session  
**Submissions due:** 12h before session

**⚠️ Instructor pre-session task:** Confirm the concurrency-token approach is pinned and working in the reference repo before this session. Do not leave this to live discovery.

**Core scope (everyone):**
- `Reservation` entity + migration (`Status`: Pending / Confirmed / Expired / Cancelled; `HoldExpiresAtUtc`)
- `IReservationService` + implementation: concurrency-token create-hold logic (blueprint §4)
  - Read `TicketType` with `RowVersion`/`Version` → check quantity → decrement → save
  - `DbUpdateConcurrencyException` → service catches → controller returns `409` Problem Details
  - Wrap read + save in a single `SaveChanges` call inside the service — no two-round-trip pattern
- `ReservationsController`: `POST /api/ticket-types/{id}/reservations` (`201 Pending` / `409`), `POST /api/reservations/{id}/confirm` (`200`), `POST /api/reservations/{id}/cancel` (`200` / `403`)
- **Two-tab (or two-terminal) live demo of the `409` race — the load-bearing demo of the project**

**Stretch scope:**
- Partial-quantity conflict resolution messaging in the `409` body
- Idempotency key on create-hold to survive client retries

**Session checkpoint:** Two concurrent hold requests for the last ticket: one `201 Pending`, one `409` with a clear Problem Details body. Inventory never goes negative. Every trainee must be able to reproduce this demo independently.

**Key teaching moment:** Why does `IReservationService` exist? Not "service layer for the sake of it" — it's the only place where the concurrency token, the quantity check, and the save happen as one atomic unit. If this logic lived in the controller, you couldn't test it in isolation, and the concurrency guarantee would be untestable.

---

### Session 7 — [DATE TBD]

**Pre-work pack out:** `pre-work/07-session-7-*` — 48h before session  
**Submissions due:** 12h before session

**Core scope (everyone):**
- `HoldExpiryService : BackgroundService`: 30s loop, scan `Pending` reservations past `HoldExpiresAtUtc`, set `Expired`, restore `TicketType.AvailableQuantity`, broadcast, save
- **`IServiceScopeFactory` pattern** — resolve a scoped `DbContext` per scan inside the singleton background service
- `EventAvailabilityHub` at `/hubs/events`: `JoinEvent(eventId)` method, `AvailabilityChanged(ticketTypeId, availableQuantity)` broadcast to group `event-{eventId}`
- Wire `AvailabilityChanged` into: hold create, confirm, cancel, expiry
- Minimal static HTML page or Swagger + browser console to watch a live update without refreshing

**Stretch scope:**
- Push notification when a hold is 2 minutes from expiry
- Admin dashboard view showing live occupancy across events

**Session checkpoint:** Create a hold → wait 30s+ → watch the hold expire and inventory restore in the browser in real time without a page refresh.

**Key teaching moment:** `IServiceScopeFactory` — "why can't I inject `DbContext` directly into the background service?" — singleton lifetime vs scoped lifetime. EF Core's `DbContext` is scoped by design (it tracks changes for one unit of work). Injecting a scoped service into a singleton is a lifetime mismatch that causes subtle, hard-to-debug state corruption. This trips up almost everyone in real jobs.

---

### Session 8 — [DATE TBD]

**Pre-work pack out:** `pre-work/08-session-8-*` — 48h before session  
**Submissions due:** 12h before session

**Core scope (everyone):**
- Unit tests on `IReservationService`: 409-on-oversell case, successful hold case, expiry-restores-inventory case
- Integration tests (`WebApplicationFactory`): create event → add ticket type → reserve → confirm happy path; reserve more than available → `409` negative test
- ProblemDetails polish — no naked `500`s anywhere in the app
- README with setup instructions
- OpenAPI / Swagger doc (`/swagger`)
- Release checklist run-through

**Stretch scope:**
- Dockerfile + docker-compose (API only; SQLite is file-based, no external services needed)
- Simple simulated payment step before confirm
- Rate limiting on reservation creation

**Session checkpoint / Final demo:**
> Create event → Add ticket type → Race two holds (two terminals simultaneously) → One `409` → Confirm the winner → Watch a second hold expire live in the browser via SignalR

`dotnet build` + `dotnet test` green. This is the graduation bar.

**Post-session handoff:** Give trainees `project-blueprint-v3-seatsure.md` §9 (Post-Internship Roadmap) as their portfolio continuation guide.

---

## Materials Status

| Material | Status | Action needed |
|---|---|---|
| `project-blueprint-v3-seatsure.md` | ✅ Ready | Source of truth — read before every session |
| `CLAUDE.md` | ✅ Updated | SeatSure context in place |
| Teaching script S4 | ❌ Task Tracker | Full rewrite for SeatSure |
| Teaching script S5 | ❌ Task Tracker | Full rewrite for SeatSure |
| Teaching script S6 | ❌ Task Tracker | Full rewrite for SeatSure |
| Teaching script S7 | ❌ Task Tracker | Full rewrite for SeatSure |
| Teaching script S8 | ❌ Task Tracker | Full rewrite for SeatSure |
| Pre-work pack S4 | ⚠️ Review | Check for Task Tracker references |
| Pre-work pack S5 | ⚠️ Review | Check for Task Tracker references |
| Pre-work pack S6 | ⚠️ Review | Check for Task Tracker references |
| Pre-work pack S7 | ⚠️ Review | Check for Task Tracker references |
| Pre-work pack S8 | ⚠️ Review | Check for Task Tracker references |
| Starter branch S4 | ❌ Not created | Mandatory (no Foundation track fallback) |
| Starter branch S5 | ❌ Not created | Mandatory |
| Starter branch S6 | ❌ Not created | Mandatory |
| Starter branch S7 | ❌ Not created | Mandatory |
| Starter branch S8 | ❌ Not created | Mandatory |
| Instructor reference repo | ❌ Not built | Build before creating starter branches |
| Concurrency approach | ❌ Pending | Spike + pin before Session 6 |
| Password hashing choice | ❌ Pending | Pin before Session 4 |

---

## Key Dates Summary (fill in once session dates are confirmed)

| Event | Date | Notes |
|---|---|---|
| S4 pre-work out | [TBD] | 48h before S4 |
| Session 4 | [TBD] | — |
| S5 pre-work out | [TBD] | 48h before S5 |
| Session 5 | [TBD] | — |
| S6 pre-work out | [TBD] | 48h before S6 |
| Session 6 | [TBD] | **Concurrency spike must be done before this** |
| S7 pre-work out | [TBD] | 48h before S7 |
| Session 7 | [TBD] | — |
| S8 pre-work out | [TBD] | 48h before S8 |
| Session 8 | [TBD] | Final demo + handoff |
