# AI MarketLens — Web Dashboard (HTML/CSS/JS)

## Launch Instructions

### Option 1 — Python HTTP Server (recommended)
```bash
cd web_dashboard
python -m http.server 8080
```
Then open: http://localhost:8080

### Option 2 — VS Code Live Server
Install the "Live Server" extension, right-click `index.html`, and select "Open with Live Server".

### Option 3 — Node.js `serve`
```bash
npx serve web_dashboard
```

> **Important:** The dashboard loads JSON data files via `fetch()` and requires a local server.
> Opening `index.html` directly via `file://` protocol will fail with a CORS error.

---

## Structure

```
web_dashboard/
├── index.html           ← Single-page dashboard (all sections)
├── css/
│   └── style.css        ← Dark theme styling
├── js/
│   ├── charts.js        ← Chart.js chart builders
│   └── app.js           ← Data loading + chart wiring
└── data/
    ├── kpis.json         ← Top-level KPI values
    ├── salary.json       ← Salary by dimension
    ├── countries.json    ← Country sample + market data
    ├── skills.json       ← Skill frequency + category + level
    ├── roles.json        ← Role distribution + cities + industry
    ├── remote.json       ← Remote work breakdowns
    └── trends.json       ← Year-over-year market trends
```

---

## Dependencies

| Library | Source | Purpose |
|---|---|---|
| Chart.js 4.4.0 | CDN (jsdelivr.net) | All charts |
| (none other) | — | No framework dependencies |

Internet connection required on first load to fetch Chart.js from CDN.
For offline use, download Chart.js and update the `<script>` tag in `index.html`.

---

## Regenerating JSON Data

If the processed datasets are updated, regenerate JSON files from project root:
```bash
python generate_dashboard_data.py
```

---

## Dashboard Sections

1. **Key Metrics** — 12 KPI cards
2. **Global Job Market** — Postings by year and role
3. **Salary Intelligence** — Salary by experience, country, role, industry, remote type
4. **Skills Intelligence** — Skill frequency, category, level distributions
5. **Remote Work** — Work mode split, by country, by experience
6. **Country Trends** — Market AI jobs, salary, remote % over time
7. **Role Intelligence** — Category, company type, industry, top cities
8. **Methodology** — Limitations table and data source documentation

---

## Data Notes

- **Historical**: posted_year 2020–2024 (35,815 rows)
- **Projected**: posted_year 2025–2026 (14,185 rows) — synthetic forward data
- **Skills**: independent dataset — job_id does not match ai_jobs (4.1% overlap)
- **Market data**: country_ai_trends ≠ 50k sample (different populations)
