# Before Session 2: HTTP, REST, and API Contracts

**Required time:** 40 minutes  
**Submit:** At least 12 hours before Session 2

## Why You Are Studying This

ASP.NET Core gives us syntax for endpoints, but the behavior belongs to HTTP. Understanding requests, responses, methods, and status codes is more important than memorizing controller attributes.

In Session 2 the team's API contract is **frozen** as `api-contract.md` in the instructor repository: every endpoint's method, path, success code, and failure codes become an agreement, not a suggestion. All tracks build against it, and reviews cite it. Session 2 delivers the rest of Sprint 1: **TT-03** (get project by id → `200` or `404`), **TT-04** (create project → `201` + `Location`, or `400` with field errors), and **TT-05** (update and delete → `204` or `404`). Your contract exercise below is your first draft of that agreement — in the session you will compare it against the frozen version.

## Learning Outcomes

You should be able to:

- Identify the method, path, query, headers, and body in a request.
- Select a reasonable HTTP method and status code.
- Explain the difference between route data, query data, and JSON body data.
- Describe an API contract before implementing it, and explain why a team freezes one.

## Part 1: Study - 20 Minutes

Read these pages:

1. MDN, Overview of HTTP:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview
2. MDN, HTTP request methods:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
3. MDN, HTTP response status codes:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

Focus on:


- `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- Safe versus idempotent methods.
- `200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`, and `500`.

Do not memorize every status code.

## Part 2: Read This Example - 5 Minutes

```http
POST https://localhost:7001/api/projects
Content-Type: application/json
Accept: application/json

{
  "name": "Internship API",
  "description": "Task tracker project"
}
```

Identify:

- Method: `POST`
- Path: `/api/projects`
- Request header: `Content-Type`
- Request body: the JSON object
- Expected successful response: `201 Created`
- Expected invalid-input response: `400 Bad Request`

One more shape to recognize: when ASP.NET Core rejects invalid input, the `400` body follows a standard error format called **Problem Details** — it includes a `title`, a `status`, and an `errors` object naming each invalid field. You will use this shape all internship; for now, just recognize that failures have a standard body, not an invented one.

## Part 3: Contract Exercise - 10 Minutes

Write the method, route, successful status, and one failure status for:

1. List all projects.
2. Find project number 12.
3. Create a project.
4. Replace project number 12.
5. Change only the status of task number 8.
6. Delete project number 12.

Then answer:

- Should `GET /api/projects` change database data?
- If the same `DELETE` is sent twice, what should the second response communicate?
- Why should a POST response identify the created resource?

## Part 4: Send Three Requests - 5 Minutes

Use the API from Session 1 and save three requests in an `.http` file:

```http
@baseUrl = https://localhost:7001

GET {{baseUrl}}/api/health

###

GET {{baseUrl}}/api/projects

###

GET {{baseUrl}}/api/projects/999
```

Adjust the port to match your application.

## Submit

- Your six endpoint contract answers.
- The `.http` file.
- The status returned by each request.
- One question about an HTTP behavior you found unclear.

## Foundation Support

Use this sentence format for every endpoint:

> When the client wants to [goal], it sends [method] to [path]. A successful server returns [status]. If [failure], it returns [status].

## Stretch

Explain why these are weak API routes and suggest improvements:

- `POST /api/createProject`
- `GET /api/getAllTasks`
- `POST /api/deleteTask?id=5`

## Blocked?

Send the request text, exact response status/body, API console output, and URL. Do not hide the response body.
