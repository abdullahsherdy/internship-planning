# CLAUDE.md — SeatSure Internship Project

This file guides Claude Code when working in this repository.

## What This Repository Is

An ASP.NET Core (.NET 10 LTS) teaching project for a backend internship: **SeatSure**, a real-time event ticketing & reservation API. Built live across Sessions 4-8 of an 8-session internship (Sessions 1-3 were a different, now-retired project — do not reference or reuse anything from that project).

The full spec is `project-blueprint-v3-seatsure.md` in this repo root — **read it before generating any code or session materials.** It is the source of truth for entities, API contract, concurrency design, and the session-by-session scope. Do not invent endpoints, status codes, or entities that aren't in that document without flagging the deviation first.

## Non-Negotiable Design Decisions (do not silently change these)

- **Controllers, not Minimal APIs.** Thin controllers, DTO records in/out, entities never cross the controller boundary.
- **SQLite** via EF Core, file-based, zero external services required to run.
- **Concurrency via optimistic concurrency token** on `TicketType` (RowVersion or manual `Version int` — pin one approach and use it consistently everywhere it applies).
- **RFC 7807 Problem Details** for every error response. No naked `500`s past Session 6.
- **Offset pagination** envelope: `{ items, page, pageSize, totalCount }`. Max pageSize 50, default 10.
- **camelCase JSON**, UTC ISO-8601 timestamps suffixed `Utc` in property names.
- **JWT auth**, roles `Organizer` / `Attendee`. Role checks via `[Authorize(Roles=...)]`; ownership checks (e.g. "is this organizer's event") are explicit code, not attribute-based.
- **`IReservationService`** is where the concurrency/hold/expiry business logic lives — never put this logic directly in a controller.
- **`HoldExpiryService : BackgroundService`** — must resolve a scoped `DbContext` per scan via `IServiceScopeFactory`, never inject `DbContext` directly into a singleton-lifetime background service.
- **SignalR hub** at `/hubs/events`, group-per-event, broadcasts `AvailabilityChanged(ticketTypeId, availableQuantity)`.

Explicitly out of scope unless a Stretch task says otherwise: generic repository/UoW, MediatR/CQRS, microservices, message queues, Redis, API versioning, Docker (Docker is Stretch/post-internship).

## Working Mode

This repo is used two ways — check which one applies before acting:

1. **Instructor prep mode**: generating teaching scripts, starter branches, per-session materials, exit tickets, the API contract doc, ADRs. Output goes in `teaching-scripts/`, `artifacts/`, or similar — mirror whatever structure already exists in the repo; don't invent a new one without checking first.
2. **Trainee build mode**: actually scaffolding/implementing the ASP.NET Core solution described in the blueprint, session by session. When in this mode, build only the scope assigned to the current session (see the blueprint's session table) — do not jump ahead and implement later sessions' features early, even if it would be "easy to just do now." The whole point is trainees build understanding incrementally.

When asked to scaffold the solution from scratch, structure it as:

```
/SeatSure.sln
/src/SeatSure.Api/           # Controllers, Program.cs, DTOs, Hubs, BackgroundServices
/src/SeatSure.Application/   # IReservationService + implementation, business logic
/src/SeatSure.Infrastructure/# DbContext, EF configurations, migrations
/tests/SeatSure.Tests/       # xUnit unit + integration tests
```

(Simplify to fewer projects if the session's scope doesn't justify the layering yet — Session 4 probably doesn't need four projects. Use judgment; the blueprint's architecture diagram shows the target end-state, not necessarily the Session-4 starting state.)

## Testing

`dotnet test` must stay green. When implementing the concurrency logic (§4 of the blueprint), always pair it with a test that proves the `409`-on-oversell behavior — that test is the evidence the whole project pivot was designed around.

## Questions to Ask Before Generating Large Chunks of Code

- Which session's scope is this for? (Don't build Session 7's SignalR hub while doing Session 4 work.)
- Core or Stretch? (Keep them clearly separated — e.g. a `// STRETCH:` comment or a separate branch, whichever the instructor prefers.)
- Is this instructor-facing (teaching script) or trainee-facing (starter code)?