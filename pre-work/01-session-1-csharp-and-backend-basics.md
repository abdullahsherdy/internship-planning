# Before Session 1: C# and Backend Basics

> **Abdullah Sherdy** — .NET Backend Instructor
> [abdullahsherdy.tech](https://abdullahsherdy.tech) · [YouTube](https://youtube.com/@abdullah.sherdy) · [LinkedIn](https://linkedin.com/in/abdullah-sherdy)

**Required time:** 45 minutes  
**Submit:** At least 12 hours before Session 1  
**AI rule:** Do the required exercise without AI. You may use AI only after submitting your first attempt.

## Why You Are Studying This

Session 1 starts by building an ASP.NET Core endpoint. You do not need to master C# first, but you must recognize the basic pieces of a C# program and understand what happens when a client sends a request to a backend.

The internship runs like a real product delivery: the instructor is the Product Owner, you are the team, and the eight sessions are four sprints. Session 1 opens **Sprint 1 — "It responds"**, which commits two user stories: **TT-01** (check the service is alive via `GET /api/health`) and **TT-02** (list projects via `GET /api/projects`). You will see stories, a board, and pull requests that reference story IDs — exactly like a company team. No Agile study is needed now; you learn it by being inside it.

## Learning Outcomes

After this preparation, you should be able to:

- Distinguish source code, build output, runtime, process, and port.
- Read a simple C# class and method.
- Use variables, conditions, loops, methods, and `List<T>`.
- Describe a backend request and response in simple words.

## Part 1: Study - 20 Minutes

Read or watch only enough to answer the questions below.

### Required resource

Microsoft Learn, "Write your first code using C#":

https://learn.microsoft.com/en-us/training/paths/get-started-c-sharp-part-1/

Complete these modules only:

1. Write your first C# code.
2. Store and retrieve data using literal and variable values.

### Read these notes

- **Source code:** the C# text written by a developer.
- **Build:** compilation that checks code and produces runnable output.
- **Runtime:** the environment that executes the built program.
- **Process:** one running instance of an application.
- **Port:** a number used to reach a network application on a machine.
- **Endpoint:** a method and URL exposed by an API, such as `GET /api/projects`.
- **Request:** data sent by a client to a server.
- **Response:** status, headers, and optional body returned by the server.

## Part 2: Required Exercise - 15 Minutes

Create a console application:

```powershell
dotnet new console -n BackendPrep
cd BackendPrep
dotnet run
```

Replace the generated code with a program that:

1. Creates a `List<string>` containing three project names.
2. Prints every project using a loop.
3. Defines a method named `FindProject`.
4. Returns the matching project or `null`.
5. Prints `"Project not found"` when there is no match.

Your solution does not need to be perfect. It must build and run.

Run:

```powershell
dotnet build
dotnet run
```

## Part 3: Check Yourself - 10 Minutes

Answer without reopening the resource:

1. What is the difference between building an application and running it?
2. What does `string?` communicate?
3. Why would a method return a value instead of printing it directly?
4. What is one difference between a console application and a Web API?
5. A browser sends `GET /api/projects`. Which side sends the request and which side returns the response?

## Submit

Submit:

- Your `Program.cs`.
- Output from `dotnet build`.
- Your five answers.
- One topic you want explained during Session 1.

## Foundation Support

If the exercise is difficult, complete the next Microsoft Learn module on basic string formatting, then retry:

https://learn.microsoft.com/en-us/training/paths/get-started-c-sharp-part-1/

Focus on making the program work. Do not study inheritance, delegates, events, or advanced LINQ yet.


---

*Prepared by* **Abdullah Sherdy** *— .NET Backend Instructor*

Found this useful? I publish more .NET and backend engineering content:

- **Website:** [abdullahsherdy.tech](https://abdullahsherdy.tech) — articles, projects, and contact
- **YouTube:** [@abdullah.sherdy](https://youtube.com/@abdullah.sherdy) — video walkthroughs and tutorials
- **LinkedIn:** [abdullah-sherdy](https://linkedin.com/in/abdullah-sherdy) — connect and follow my work

*Questions about this material? Reach out on any channel above.*
