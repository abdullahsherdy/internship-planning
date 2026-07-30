# Before Session 8: Release Readiness and Demo Preparation

**Required time:** 45 minutes plus one timed rehearsal  
**Submit:** At least 12 hours before Session 8

## Why You Are Studying This

A backend is not finished when it works only on the developer's machine. Another developer must be able to configure, run, test, and understand it. Your demo must provide evidence of engineering decisions, not only show a successful request.

Session 8 closes Sprint 4 with **TT-14** (the API documents itself — OpenAPI plus a README that works on a clean machine) and **TT-15** (the release checklist passes). Your demo is the final sprint review: you present working software to the Product Owner and answer for the decisions behind it. Board honesty applies — any story not truly Done goes back to the Backlog, stated plainly, not hidden.

## Learning Outcomes

You should be able to:

- Run a repeatable release-readiness check.
- Write setup instructions that another developer can follow.
- Demonstrate success and failure behavior.
- Explain one design decision, one test, and one verified use of AI.

## Part 1: Release Checklist - 15 Minutes

Run:

```powershell
dotnet restore
dotnet build --no-restore
dotnet test --no-build
```

Check:

- A stranger can go from `git clone` to a running API in at most 5 commands using only the README.
- `dotnet build --warnaserror` is clean (no compiler warnings) and `dotnet test` is green.
- No secrets or local passwords are committed — including in Git history.
- Configuration values are documented.
- Migrations apply from zero: delete the database file, run `dotnet ef database update`, seed, and smoke-test.
- OpenAPI starts and reflects the real contract (spot-check three endpoints).
- Every request in your `.http` file returns the status code documented in `api-contract.md`.
- Every failure path returns Problem Details; no stack trace appears in any response body.
- Logs do not expose secrets or sensitive data.

Record every failure. Fix the highest-impact issue first.

## Part 2: README Review - 10 Minutes

Your README must include:

1. Project purpose.
2. Implemented features.
3. Technology choices.
4. Prerequisites.
5. Setup and configuration.
6. Database migration/startup.
7. Run commands.
8. Test commands.
9. API request examples.
10. Known limitations and next steps.

Ask a peer to follow the README without verbal help. Record where they become blocked.

## Part 3: Four-Minute Demo - 15 Minutes

Prepare this exact structure:

- **0:00-0:30:** problem and project scope.
- **0:30-1:10:** request path through controller, service/rule, EF Core, database.
- **1:10-2:00:** one successful API request.
- **2:00-2:40:** one validation, not-found, or authorization failure.
- **2:40-3:20:** one meaningful automated test.
- **3:20-3:50:** one design decision and tradeoff.
- **3:50-4:00:** one next improvement.

Do not spend demo time installing software, typing long commands, or reading the README.

## Part 4: AI Reflection - 5 Minutes

Prepare one example containing:

- The problem you asked AI to help with.
- The prompt or summary.
- The suggestion received.
- How you verified it.
- What you changed or rejected.
- What you learned.

## Check Yourself

1. Can a new developer run the project from your README?
2. Can you demonstrate one failure, not only a happy path?
3. Can you explain why each main project layer exists?
4. Do all tests pass from a clean command?
5. Can you identify one limitation honestly?

## Submit

- Link to final repository/branch.
- Output from restore, build, and test.
- Completed release checklist.
- Peer README feedback and your fix.
- Four-minute rehearsal recording or timing evidence.
- AI reflection.

## Foundation Support

Use pre-written `.http` requests during the demo. Keep the API and database ready before your turn. Have a local fallback even if public deployment is available.

## Stretch

Add one of:

- CI build/test status.
- Health-check endpoint.
- Deployment link.
- Structured release notes.
- Measured query improvement.

Explain why it improves delivery or operation.

## Blocked?

Report deployment problems separately from core API problems. A failed hosting provider must not prevent you from demonstrating the local API, tests, and release process.

