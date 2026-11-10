# SQLForge - learn SQL in your browser (Phase 1 shell)

Static site for GitHub Pages. SQL runs in-browser via sql.js (SQLite, pinned 1.10.3).

## Repo tree
```
sqlforge/
├─ index.html          app shell (editor, results, schema explorer, progress, theme)
├─ data/company.sql    dataset (seeded by deterministic arithmetic, no RNG)
├─ lessons/manifest.json   list of lesson files
├─ lessons/*.json      one file per lesson
└─ README.md
```
## Lesson schema (JSON)
id, module, title, order, level (beginner|intermediate|advanced), estimatedMinutes, prerequisites[ids], engines[], dataset (file in /data),
theory (markdown subset), examples[{title,sql}], exercises[{id, level, task, starter, hint1, hint2, solution, explain[], compare{ordered, columnNames, floatTolerance}}].

## Add a lesson
1. Create `lessons/mNN-lNN-name.json` following the schema. 2. Add its filename to `lessons/manifest.json`. 3. Reload.

## Run locally
`python3 -m http.server 8000` then open http://localhost:8000 (fetch needs http, not file://).

## Deploy
Push to GitHub, then Settings > Pages > Deploy from branch > `main` / root.
