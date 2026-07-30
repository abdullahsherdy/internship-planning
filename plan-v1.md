# .NET Backend Internship — Plan

**Instructor:** (original plan)
**Client:** Netpoints
**Format:** Online · 8 sessions × 3 hours = 24 hours · twice per week
**Environment (assumed):** Windows + Visual Studio 2022 Community · .NET 8 LTS · SQL Server / LocalDB · EF Core
**Cohort size:** ~22 trainees

---

## 1. Goals

**Primary goal (floor):** Broad, practical exposure to the .NET backend ecosystem so every trainee can continue learning independently after the internship ends.

**Stretch goal (ceiling):** Any trainee who completes all pre-work and homework leaves *junior-ready* — able to build, secure, and deploy an ASP.NET Core Web API on their own.

**Trainee take-home value:**
- One end-to-end project on their GitHub (portfolio piece).
- A recorded 5-minute demo of that project (for LinkedIn / job applications).
- A signed certificate of completion.
- A curated "what to learn next" roadmap.

---

## 2. Cohort snapshot

Grouped by starting level so per-session pre-work can be targeted correctly.

### Advanced (3) — stretch tasks + peer-mentor role
- **Yousef Emad** — grad 2023, working backend dev (Express.js), exploring .NET
- **Mohamed Mohamed** — grad 2025, EF Core + ADO.NET + WinForms, frontend→backend switch
- **Moaz Alaa** — last-year Computer Engineering, has built basic CRUD .NET apps

### Intermediate — hands-on basics (6)
- **Hassan Mohamed** — Engineering, .NET (personal projects, no real work)
- **Moaz Ali** — Faculty of Science, .NET (personal projects)
- **Habiba Khaled** — 3rd yr CS, ITI 1-month .NET + EF Core, NTI React/Next
- **Mohamed Galal** — 4th yr FCIS, has .NET knowledge
- **Shrouk Ragap** — FCIS Ain-Shams, currently in ITI .NET
- **Fatma Alzahraa** — grad 2026, .NET graduation project, works as Odoo dev

### Theoretical / very basic (6)
- **Abdulwahab** — 3rd yr CS, basics of .NET
- **Ahmed Al-said** — networking background, basic .NET
- **Hazem Mohamed** — 2nd yr, DSA/OOP but no .NET
- **Nada** — MUST Uni CS, basic full-stack (React + .NET + DB)
- **Aef** — CS Zagazig, faculty-level .NET
- **Mohamed Mossad** — grad 2026

### Beginners — no .NET at all (5)
- **Mazen** — Faculty of Science
- **Salama Nasser** — grad 2023 Helwan
- **Rawan Khaled** — 4th yr FCIS-AOU
- **Nour Eldien** — grad Computer Engineering
- **Hana Haitham** — status unclear, treat as beginner

**Design implication:** teach to the middle (Intermediate), give the Advanced group stretch work + mentoring duties, and use pre-session prep material to lift Beginner/Theoretical up to the middle by session start.

---

## 3. How the skill gap is handled

1. **Pre-work gate before Session 1** — C# fundamentals checklist + environment verification. Ungraded, but framed as "you will be lost without this."
2. **Per-session prep pack** — sent 48h before each session. 30–60 min of curated reading/video. Beginners must do it; intermediates skim; advanced skip.
3. **Stretch tasks in every session** — advanced trainees get a harder variant of the exercise (e.g. add pagination + filtering with expression trees instead of a plain GET).
4. **Peer-mentor pairing** — each Advanced trainee is paired with 2 Beginners. Reinforces the mentor's learning; unblocks the beginner between sessions.
5. **Office-hours channel** — a Discord/WhatsApp group for async questions between sessions. You answer once a day; peer-mentors answer the rest.

---

## 4. Final project (built incrementally across all 8 sessions)

**Project: Task Management REST API**

Small enough to finish, big enough to touch every real-world concept:
- Users, Projects, Tasks, Assignments (many-to-many)
- JWT auth, role-based authorization (Admin / Member)
- Filtering, pagination, sorting
- Swagger/OpenAPI documentation
- Deployed to a public URL by session 8

Each session ships one working slice of this project. By session 8 every trainee owns a public GitHub repo with a deployed API.

---

## 5. Syllabus — 8 sessions × 3 hours

Each session follows the same shape:
- **0:00–0:15** — recap of homework / questions from prep pack
- **0:15–1:15** — concept + live-coded demo
- **1:15–1:30** — break
- **1:30–2:30** — guided exercise (add feature X to the project)
- **2:30–3:00** — Q&A, homework brief, stretch task for advanced group

| # | Session | Core topics (in-session) | Pre-work sent to beginners |
|---|---------|---------------------------|-----------------------------|
| 1 | **Kickoff + C# & .NET landscape** | .NET ecosystem, project types, C# refresher (types, LINQ, async), first Console + first Web API | Install VS 2022, C# syntax basics, OOP recap |
| 2 | **ASP.NET Core Web API fundamentals** | HTTP/REST, controllers, routing, model binding, middleware, DI container | HTTP methods, status codes, JSON, what an API is |
| 3 | **EF Core I — Data access** | DbContext, code-first migrations, CRUD, LocalDB/SQL Server | SQL basics (SELECT/JOIN), what an ORM is |
| 4 | **EF Core II — Relationships & LINQ** | 1-to-many, many-to-many, eager/lazy loading, DTOs, AutoMapper | LINQ practice, relational modeling |
| 5 | **Architecture & clean code** | Repository + Service layers, Unit of Work, FluentValidation, global error handling | SOLID recap, layering diagrams |
| 6 | **Authentication & Authorization** | ASP.NET Identity, JWT, roles/policies, password hashing | Cookies vs tokens, what JWT is |
| 7 | **Production-readiness** | Logging (Serilog), Swagger/OpenAPI, API versioning, config/secrets, async pitfalls, unit test intro (xUnit) | Read: 12-factor app basics |
| 8 | **Deployment + Demo Day** | Publish to IIS/Azure App Service, Dockerfile walkthrough, live demo of each trainee's project, next-steps roadmap | Prep 5-min demo of their API |

### Per-session detail (homework + stretch tasks)

**Session 1 — Kickoff + C# & .NET landscape**
- Course expectations, GitHub repo setup, communication channels
- Live demo: `dotnet new console` → `dotnet new webapi` → first `/hello` endpoint
- **Homework:** initialize the Task Management repo; push "Hello World" Web API

**Session 2 — ASP.NET Core Web API fundamentals**
- Live demo: `Projects` and `Tasks` in-memory CRUD
- **Homework:** implement full in-memory CRUD for `Projects`
- **Stretch (advanced):** custom middleware for request timing

**Session 3 — EF Core I: Data access**
- Live demo: swap in-memory storage for EF Core
- **Homework:** persist `Projects` + `Tasks` to LocalDB
- **Stretch (advanced):** raw SQL escape hatch (`FromSqlInterpolated`)

**Session 4 — EF Core II: Relationships & LINQ**
- Task ↔ User assignments; the N+1 trap; DTOs vs entities
- **Homework:** add `Users`, `Assignments`; return DTOs, not entities
- **Stretch (advanced):** pagination + sorting via `IQueryable` extensions

**Session 5 — Architecture & clean code**
- Layering: Controller → Service → Repository → DbContext
- **Homework:** refactor project into layered structure
- **Stretch (advanced):** introduce MediatR + CQRS-lite for one feature

**Session 6 — Authentication & Authorization**
- Live demo: register / login / protect endpoints
- **Homework:** add auth; only owners can edit their tasks
- **Stretch (advanced):** refresh-token rotation + revocation list

**Session 7 — Production-readiness**
- Serilog, Swagger, User Secrets, xUnit intro
- **Homework:** add Swagger, Serilog, one unit test; move connection string to User Secrets
- **Stretch (advanced):** integration test with `WebApplicationFactory`

**Session 8 — Deployment + Demo Day**
- Publish flow; deploy to Azure App Service free / Somee / MonsterASP
- **Demo Day:** each trainee gives a 5-minute live demo (recorded)
- Certificate handout + "what to learn next" roadmap

---

## 6. Pre-work gate (sent before Session 1)

A single document + checklist. Deadline: 24h before Session 1.

**Environment**
- [ ] Windows 10/11
- [ ] Visual Studio 2022 Community with **ASP.NET and web development** workload
- [ ] .NET 8 SDK (`dotnet --version` prints 8.x)
- [ ] SQL Server LocalDB or Express installed
- [ ] Git installed + a GitHub account
- [ ] Postman (or VS Code REST Client)

**C# / OOP knowledge check** (self-assessed, no grade)
- Types, variables, control flow
- Classes, inheritance, interfaces, polymorphism
- Collections (`List<T>`, `Dictionary<K,V>`)
- LINQ basics (`Where`, `Select`, `FirstOrDefault`)
- `async`/`await` at a conceptual level

**Suggested resources** (free)
- Microsoft Learn "C# for beginners" playlist
- Tim Corey — C# Fundamentals (YouTube)
- freeCodeCamp — C# full course

Anyone who cannot check the environment boxes gets a 1-hour "install session" 24h before Session 1.

---

## 7. Assessment (recommended — pending company confirmation)

- **Attendance** — required for certificate
- **Weekly commit to their project repo** — proves the work, not just the watching
- **Session 8 demo** — 5-minute recorded walkthrough of their API
- **Certificate of completion** — you sign off; huge motivation for juniors

No graded exams. Portfolio > grades for this cohort.

---

## 8. Deliverables you produce (in order)

1. **plan.md** — this file (done)
2. **Pre-work gate document** — sent to all trainees before Session 1
3. **Session-1 detailed pack** — agenda, slides/notes, live-demo code, exercise, homework brief
4. Sessions 2–8 packs — one at a time, iterated based on how the cohort responds
5. **Peer-mentor briefing** — 1-page note to the 3 advanced trainees explaining their role and stretch tasks
6. **Instructor cheat-sheet per session** — timings, common questions, troubleshooting

---

## 9. Open items — need to confirm with the company

- Preferred delivery platform (Zoom / Google Meet / MS Teams)
- Session start time and days of the week
- Language of instruction (Arabic-first with English terms? English-only?)
- Whether the company wants to be present at Demo Day
- Whether they'll issue their own certificate or want yours
- Deployment target — Azure credit available? Or free-tier only?

---

## 10. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Beginners fall behind by Session 3 | Pre-work gate + peer mentors + async office hours |
| Advanced trainees disengage | Stretch tasks in every session + mentoring role gives them status |
| Environment/install issues eat Session 1 | Pre-work "install session" 24h before + a Docker-based fallback dev container |
| Attendance drops mid-course (twice-a-week is intense) | Frame the project as cumulative — missing a session = broken project = strong pressure to attend |
| A trainee can't finish the deployment in Session 8 | Provide a shared free-tier deployment recipe; pair with a mentor during the session |
