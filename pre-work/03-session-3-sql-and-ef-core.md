# Before Session 3: Relational Databases, SQL, and EF Core

**Required time:** 45 minutes  
**Submit:** At least 12 hours before Session 3  
**Important:** SQL concepts are required. EF Core terminology is preparation, not a request to build the database early.

## Why You Are Studying This

EF Core does not remove the need to understand databases. A backend developer must know what tables, keys, constraints, joins, and transactions mean before asking an ORM to generate SQL.

Session 3 opens **Sprint 2 — "It remembers"** with story **TT-06**: your projects must survive a service restart (create → restart the process → the project is still there). That is what EF Core, SQLite, and your first migration deliver. In the session you will draw the schema by hand *before* the ORM generates it — this pre-work is that drawing hand warming up.

## Learning Outcomes

You should be able to:

- Model Projects and Tasks as relational tables.
- Explain primary and foreign keys.
- Write simple `SELECT`, `INSERT`, and `JOIN` statements.
- Explain the roles of `DbContext`, entity, migration, and database.

## Part 1: Database Notes - 10 Minutes

- **Table:** a structured collection of rows.
- **Primary key:** uniquely identifies a row.
- **Foreign key:** references a row in another table.
- **Constraint:** a database rule, such as required, unique, or valid relationship.
- **Index:** an additional structure that can speed reads but adds storage/write cost.
- **Transaction:** a set of changes that should succeed or fail together.
- **One-to-many:** one Project can have many Tasks; each Task belongs to one Project.

The database, not only C# code, should protect important data rules.

## Part 2: SQL Exercise - 15 Minutes

Given:

```sql
CREATE TABLE Projects
(
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT NULL
);

CREATE TABLE Tasks
(
    Id INTEGER PRIMARY KEY,
    ProjectId INTEGER NOT NULL,
    Title TEXT NOT NULL,
    Status TEXT NOT NULL,
    FOREIGN KEY (ProjectId) REFERENCES Projects(Id)
);
```

Write SQL for:

1. Insert one Project.
2. Insert one Task belonging to that Project.
3. Select every Project.
4. Select only Tasks with status `Done`.
5. Join Tasks to Projects and return task title plus project name.

Then answer:

- What invalid data does `NOT NULL` prevent?
- What invalid data does the foreign key prevent?
- Should Project names be unique in this project? Explain your decision.
- What should happen to a Project's Tasks when the Project is deleted — block the delete, or delete them too? Name one risk of each choice.

## Part 3: EF Core Study - 15 Minutes

Read:

1. EF Core overview:
   https://learn.microsoft.com/en-us/ef/core/
2. EF Core migrations overview:
   https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/

Learn these terms:

- **Entity:** a C# object mapped to persisted data.
- **DbContext:** coordinates database access and tracked changes.
- **DbSet:** entry point for querying and changing one entity type.
- **Migration:** a reviewed description of a schema change.
- **Provider:** EF Core integration for a database such as SQLite or SQL Server.

Team discipline you will follow in the session: after `dotnet ef migrations add <Name>`, the generated migration file is **opened and read before** `dotnet ef database update` is ever run. A migration is code you review, not magic you trust.

Do not run migrations against an important database during pre-work.

## Part 4: Schema Artifact - 5 Minutes

Draw two boxes named `Projects` and `Tasks`. Include columns, primary keys, the foreign key, required/optional fields, and the relationship direction.

Paper, Excalidraw, draw.io, or another simple tool is acceptable.

## Check Yourself

1. Can a Task exist without a Project in the proposed schema?
2. What is the difference between a C# validation rule and a database constraint?
3. Why must a generated migration be reviewed?
4. What can an ORM hide from a developer?
5. When would a transaction be important?

## Submit

- Your five SQL statements.
- The schema diagram.
- Answers to the three design questions.
- One database rule you want enforced and where you would enforce it.

## Foundation Support

Use Microsoft's introductory Transact-SQL learning path for additional practice:

https://learn.microsoft.com/en-us/training/paths/get-started-querying-with-transact-sql/

Complete only the introduction and basic SELECT material.

## Stretch

Add `CreatedAtUtc` and `DueDate` to the schema. Decide their data type and nullability. Add one useful index and explain which query it helps. If you argued Project names should be unique, sketch how a unique index would enforce it and what HTTP status a duplicate-name create should return — this is the Session 3 stretch feature.

## Blocked?

Send your attempted SQL and the exact concept causing difficulty. A design can be wrong and still be useful for discussion; submit your attempt.

