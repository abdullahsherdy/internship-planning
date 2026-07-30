# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **documentation-only workspace** — no application code, builds, or tests. It contains the curriculum for a Netpoints .NET backend internship: 8 online sessions x 3 hours (24 hours total), for a cohort of 20 trainees. The cohort is organized into three tracks — Stretch (2–4), Core (8–10), Foundation (6–8) — assigned per `plan_v2.md` §2 from the interview roster and confirmed by a baseline diagnostic (the older "3 advanced / 6 intermediate / 6 basic / 5 beginners" split in `plan.md` was corrected by plan_v2; use the track model).

The teaching stack described by the curriculum is .NET 10 LTS, C#, ASP.NET Core Web API (controllers), EF Core, SQLite (SQL Server optional), xUnit, Git/GitHub. The cumulative project is a **Task Tracker REST API** (Project + TaskItem entities only — deliberately small).

## Authoritative Documents (read in this order)

1. **`plan.md`** — the base delivery plan. Contains the graduation floor (11 required capabilities), teaching principles, project scope, the eight-session syllabus, the AI-usage curriculum, assessment rubric, and risks.
2. **`plan_v2.md`** — the roster-grounded revision that layers on top of `plan.md` (session format, syllabus, AI curriculum, rubric unchanged unless stated there). It defines the three-track model with named provisional assignments (§2), the per-track deliverable matrix (§5), the **frozen API contract** (§6 — the single source of truth for endpoints, status codes, error shape, pagination envelope), and ADRs recording the key decisions (§7). Where plan.md and plan_v2.md disagree, plan_v2 wins.
3. **`project-blueprint.md`** — the buildable technical spec of the Task Tracker: code-complete domain/DbContext/controller patterns, sprint backlog with user stories (TT-xx IDs), DB design, engineering standards, and the Agile delivery frame (4 sprints, instructor as Product Owner). The instructor reference repo is constructed from this document.
4. **`PLAN_EVALUATION.md`** — the audit of the original plan: what was kept, the 10 critical issues found, and the original→revised change table. Read this to understand *why* the plan is shaped the way it is — future planning should stay consistent with its conclusions.
5. **`MILESTONES.md`** — the big-picture milestone map: per-session project/trainee/instructor milestones, the three assessment gates, and the concept-debt ledger. Check it when writing or revising session material.
6. **`plan-v1.md`** — the preserved original plan. Historical reference only; superseded. Do not extend it.
7. **`prompt.txt`** — the original instructor request that produced this work.
8. **`pre-work/`** — send-ready trainee packs, one per session plus `00-pre-work-gate.md` (environment/baseline gate), indexed in `pre-work/README.md`.
9. **`teaching-scripts/`** — minute-by-minute instructor delivery scripts for all eight sessions (01 is final; 02–08 are drafts finalized 24h pre-session); the mandatory script template is at the end of `teaching-scripts/01-session-1-script.md`.
10. **`scripts/`** — session slide decks (currently `session-1-slides.md`).
11. **`Trainees info/Trainees_interview_analysis.md`** — trainee interview profiles that drive the track assignments.

## Central Outcome (the design constraint for everything)

Every graduating trainee independently builds and explains a database-backed ASP.NET Core endpoint with validation, correct HTTP behavior, DTO mapping, async EF Core access, a test, Git evidence, and verified AI assistance.

When editing or extending any document, changes must serve this outcome — not topic coverage. The evaluation explicitly rejected "cover many .NET topics" in favor of "prove a small set of backend capabilities."

## Key Curriculum Decisions (do not silently reverse these)

These were deliberate corrections from the audit (`PLAN_EVALUATION.md`) and the roster analysis (`plan_v2.md`); preserve them in any revision:

- **Scope is capped**: Project + TaskItem only. No Users, Assignments, roles, or many-to-many until the core API is complete.
- **No premature patterns**: no generic repository, Unit of Work wrappers, AutoMapper, MediatR, or CQRS in the core path. Direct EF Core + explicit DTO projection + one focused service. Patterns are stretch/comparison work only.
- **SQL before EF Core**: raw SQL and relational modeling are taught in Session 3 before the ORM hides them.
- **Auth is not on the graduation floor**: Session 7 uses a supplied auth starter; implementing auth independently is stretch work.
- **Testing lands in Session 6** (not late), with both unit and integration tests.
- **AI verification workflow in every session**: Explain → Plan → Generate → Verify → Reflect. Generated code is only acceptable when the trainee can explain, run, test, and revise it.
- **Certificate honesty**: three outcomes (Completed / Completed with distinction / Participated), evidence-based rubric with 70/100 floor — never "job-ready" claims for 24 hours.
- **The API contract is frozen** (`plan_v2.md` §6): all tracks build against the same contract; differentiation is depth on one codebase (three depths), never divergent APIs. Reviews check against the contract, not taste.
- **Track movement stays open both directions** all internship; demonstrated ability (baseline diagnostic, submissions) beats interview self-report.
- **Stretch trainees are reviewers, not co-instructors**: they point at the line and ask a question — never type on someone else's machine.

## Pre-Work Pack Structure (mandatory template)

Every file in `pre-work/` follows this exact 9-section structure — keep it when editing or adding packs:

1. Why you are studying this
2. Learning outcomes
3. Selected study material
4. Required exercise
5. Check yourself
6. Submit
7. Foundation support
8. Stretch
9. Blocked?

Constraints: required work is 30–45 minutes, one resource per concept, one small artifact. Packs are sent 48 hours before a session; submissions due 12 hours before. Do not pad packs with extra optional resources.

## Editing Conventions

- All content is Markdown intended to be sent directly to trainees or converted to the company's document format — write for that audience (clear, imperative, no internal jargon).
- Placeholders (repository paths, ports, channel names) exist intentionally in packs; the instructor replaces them before sending (see "Instructor Review Before Sending" in `pre-work/README.md`).
- If you change the syllabus in `plan.md`/`plan_v2.md`, propagate the change to the matching pre-work pack, teaching script, and `pre-work/README.md` schedule table, and vice versa. Changes to the API contract or entities must also be reflected in `project-blueprint.md` (and story IDs TT-xx kept consistent).
- `README.md` at the root is the workspace index — update it if documents are added or renamed.
- Open questions for the client are tracked in `plan.md` §13 ("Decisions to Confirm With Netpoints"); add new client-facing decisions there rather than embedding assumptions in packs.
