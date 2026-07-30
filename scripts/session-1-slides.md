# Session 1 Teaching Script - Backend Mental Model, C#, and the First Endpoint

**Duration:** 3 hours | **Format:** Online, live coding + guided pairs
**Session outcome:** :
1. Every trainee runs a controller-based ASP.NET Core API.
2. hits `GET /api/health` and `GET /api/projects`.
3. sets a breakpoint.
4. explains the request/response cycle in their own words.

---

## 0:00-0:15 — Opening and Retrieval Quiz

**Say (welcome, 4 min):**

> "Over eight sessions you will build one real API — a Task Tracker — and by the end you'll be able to build and *explain* a database-backed endpoint on your own. Explain is the key word. In this internship, code you cannot explain does not count, whether a person wrote it or an AI wrote it."

**Then run the Sprint 1 kickoff (this doubles as the Agile lesson — 2 min):**

> "We are also going to work the way companies work. This internship is a product delivery: I am the Product Owner, you are the team, and these eight sessions are four two-week sprints. Here is the board —" *(share the GitHub Projects board)* "— every feature is a user story with an ID. This sprint, Sprint 1, is called 'It responds' and commits two stories today: **TT-01** — as an API consumer I can check the service is alive — and **TT-02** — as a user I can list my projects. Your homework and pull requests will reference these IDs, exactly like a real team. The quiz-and-blockers slot we just did? In a company that's called a standup. You'll learn Agile by being inside one, not from slides."

**Retrieval quiz (5 questions from pre-work, ~7 min, no notes):**

1. What is the difference between the .NET SDK and the .NET runtime? *(SDK builds, runtime runs)*
2. What does a backend server actually do when a request arrives? *(receives HTTP request, runs code, usually touches data, returns a response)*
3. In C#, what is the difference between `int` and `string`? *(value with fixed numeric range vs reference to text)*
4. What does `string?` mean with the question mark? *(the value may be null; compiler forces you to check)*
5. What command runs a .NET project from the terminal? *(`dotnet run`)*

**How to use results:** Don't grade — read the room. If <60% get Q1/Q2, slow the concept block down and cut the async mention. Say out loud: "Getting these wrong now is fine. Getting them wrong in Session 4 is not — that's what the quizzes are for."

**Blockers check (3 min):** "Who could not get `dotnet --version` working?" Assign those trainees a pair partner *now* for the guided block; do not debug environments live.

---

## 0:15-0:45 — Concept Block: The Backend Mental Model

Rule for this block: **no framework names yet.** No "controller", no "ASP.NET". Only the machine model. Every framework concept later gets hooked onto this model.

### Concept 1: What is a backend? (Problem → Solution)

**Problem framing — say:**

> "You open a food delivery app and tap 'Order'. Your phone does not know your address history, doesn't know the restaurant's menu prices, and definitely can't charge your credit card. So where does all of that live, and how does your tap reach it?"

Let them answer. Someone will say "a server." Push once: "What *is* a server, physically?"

**Solution — the model. Draw this (share screen, draw live, don't paste a finished diagram):**

```
[Client: phone/browser]
        |  1. HTTP request  (method + path + headers + body)
        v
[Server: a computer, always on]
   [Process: your running program, listening on a PORT]
        |  2. your code runs
        v
   [Database: organized, persistent data]
        |  3. data comes back
        v
        |  4. HTTP response (status code + body)
[Client renders the result]
```

**Explain each word on the diagram, one sentence each:**

- **Server** — "Just a computer that never sleeps. Nothing magical. Your laptop will be the server today."
- **Process** — "A running program. When you run your API, the OS starts a process."
- **Port** — "A numbered door on the machine. Many processes, one machine — the port says which door. Your API will listen on one specific port; you'll see the number in the terminal."
- **HTTP** — "The agreed message format between client and server. A request says *what you want*; a response says *what happened*. We go deep on this in Session 2 — today just: request in, response out."
- **Database** — "The data survives even when the process stops. Today our data will live in memory and die on restart — and you will *see* it die. That pain is the reason Session 3 exists."

**Check understanding (cold-call two people):**
- "I run two different APIs on my laptop at once. What must be different between them?" *(port)*
- "The server restarts. What's gone — the code or the data?" *(data, if it was in memory; code is on disk)*

### Concept 1b: The backend landscape — where does this code run? (5 min)

Draw the three-column map from `project-blueprint.md` §1 (monolith / microservices / serverless). Problem-first:

> "Two questions companies argue about. One: our API runs 24/7 even at 3 a.m. with zero users — we pay for idle. The serverless answer: don't own a process at all; upload a *function*, the cloud runs it per request and bills per millisecond. The cost: cold starts, and there is no 'the process' — so no in-memory anything. Two: two hundred developers deploying one program step on each other. The microservices answer: split it into many small processes. The cost: every method call becomes a network call that can fail."
>
> "We are building a **monolith** — one process, one deploy, one database — and that is not the beginner option, it's the *correct starting* option. You earn the right to split a monolith by first building a good one. Keep this map; we return to it in Session 3 and Session 8."

**Transition line:**

> "So the backend is: a process on a port, receiving HTTP, running code, using data. Now — what do we need installed to *build* that process in .NET? Let's name the pieces you installed in the pre-work."

### Concept 2: The .NET pieces (5 min, fast)

**Problem framing:** "You wrote C# in a `.cs` file. Your CPU cannot read C#. What has to happen?"

- **SDK vs runtime** — "The SDK is the factory (compiler + tools). The runtime is the engine that runs the result. You installed the SDK; it includes the runtime."
- **Compilation** — "`dotnet build` turns your C# into something the runtime executes. If the compiler complains, nothing runs — and that's a feature. The compiler is the first reviewer of your code and the cheapest bug-finder you will ever have."
- **Solution vs project** — "A project (`.csproj`) is one buildable thing — an API, a test suite. A solution (`.sln`) is a folder-of-projects that tools understand. Today: one solution, one project. Session 6 adds a test project to the same solution."
- **NuGet** — "The package manager — other people's compiled code, versioned. Same idea as npm or pip. We'll use it for real in Session 3 with EF Core."

**Transition line:**

> "Pieces named. Last thing before we build: a fast tour of the C# you'll read and write today. I'm not teaching all of C# — I'm teaching exactly what today's code needs."

### Concept 3: C# rapid tour (10 min, one evolving example)

*(Timing note: the landscape map costs 5 min — recover it here. If running behind, cut Step 5's fix-it demo to a description and drop the async sentence entirely; both are repaid later anyway.)*

Do this in a **console project, not the API** — zero framework noise. Have `dotnet new console -o CSharpTour` pre-created. One example that evolves; each evolution is a problem→solution step.

**Step 1 — types and variables. Type:**

```csharp
string name = "Task Tracker";
int taskCount = 3;
bool isDone = false;
Console.WriteLine($"{name} has {taskCount} tasks. Done: {isDone}");
```

> "C# is statically typed: every variable has a type the compiler knows. Try `taskCount = "three"` — " *(do it)* " — it won't even compile. In Python this explodes at runtime, maybe in production, maybe at 3 a.m. Here it explodes now, on my screen. That's the deal with static typing: annoy you early, save you late."

**Step 2 — problem: loose data. Say:**

> "Real projects aren't three loose variables. A 'project' in our Task Tracker has a name, a description, a creation date — those belong together. Loose variables can drift apart. What groups data and behavior?"

**Solution — a class:**

```csharp
public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string? Description { get; set; }
}
```

- "`{ get; set; }` — a property: a field with a public door."
- **Nullability, pointing at the two strings:** "`Name` is `string` — the compiler assumes it's never null, so I gave it a default. `Description` is `string?` — null is allowed, and the compiler will *force* anyone who reads it to consider that. This one question mark kills the most famous crash in programming: the null reference exception. From today: if a thing can be absent, its type says so."

**Step 3 — problem: many projects. Solution — collections:**

```csharp
var projects = new List<Project>
{
    new Project { Id = 1, Name = "Website" },
    new Project { Id = 2, Name = "Mobile App" }
};

foreach (var p in projects)
    Console.WriteLine($"{p.Id}: {p.Name}");
```

- "`List<Project>` — a growable list, and the `<Project>` means the compiler guarantees only projects go in. `var` — the compiler infers the type; it's still statically typed, just less typing."

**Step 4 — records (30 seconds, seed for later):**

```csharp
public record ProjectDto(int Id, string Name);
```

> "A record: a one-line class for carrying data. In about forty minutes you'll see me use exactly this for API responses. Park it."

**Step 5 — exceptions (show, don't dwell):**

```csharp
Project? found = projects.FirstOrDefault(p => p.Id == 99);
Console.WriteLine(found.Name);   // compiler warning! found may be null
```

Run it — `NullReferenceException`. Then fix:

```csharp
if (found is null)
{
    Console.WriteLine("Not found");
    return;
}
Console.WriteLine(found.Name);
```

> "Two lessons in one crash. First: an exception is C# saying 'I cannot continue' — unhandled, it kills the process. Second: the compiler *warned me* on that line before I ran it. It knew. Read your warnings — they are free bug reports."

**Async — one sentence only:** "You'll also see `async`/`await` in code soon. For now, one sentence: it lets the server handle other requests while waiting for slow things like databases. Real explanation arrives in Session 4 when we actually wait on a database."

**Transition line into the break-less pivot to live coding:**

> "That's every C# feature today's code needs: types, classes, properties, nullability, lists, records, one exception. Now we stop talking about backends and go run one."

---

## 0:45-1:20 — Instructor Live Coding

**Rules for yourself:** Type everything, paste nothing. Narrate *why* before *what*. When an error appears — celebrate it, don't apologize. You will make one deliberate compiler error (scripted below) for the AI exercise.

### A. Create the solution (5 min)

```bash
mkdir TaskTracker && cd TaskTracker
dotnet new sln --name TaskTracker
dotnet new webapi --use-controllers -o TaskTracker.Api
dotnet sln add TaskTracker.Api
cd TaskTracker.Api
```

> "One solution, one project — matching the diagram: this project will become the *process* on a *port*. `--use-controllers` because we want the request boundary visible in an explicit class, which is also what you'll meet in most enterprise .NET codebases."

Open in the IDE. **File tour, 30 seconds each, mapping to concepts already taught:**

- `TaskTracker.Api.csproj` — "The project file. Note `<Nullable>enable</Nullable>` — the question-mark rules from the console demo are enforced here. `<TargetFramework>net10.0</TargetFramework>` — the runtime we compile for."
- `Program.cs` — "The entry point. Line by line: `CreateBuilder` prepares the app, `AddControllers` registers controller support, `Build`, `MapControllers` connects HTTP paths to our classes, `Run` — *this* starts the process and listens on the port. Every line maps to the diagram."
- `Properties/launchSettings.json` — "Here's your port number for local dev."
- Delete the WeatherForecast sample. "We never keep code we didn't choose."

### B. Problem: is anything even alive? → `GET /api/health` (8 min)

**Problem framing:**

> "Before writing real features, I want the dumbest possible endpoint — one that just proves the process is up and reachable. Every production system has this; it's called a health check. Load balancers call it to decide if your server gets traffic."

Create `Controllers/HealthController.cs` — **type it, narrating:**

```csharp
using Microsoft.AspNetCore.Mvc;

namespace TaskTracker.Api.Controllers;

[ApiController]
[Route("api/health")]
public class HealthController : ControllerBase
{
    [HttpGet]
    public IActionResult Get()
    {
        return Ok(new { status = "healthy", timeUtc = DateTime.UtcNow });
    }
}
```

**Narration map (point at each part):**

- "`HealthController` is a *class* — same keyword as `Project` in the console demo. The framework creates it when a request arrives."
- "`[Route("api/health")]` — this attribute is the address on the door: requests whose path is `/api/health` come here."
- "`[HttpGet]` — and of those, GET requests run this method."
- "`Ok(...)` — build a response with status `200 OK`. The object becomes JSON automatically."
- "`ControllerBase` gives us helpers like `Ok`. `[ApiController]` turns on API conveniences — take it on faith today, we unpack part of it in Session 2."

```bash
dotnet run
```

> "Look at the terminal: `Now listening on: http://localhost:5xxx`. There is the port from our diagram. The process is alive."

Open the browser at `/api/health`. JSON appears.

> "You just watched the whole diagram execute: browser sent an HTTP GET to a port, the process routed it to our method, our object became JSON, status 200 came back."

### C. The `.http` file (4 min)

**Problem framing:** "The browser can only easily send GETs. We need POST, PUT, DELETE from Session 2 on — and clicking around isn't repeatable. Solution: requests as a file, in the repo, next to the code."

Create `TaskTracker.Api.http`:

```http
@baseUrl = http://localhost:5xxx

### Health check
GET {{baseUrl}}/api/health

### List projects
GET {{baseUrl}}/api/projects

### One project by id  (homework will make this work)
GET {{baseUrl}}/api/projects/1
```

Click "Send Request" on the health check. Show the raw response pane: status line, headers, body. "This raw view is what HTTP actually is — Session 2 lives in this pane."

### D. Problem: real data → `GET /api/projects` (12 min)

**Problem framing:**

> "Health proves we're alive. Now the first real Task Tracker feature: list projects. Two design questions before any code. One — where does the data live? No database until Session 3, so: a list in memory, and we'll pay for that choice on purpose. Two — what shape does the caller see? That one matters more than it looks."

Create `Models/Project.cs` — "same class from the console tour, plus a timestamp":

```csharp
namespace TaskTracker.Api.Models;

public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string? Description { get; set; }
    public DateTime CreatedAtUtc { get; set; }
}
```

Create `Controllers/ProjectsController.cs`:

```csharp
using Microsoft.AspNetCore.Mvc;
using TaskTracker.Api.Models;

namespace TaskTracker.Api.Controllers;

[ApiController]
[Route("api/projects")]
public class ProjectsController : ControllerBase
{
    private static readonly List<Project> Projects = new()
    {
        new Project { Id = 1, Name = "Website Redesign", Description = "Company site", CreatedAtUtc = DateTime.UtcNow },
        new Project { Id = 2, Name = "Mobile App", Description = null, CreatedAtUtc = DateTime.UtcNow }
    };

    [HttpGet]
    public IActionResult GetAll()
    {
        var response = Projects
            .Select(p => new ProjectResponse(p.Id, p.Name, p.Description))
            .ToList();

        return Ok(response);
    }
}

public record ProjectResponse(int Id, string Name, string? Description);
```

**Narration highlights:**

- "`static` on the list — one list shared across requests, so it survives *between* requests. But watch what happens on restart later."
- "**The record returns** — I am *not* returning `Project` directly. `ProjectResponse` is the shape the caller sees; `Project` is the shape I store. Today they're nearly identical and this feels like ceremony. In Session 3 the stored shape grows database concerns the caller must never see — and this line is why they won't. The API contract and the storage model are different things that happen to look similar today."
- "`Select` — for each project, build a response record. That's LINQ; Session 4 goes deep. Today, read it as 'transform each item'."
- "Note `Description` is `string?` all the way through — the null-ness is part of the contract, honestly declared."

**⚠ SCRIPTED DELIBERATE ERROR + AI exercise (5 min).** While typing `ProjectResponse`, "accidentally" write:

```csharp
new ProjectResponse(p.Id, p.Name)   // missing third argument
```

Build fails: `CS7036: There is no argument given that corresponds to the required parameter 'Description'...`

**Say:**

> "Compiler error — good, free bug report. Now, this session's AI practice: I'll paste *only the error and this line* into the AI assistant and ask it to explain — not fix — the error."

Do it live. Read the AI's explanation aloud. Then:

> "Here's the workflow you'll use all internship: the AI *explained*, I *verify* — the record has three parameters, I passed two, that checks out against the code in front of me. I fix it myself, and I rebuild — because a green build is evidence and an AI's confidence is not."

Fix, `dotnet run`, send the `.http` request for `/api/projects`. JSON list appears. **Note the `description: null`** in project 2 — "there's our `string?` on the wire."

### E. The payoff pain: restart (2 min)

> "One last thing. Watch closely." Stop the process. Start it. Send the request again. Same data — "because it's hard-coded. But imagine we had a POST that added project 3 —" *(if time allows, add one to the list via a debugger watch or just say it)* "— anything added at runtime would be gone. In-memory data dies with the process. Remember this feeling; it's the entire motivation for Session 3."

**Transition to break:**

> "Ten minutes. When we return, you build exactly this, in pairs, and then each of you proves it alone."

---

## 1:20-1:30 — Break

Stay on the call, camera off. Post the guided-exercise doc and the `session-1-start` starter link in chat during the break.

---

## 1:30-2:25 — Guided Implementation in Pairs

Pairs were assigned at 0:12 (blocked-setup trainees with verified ones; keep advanced trainees together, not distributed — they move fast, and beginners must type, not watch).

**Exercise (post as a checklist):**

1. Create the solution and controller API (`dotnet new sln`, `dotnet new webapi --use-controllers`, `dotnet sln add`).
2. Delete the WeatherForecast sample.
3. Implement `GET /api/health` returning your own status object — add one extra field of your choice.
4. Create the `Project` model and `GET /api/projects` returning **at least 3 projects** through a `ProjectResponse` record — at least one project with a `null` description.
5. Create an `.http` file with both requests; send both; screenshot the responses.
6. Both partners must run it on **their own machine**.

**Foundation hints (post only in the foundation group's channel):**

- Command sequence with exact flags.
- Skeleton of `HealthController` with the attribute lines given, method body blank.
- "If the build fails, read the *first* error only, bottom pane. Fix, rebuild, repeat."

**Stretch (for pairs done early — this is the session stretch goal):**

- Add `GET /api/projects?name=web` — filter the list by name substring. Hint: a method parameter `string? name` on `GetAll` is automatically read from the query string. (`Where(p => p.Name.Contains(name, StringComparison.OrdinalIgnoreCase))`.)
- Then: what happens when `name` is not supplied? Why does `string?` matter here?

**Yousef's special assignment (brief him privately before the session — see plan_v2 §2):** instead of the stretch above, he builds v1 of the **Express ↔ ASP.NET Core mapping sheet** while following along: routing (`app.get` ↔ `[HttpGet]`), middleware pipeline, DI, config. It becomes a cohort resource and he learns .NET through contrast.

**Instructor loop during this block — rotate breakout rooms every ~6 min. In each room ask one of:**

- "Point at the line where the port is decided."
- "Why does `ProjectResponse` exist when `Project` already has these properties?"
- "Make the description of one project null — what does the JSON show?"

**Common failure patterns to expect (from the known-issues sheet):** route typo (`api/Health` vs attribute mismatch is fine — routes are case-insensitive; but `[Route("health")]` without `api/` will 404 the `.http` file), forgetting `MapControllers` if someone recreated `Program.cs`, running from the solution folder instead of the project folder.

**AI rule for this block (state it before starting):** "AI is allowed for *explaining errors* only — the same workflow I demonstrated. If AI writes a line for you, you must be able to tell your partner what every token does. I will ask."

---

## 2:25-2:45 — Independent Checkpoint

**This is individual. Breakout rooms of 1, or muted main room. Post:**

> **Checkpoint (submit before you leave):**
> 1. Change `GET /api/health` to also return the string `"session-1"` in a field called `version`.
> 2. Set a breakpoint inside `GetAll` in `ProjectsController`.
> 3. Send the request from your `.http` file and hit the breakpoint.
> 4. While paused: hover `Projects`, screenshot the inspector showing the list contents.
> 5. In 3-5 written sentences: trace what happened from clicking "Send Request" to JSON appearing, using the words **port, route, method, status code**.
>
> Submit: the screenshot + the sentences + a push of your repo (or zip upload if Git isn't set up — Git becomes required by Session 2).

**Grading is pass/needs-follow-up, nothing else.** The 3-5 sentences are the real signal — they predict who needs office hours before Session 2. Anyone who writes "the controller sends the request" (direction confusion) gets a 10-minute office-hours invite.

While they work, you triage submissions live and answer *only* checkpoint-blocking questions.

---

## 2:45-3:00 — Review, Exit Ticket, Next Pre-Work

**Recap — cold-call, one question per person, using the diagram (re-share it):**

- "Where in our code did we choose the URL path?" *(the `[Route]` attribute)*
- "What runs first when a request arrives — `Program.cs` or the controller method?" *(Program.cs already ran at startup; routing then dispatches to the method)*
- "Why did we return a record instead of the model class?" *(contract vs storage shape)*
- "What happens to the project list when the process restarts, and which session fixes that?" *(gone; Session 3)*

**Exit ticket (2 min, anonymous form):**

1. One thing that clicked today.
2. One thing still fuzzy.
3. Confidence 1-5: "I could recreate the health endpoint alone."
4. Did you use AI today? For what, and did you verify it?

**Homework brief (say + post):**

> "Homework: `GET /api/projects/{id}` — one project by id, from the same in-memory list. Two behaviors: found → `200` with the project; not found → `404`. Hint: the method signature is `Get(int id)` and the route template is `[HttpGet("{id}")]` — that's model binding, which Session 2 explains properly; today you use it and notice the magic. Plus a README with the exact commands to run your project — I will test your README by following it word for word on a machine that is not yours. Pre-work pack for Session 2 lands in 48 hours: HTTP and REST — the raw-response pane we saw today becomes the whole subject."

**Close:**

> "Today you ran a process on a port and served two endpoints. Session 2 makes you fluent in the language the client and server are speaking. Same time Thursday."



