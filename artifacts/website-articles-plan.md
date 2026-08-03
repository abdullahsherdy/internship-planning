# Plan: Articles + Interactive Playground on abdullahsherdy.tech

**Status:** Approved plan, ready to execute
**Target repo:** abdullahsherdy.tech (plain React, hosted on Vercel free plan)
**Author intent:** Publish .NET/C# teaching content (starting with the Netpoints Session 4 reference) as branded articles with creative UI, animations, strong UX, and an in-browser code editor where readers can run the examples.

**How to use this file:** copy it into the website repo root (or `artifacts/`), open Claude Code in that repo, and say "execute the articles plan" — everything needed is specified below.

---

## 1. Goals

1. New **Articles** section: Markdown-driven tutorials with syntax highlighting, tags, reading time, and per-article SEO.
2. **Interactive playground**: readers edit and run C# code examples in the browser.
3. **Design upgrade**: modern typography, motion, dark mode, polished reading experience.
4. **Zero hosting cost**: everything static/client-side — fits Vercel free plan. No backend, no CMS, no database.
5. **Personal branding**: every article carries the byline header and CTA footer already used in the internship packs.

Non-goals (v1): comments, newsletter backend, search server, CMS, auth.

## 2. Architecture Decisions

| Decision | Choice | Why |
|---|---|---|
| Content storage | Markdown files in the repo (`src/content/articles/*.md`) | Same format as existing packs; git is the CMS; free |
| Markdown rendering | `react-markdown` + `remark-gfm` + `remark-frontmatter` | Pure client-side, tables + fenced code support |
| Syntax highlighting | `highlight.js` via `rehype-highlight` (C#, SQL, bash, JSON) | Lightweight, no build plugin needed in plain React |
| Routing | `react-router-dom` v7 (add if not present) | `/articles`, `/articles/:slug` |
| Animations | `framer-motion` | Page transitions, scroll-reveal, micro-interactions |
| Code editor | **Monaco Editor** (`@monaco-editor/react`), lazy-loaded | The VS Code editor; familiar to devs; lazy load keeps initial bundle small |
| Code execution | **Piston public API** (`https://emkc.org/api/v2/piston/execute`) — free, no API key, supports C#/.NET | Only realistic zero-cost way to *run* C# from a static site |
| Execution fallback | If Piston is down: show output placeholder + "copy code" button | Graceful degradation |
| Frontmatter parsing | Tiny hand-rolled parser (or `gray-matter` if bundler supports Buffer polyfill — prefer hand-rolled, ~30 lines) | Avoid Node polyfill issues in Vite/CRA |
| Article loading | `import.meta.glob('/src/content/articles/*.md', { as: 'raw' })` (Vite) or `require.context` (CRA) — detect at build start | Bundles articles at build time, no fetch needed |

**Note on execution:** running C# fully in-browser (WASM) needs a ~30–60 MB runtime download — bad UX. Piston is an external free service (documented external data flow: user-typed code is sent to emkc.org for compilation). State this in a small tooltip near the Run button ("runs via Piston, an open-source execution engine").

## 3. File Manifest (what to create in the website repo)

```
src/
├── content/
│   └── articles/
│       └── efcore-linq-csharp-foundations.md     # Session 4 reference, adapted (first article)
├── lib/
│   ├── articles.js        # loads all .md files, parses frontmatter, exports sorted article list
│   ├── frontmatter.js     # minimal ---key: value--- block parser
│   └── readingTime.js     # words/200 → "18 min read"
├── components/
│   ├── articles/
│   │   ├── ArticleCard.jsx        # cover card: title, tags, date, reading time, hover motion
│   │   ├── ArticleList.jsx        # responsive grid + tag filter chips
│   │   ├── ArticleView.jsx        # renders one article (react-markdown + custom renderers)
│   │   ├── CodeBlock.jsx          # replaces <pre>: highlight + "Copy" + "Try it ▶" button
│   │   ├── TagChip.jsx
│   │   ├── TableOfContents.jsx    # sticky sidebar from h2/h3, scroll-spy highlight
│   │   └── AuthorFooter.jsx       # the CTA footer (site/YouTube/LinkedIn) — single source
│   ├── playground/
│   │   ├── Playground.jsx         # Monaco (lazy) + Run button + output pane + status
│   │   ├── PlaygroundModal.jsx    # full-screen overlay opened from "Try it ▶"
│   │   └── runCode.js             # POST to Piston; language map; timeout + error handling
│   └── shared/
│       ├── PageTransition.jsx     # framer-motion route transition wrapper
│       └── Seo.jsx                # sets document.title + meta description per page
├── pages/
│   ├── ArticlesPage.jsx           # /articles
│   └── ArticlePage.jsx            # /articles/:slug
└── styles/
    └── article.css                # reading typography (max-width 72ch, print-friendly)
```

Plus edits to existing files:

- `App.jsx` (or router file): add `/articles` and `/articles/:slug` routes with lazy imports.
- Navbar component: add "Articles" link.
- Home page: add a "Latest articles" strip (top 3 `ArticleCard`s) for discovery.
- `vercel.json`: add SPA rewrite so deep links work: `{ "rewrites": [{ "source": "/(.*)", "destination": "/" }] }` (skip if already present).

## 4. Content Model

Frontmatter schema at the top of every article:

```markdown
---
title: "C#, LINQ, and EF Core Foundations — the Complete Reference"
slug: "efcore-linq-csharp-foundations"
date: "2026-08-03"
tags: ["csharp", "efcore", "linq", "dotnet"]
description: "Delegates to lambdas to LINQ to EF Core loading strategies — everything behind a database-backed ASP.NET Core endpoint."
cover: ""            # optional image path
draft: false
---
```

Rules:
- `slug` = filename without extension; must match.
- `draft: true` articles are excluded from production builds.
- The byline header from the packs is **not** written per file — `ArticleView` renders author info from one config object (`src/lib/author.js`) so branding updates happen in one place.

Code fences opt into the playground with a language + `run` hint: ` ```csharp run ` → `CodeBlock` shows "Try it ▶"; plain ` ```csharp ` shows only Copy. (Snippets that can't run standalone — entity classes, controller fragments — stay non-runnable; only self-contained `Main`-able examples get `run`.)

## 5. Playground Design

- **Entry points:** "Try it ▶" on runnable code blocks (opens `PlaygroundModal` pre-filled) and a standalone `/playground` route (stretch, phase 4).
- **Editor:** Monaco, `csharp` language, dark theme matching site, `React.lazy` + Suspense so it never affects article load.
- **Run flow:** Run button → `runCode.js` POSTs `{ language: "csharp", version: "*", files: [{ content }] }` to Piston → show compile errors (stderr) or stdout in output pane; 15 s timeout; disable button while running; keyboard shortcut Ctrl+Enter.
- **UX details:** first-run notice "Code executes on Piston (open-source, public). Don't paste secrets."; retry button on network failure; output pane monospace with preserved whitespace.
- **Wrap trick:** article snippets that are expression-only get auto-wrapped in a `Main` template before sending, so `Console.WriteLine(...)` examples run as-is.

## 6. UI / UX / Animation Direction

- **Typography:** article body max-width ~72ch, 17–18 px, generous line height; distinct heading scale; `Inter`/`Segoe UI` text + `Cascadia Code`/`JetBrains Mono` for code.
- **Motion (framer-motion):** fade+slide page transitions; article cards lift on hover with spring; headings/sections reveal on scroll (`whileInView`, once); TOC scroll-spy with animated indicator; subtle progress bar at top of article showing read progress.
- **Dark mode:** respect `prefers-color-scheme` + manual toggle persisted to `localStorage` (skip if site already has one).
- **Mobile:** TOC collapses to a floating button; playground modal becomes full-screen; tables scroll horizontally.
- **Accessibility:** honor `prefers-reduced-motion`; focus states on all interactive elements; semantic headings.

## 7. SEO / Marketing

- `Seo.jsx` sets title `"{article.title} — Abdullah Sherdy"`, meta description, canonical URL, OpenGraph + Twitter card tags per article.
- JSON-LD `Article` structured data (author = you, links to LinkedIn/YouTube).
- Auto-generate `sitemap.xml` at build (small node script in `scripts/generate-sitemap.mjs`, run in the Vercel build command).
- Every article ends with `AuthorFooter` (the CTA block: website/YouTube/LinkedIn) and starts with the byline.

## 8. Dependencies to add

```bash
npm i react-router-dom react-markdown remark-gfm rehype-highlight framer-motion @monaco-editor/react
```

(`highlight.js` comes via `rehype-highlight`; verify none are already installed before adding.)

## 9. Build Phases (execute in order; each phase ships independently)

**Phase 1 — Content pipeline + reading experience** *(the core, do first)*
1. Detect bundler (Vite vs CRA) → pick glob-import strategy.
2. `frontmatter.js`, `articles.js`, `readingTime.js`, `author.js`.
3. Routes + `ArticlesPage` + `ArticlePage` + `ArticleView` + `CodeBlock` (highlight + copy only).
4. Port the Session 4 reference as the first article (adapt: remove internship-internal references like TT-xx/session numbers, keep all technical content; add frontmatter).
5. `vercel.json` rewrite. **Acceptance:** article renders beautifully at `/articles/efcore-linq-csharp-foundations`, deep link works on Vercel preview.

**Phase 2 — Design + motion**
6. `article.css` typography pass, dark mode, `PageTransition`, card hover, scroll reveals, reading progress bar, `TableOfContents`.
7. Navbar link + home-page "Latest articles" strip. **Acceptance:** Lighthouse ≥ 90 performance/accessibility on the article page.

**Phase 3 — Playground**
8. `runCode.js` + `Playground.jsx` + `PlaygroundModal.jsx`, lazy Monaco, `run`-hint wiring in `CodeBlock`, Main-wrap template, Piston notice.
9. Mark the runnable snippets in the first article with `run`. **Acceptance:** a reader edits the delegates example, hits Run, sees output; Piston-down case degrades gracefully.

**Phase 4 — SEO + stretch**
10. `Seo.jsx`, JSON-LD, sitemap script, OG tags.
11. Stretch: standalone `/playground` route; tag filter page; RSS feed (`scripts/generate-rss.mjs`).

**Quality gates per phase:** `npm run build` succeeds; no console errors; mobile viewport checked; test in browser before calling done.

## 10. Content Roadmap (after launch)

1. **Launch article:** the Session 4 reference (C#/LINQ/EF Core foundations) — largest, highest-value.
2. Split follow-ups from existing material: "The N+1 problem, measured", "Eager vs Lazy vs Explicit loading", "Why your LINQ runs in memory (IEnumerable vs IQueryable)", "async/await in ASP.NET Core without the myths" — each ~8 min read, cross-linked, all sourced from packs you already wrote.
3. Cross-post summaries to LinkedIn with a link back; mention the site in YouTube descriptions.

---

## Kickoff checklist (what you do)

1. Copy this file into the website repo (root or `artifacts/`).
2. Open Claude Code in that repo directory, run `/init` so it learns the codebase.
3. Say: **"Execute the articles plan in artifacts/… — start with Phase 1."**
4. Have the repo's git remote + Vercel auto-deploy already connected (push = publish); we work on a branch and you review the Vercel preview before merging.
