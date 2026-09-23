# Power BI Data Model Reference
## AI MarketLens — AI-Powered Global Data Science & AI Job Market Intelligence Platform

---

## Tables

| Table Name | Source File | Rows | Role |
|---|---|---|---|
| powerbi_jobs | data/exports/powerbi_jobs.csv | 50,000 | Main fact table |
| powerbi_country_trends | data/exports/powerbi_country_trends.csv | 42 | Market aggregate dimension |
| powerbi_skills | data/exports/powerbi_skills.csv | 224,605 | Independent skills table |

---

## Data Model Diagram

```
powerbi_jobs (50,000 rows)
  Columns: job_id [PK], job_title, company_type, industry, country,
           city, remote_type, experience_level, min_experience_years,
           salary_min_usd, salary_max_usd, posted_year, company_size,
           salary_mid, salary_range, role_category, period_type,
           market_total_ai_jobs, market_avg_salary_usd,
           market_remote_percentage, market_top_skill
         |
         | Lookup relationship (M:1)
         | powerbi_jobs[country + posted_year]
         |     ──────────────────────────────>
         |
powerbi_country_trends (42 rows)
  Columns: country [PK part 1], year [PK part 2], total_ai_jobs,
           avg_salary_usd, remote_percentage, top_skill, period_type
  Composite PK: country + year


powerbi_skills (224,605 rows) — STANDALONE / NO JOIN TO powerbi_jobs
  Columns: job_id [NOT joined], skill, skill_category, skill_level

  !! WARNING: powerbi_skills.job_id and powerbi_jobs.job_id have only
     4.1% overlap. This is a known dataset generation artifact.
     DO NOT create a relationship between these tables.
     Analyse skills independently.
```

---

## Relationships

### Relationship 1: powerbi_jobs → powerbi_country_trends

| Property | Value |
|---|---|
| From table | powerbi_jobs |
| From columns | country, posted_year |
| To table | powerbi_country_trends |
| To columns | country, year |
| Cardinality | Many-to-One |
| Direction | Single (jobs → trends) |
| Active | Yes |

**How to create in Power BI:**  
Power BI Desktop does not natively support composite key relationships through the GUI.  
Use one of these approaches:

**Option A — Surrogate key (recommended):**
1. In Power Query, add a calculated column to both tables:  
   `CountryYear = [country] & "|" & Text.From([posted_year])` (jobs)  
   `CountryYear = [country] & "|" & Text.From([year])` (trends)
2. Create a Many-to-One relationship on `CountryYear`.

**Option B — DAX RELATED (alternative):**  
Since the market columns are pre-joined in the export (`market_total_ai_jobs`, etc.),
**no relationship is strictly required** — the market values are already embedded in
`powerbi_jobs`. Use the pre-joined columns for cross-table metrics directly.

**Recommended approach for this project:** Use Option B — the enriched export already
includes all market-level columns in `powerbi_jobs`. The standalone
`powerbi_country_trends` table is used only for **market-level trend charts**
(total AI jobs over time, YoY growth, remote % trends).

---

## Column Descriptions (powerbi_jobs — selected key columns)

| Column | Type | Description | Dashboard Use |
|---|---|---|---|
| job_id | Text | Unique job identifier (PK) | Counting only |
| job_title | Text | Job role (6 categories) | Grouping, filtering |
| company_type | Text | Startup / MNC / Research Lab | Segmentation |
| industry | Text | Tech / Healthcare / Retail / Finance / Education | Segmentation |
| country | Text | 6 countries | Geography |
| city | Text | City or "Remote" | Location analysis |
| remote_type | Text | Remote / Hybrid / Onsite | Work mode |
| experience_level | Text | Entry / Mid / Senior | Salary driver, segmentation |
| salary_min_usd | Integer | Min annual salary (USD) | Salary analysis |
| salary_max_usd | Integer | Max annual salary (USD) | Salary analysis |
| posted_year | Integer | 2020–2026 | Temporal analysis |
| company_size | Text | Small / Medium / Large | Segmentation |
| salary_mid | Decimal | (min+max)/2 — central salary estimate | Primary salary KPI |
| salary_range | Decimal | max−min — salary band width | Variability |
| role_category | Text | Analytics / Engineering | Role segmentation |
| period_type | Text | Historical / Projected | Temporal segmentation |
| market_total_ai_jobs | Integer | Country-year total AI jobs (market-wide) | Market context |
| market_avg_salary_usd | Integer | Country-year avg salary (market-wide) | Market salary |
| market_remote_percentage | Integer | Country-year remote % (market-wide) | Market remote work |
| market_top_skill | Text | Most demanded skill that country-year | Market skill |

---

## Excluded Column

| Column | Reason Excluded |
|---|---|
| employment_type | Zero variance — all rows are "Full-time". Dropped in preprocessing. |
| min_experience_years | Redundant with experience_level (Entry=0, Mid=2, Senior=5). |

---

## Skills Table (Standalone)

`powerbi_skills` is used for skills-specific visuals only.  
It connects to no other table.  
Use it to build:
- Skill frequency bar chart
- Skill category donut
- Skill level donut
- Cross-filter with independent skill slicers

**Do NOT create a relationship** between `powerbi_skills[job_id]` and `powerbi_jobs[job_id]`.  
The job_id values share only 4.1% overlap due to a dataset generation artifact.  
Any join would produce 95.9% null rows.

---

## Model Best Practices for this Project

1. Import mode (not DirectQuery) — all files are small static CSVs.
2. Disable the auto-date hierarchy on `posted_year` — use the integer year directly.
3. Sort `experience_level` by a custom sort column: Entry=1, Mid=2, Senior=3.
4. Sort `company_size` by: Small=1, Medium=2, Large=3.
5. Create a `period_type` slicer default filter to "Historical" for non-projected analysis.
6. Use **Bookmarks** to toggle between "All Years" and "Historical Only" views.
