# Before Session 7: API Security, Authentication, and Responsible AI

> **Abdullah Sherdy** — .NET Backend Instructor
> [abdullahsherdy.tech](https://abdullahsherdy.tech) · [YouTube](https://youtube.com/@abdullah.sherdy) · [LinkedIn](https://linkedin.com/in/abdullah-sherdy)

**Required time:** 50 minutes  
**Submit:** At least 12 hours before Session 7

## Why You Are Studying This

Security failures often happen when an application trusts a client too much. AI can increase the speed of both useful work and insecure mistakes, so every suggestion still needs threat-aware review and technical verification.

Session 7 opens Sprint 4 with story **TT-13**: only a project's owner may modify it — no token → `401`, someone else's project → `403`, your own → success. You will integrate a **supplied auth starter**; you are *not* expected to implement JWT authentication from scratch (that is stretch-only work). The transferable skill for everyone is enforcing and testing the ownership rule.

## Learning Outcomes

You should be able to:

- Distinguish authentication from authorization.
- Explain identity, claim, role, policy, and ownership.
- Identify common API trust-boundary risks.
- Use AI through small prompts, explicit constraints, and verification.

## Part 1: Authentication and Authorization - 15 Minutes

Read:

1. ASP.NET Core authentication overview:
   https://learn.microsoft.com/en-us/aspnet/core/security/authentication/
2. ASP.NET Core authorization introduction:
   https://learn.microsoft.com/en-us/aspnet/core/security/authorization/introduction?view=aspnetcore-10.0

Learn:

- **Authentication:** establishes who the caller is.
- **Authorization:** decides whether that caller may perform an action.
- **Claim:** a statement about an identity.
- **Role:** a broad named category, such as Admin.
- **Policy:** a rule composed from requirements.
- **Ownership:** authorization based on the requested resource.

Answer:

1. Can a caller be authenticated but forbidden?
2. Why is hiding a button in a frontend not authorization?
3. Who must verify that a task belongs to the current user?

## Part 2: Threat Review - 15 Minutes

Review the Task Tracker and identify one example of each:

- Client sends an ID belonging to another user.
- Client sends a field it should not control.
- Secret is committed to the repository.
- Sensitive data is written to logs.
- Input is trusted without validation.
- An endpoint returns more fields than required.

For each risk, write:

- Attack or mistake.
- Impact.
- Server-side control.
- Evidence that would verify the control.

## Part 3: AI Engineering Workflow - 15 Minutes

Read GitHub's responsible-use guidance:

https://docs.github.com/en/copilot/responsible-use

Use this workflow:

1. **Explain:** define the problem yourself.
2. **Plan:** ask for options and tradeoffs.
3. **Generate:** request one small change.
4. **Verify:** build, test, run, inspect, and check official docs.
5. **Reflect:** record accepted, changed, and rejected suggestions.

Improve this weak prompt:

```text
Add JWT and make my API secure.
```

Your improved prompt must include:

- Current project context.
- One specific change.
- Security constraints.
- Files or scope allowed to change.
- Expected status codes.
- Tests required.
- Request for assumptions and risks.

Do not ask AI to implement the whole authentication system.

## Part 4: Verify an AI Answer - 5 Minutes

Ask an approved AI tool:

> List five security checks for an ASP.NET Core endpoint that updates a task.

For every suggestion mark:

- `Valid and relevant`
- `Valid but not relevant`
- `Needs verification`
- `Incorrect`

Provide one sentence of evidence. Official documentation, existing code, a test, or runtime behavior counts as evidence. The AI's explanation does not.

## Check Yourself

1. What is the difference between `401` and `403`?
2. Why must resource ownership be checked after identifying the resource?
3. Why should password hashing not be implemented manually?
4. What information must never be pasted into a public AI tool?
5. What evidence is stronger than a confident AI answer?

## Submit

- Three authentication/authorization answers.
- Six-row threat review.
- Improved AI prompt.
- Classified AI security suggestions with evidence.
- One AI suggestion you rejected.

## Foundation Support

Use this request review:

1. Who is calling?
2. Are they authenticated?
3. What action are they requesting?
4. Are they authorized for this resource?
5. Is the input valid?
6. What data may the response expose?
7. What should be logged?

## Stretch

Design an ownership policy for updating a Task. Explain where the current user ID comes from, where the Task owner comes from, and the expected `401`, `403`, and `404` behavior.

## Blocked?

Security questions should include the endpoint, caller, resource, requested action, and expected rule. Never post a real token, password, connection string, or secret.

---

*Prepared by* **Abdullah Sherdy** *— .NET Backend Instructor*

Found this useful? I publish more .NET and backend engineering content:

- **Website:** [abdullahsherdy.tech](https://abdullahsherdy.tech) — articles, projects, and contact
- **YouTube:** [@abdullah.sherdy](https://youtube.com/@abdullah.sherdy) — video walkthroughs and tutorials
- **LinkedIn:** [abdullah-sherdy](https://linkedin.com/in/abdullah-sherdy) — connect and follow my work

*Questions about this material? Reach out on any channel above.*
