# Pre-Work Gate: Setup and Baseline

## 1. Why This Matters

Session 1 must be used for backend learning, not downloading SDKs or creating accounts. This gate verifies that every trainee can build, run, request, and commit before live training.

The internship runs three tracks — Foundation, Core, and Stretch — on the **same project and the same API contract**, differing in depth, not in kind. The baseline diagnostic below places you provisionally; moving between tracks later is normal in both directions and is based on what you demonstrate, not what you self-report.

## 2. Outcomes

You can:

- Run the .NET CLI and identify the installed SDK.
- Clone, build, and run a small repository.
- Send an HTTP request to a local API.
- Create a Git commit.
- Show your C#, HTTP, SQL, and Git baseline.

## 3. Timebox

- Required: 60 minutes setup, plus the 45-minute baseline diagnostic (sent separately by the instructor).
- Foundation support: up to 60 additional minutes.
- Complete at least 24 hours before Session 1.

## 4. Must Do

### Install or verify

- Instructor-selected .NET 10 SDK.
- Visual Studio with ASP.NET and web development workload, or approved editor.
- Git and GitHub account.
- Instructor-approved API client: `.http` files, Postman, or Bruno.
- Database tool only if specified.

### Run checks

```powershell
dotnet --info
git --version
```

Clone the starter repository, then:

```powershell
dotnet restore
dotnet build
dotnet run --project src/TaskTracker.Api
```

Send:

```http
GET {{baseUrl}}/api/health
Accept: application/json
```

Create a branch, make the small change specified by the instructor, commit, and push.

### Self-assessment: no AI

Mark each topic `Know`, `Unsure`, or `Do not know`:

1. Variable, method, class, interface, exception.
2. `List<T>` and simple `Where`/`Select`.
3. Purpose of `async` and `await`.
4. HTTP GET versus POST.
5. `200`, `201`, `400`, `404`, and `500`.
6. Table, row, primary key, and foreign key.
7. Clone, branch, commit, push, and pull request.
8. One backend responsibility.

### Baseline diagnostic: 45 minutes, no AI, sent separately

The instructor will send a timed diagnostic with three parts:

1. **Read C# and predict output** (15 min) — no writing code, just reading it.
2. **Fix one small bug** in a prepared repository (15 min).
3. **Trace a request in writing** (15 min) — describe what happens between a client sending `GET /api/health` and receiving a response.

This is not graded pass/fail. It places you in a provisional track (Foundation, Core, or Stretch) so support and stretch work fit your actual level. Attempting it honestly without AI is what makes the placement useful to you.

## 5. Check Yourself

Answer without notes:

1. What command proves that the project compiles?
2. What evidence shows the API is running?
3. What is the difference between SDK and runtime?
4. Why should a secret not be committed?
5. If the API returns `404`, what two broad causes would you investigate?

## 6. Submit Before Session

- Installed SDK version from `dotnet --info`.
- Response from `/api/health`.
- Link to pushed branch/commit.
- Self-assessment.
- Completed baseline diagnostic (follow the submission instructions sent with it).
- Operating system and editor.

Do not include tokens, passwords, connection strings, or secrets.

## 7. Foundation Support

Attend the setup clinic if a command fails. Send the command, full error, OS, `dotnet --info`, and what you already tried.

## 8. Stretch

Explain the differences between:

- Build time and runtime.
- Source and compiled output.
- Process and port.
- HTTP client and server.

## 9. Blocked?

Post in the setup-help channel before the deadline. Environment blockers reported during Session 1 move to the recovery workflow so live training can continue.

