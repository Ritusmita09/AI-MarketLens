# Power BI Setup Guide
## AI MarketLens — AI-Powered Global Data Science & AI Job Market Intelligence Platform

---

## Prerequisites

- Power BI Desktop (latest version recommended — download from Microsoft)
- The following CSV export files from this project:

| File | Path | Rows |
|---|---|---|
| powerbi_jobs.csv | `data/exports/powerbi_jobs.csv` | 50,000 |
| powerbi_skills.csv | `data/exports/powerbi_skills.csv` | 224,605 |
| powerbi_country_trends.csv | `data/exports/powerbi_country_trends.csv` | 42 |

---

## Step 1 — Create a New Power BI Report

1. Open Power BI Desktop.
2. Click **Get Data → Text/CSV**.
3. Import the three CSV files listed above, one at a time.

---

## Step 2 — Apply the Custom Theme

1. In Power BI Desktop, go to the **View** tab.
2. Click **Themes → Browse for themes**.
3. Navigate to `powerbi/powerbi_theme.json` in this project folder.
4. Select and apply the theme.

This applies the AI MarketLens colour palette, typography, and card styles.

---

## Step 3 — Set Data Types

After importing, verify these column types in Power Query Editor:

### powerbi_jobs.csv
| Column | Type |
|---|---|
| job_id | Text |
| job_title | Text |
| company_type | Text |
| industry | Text |
| country | Text |
| city | Text |
| remote_type | Text |
| experience_level | Text |
| min_experience_years | Whole Number |
| salary_min_usd | Whole Number |
| salary_max_usd | Whole Number |
| posted_year | Whole Number |
| company_size | Text |
| salary_mid | Decimal Number |
| salary_range | Decimal Number |
| role_category | Text |
| period_type | Text |
| market_total_ai_jobs | Whole Number |
| market_avg_salary_usd | Whole Number |
| market_remote_percentage | Whole Number |
| market_top_skill | Text |

### powerbi_skills.csv
| Column | Type |
|---|---|
| job_id | Text |
| skill | Text |
| skill_category | Text |
| skill_level | Text |

### powerbi_country_trends.csv
| Column | Type |
|---|---|
| country | Text |
| year | Whole Number |
| total_ai_jobs | Whole Number |
| avg_salary_usd | Whole Number |
| remote_percentage | Whole Number |
| top_skill | Text |
| period_type | Text |

---

## Step 4 — Build the Data Model

See **POWERBI_DATA_MODEL.md** for full relationship details.

Key relationships to create in Power BI:
1. `powerbi_jobs[country] + powerbi_jobs[posted_year]` → `powerbi_country_trends[country] + powerbi_country_trends[year]`  
   (Many-to-One)
2. Skills remain **analytically separate** — do NOT join powerbi_skills to powerbi_jobs on job_id.  
   The job_id columns have only 4.1% overlap (dataset generation artifact — see audit report).

---

## Step 5 — Create DAX Measures

See **POWERBI_DAX_MEASURES.md** for all DAX formulas.

Create a dedicated measures table:
1. In the **Modeling** tab, click **New Table**.
2. Enter: `_Measures = DATATABLE("Placeholder", STRING, {{""}})` 
3. Add all measures from POWERBI_DAX_MEASURES.md to this table.

---

## Step 6 — Build the Report Pages

Create five pages:

| Page | Title |
|---|---|
| 1 | Executive Overview |
| 2 | Salary Intelligence |
| 3 | Job Market Trends |
| 4 | Skills Intelligence |
| 5 | Work & Role Intelligence |

Refer to the Visual Layout section below for each page's visuals.

---

## Step 7 — Add Slicers (Filters)

On all pages, add the following slicers from powerbi_jobs:
- `posted_year` (filter: Historical = 2020–2024, Projected = 2025–2026)
- `country`
- `industry`
- `job_title`
- `experience_level`
- `remote_type`
- `company_type`
- `company_size`
- `period_type`

---

## Page Layout Specifications

### Page 1 — Executive Overview

**KPI Cards** (top row):
- Total Job Postings: `[Total Job Postings]`
- Average Salary: `[Average Salary]`
- Median Salary: `[Median Salary]`
- Remote Job %: `[Remote Job Pct]`
- Countries Covered: `[Countries Covered]`
- Skills Tracked: `[Skills Tracked]`

**Charts:**
1. Line chart: Total AI Jobs by Year (from powerbi_country_trends — market level)  
   X: year | Y: total_ai_jobs | Legend: country | Add period_type as colour/dashed line
2. Bar chart: Job Postings by Country (from powerbi_jobs)  
   X: country | Y: [Total Job Postings]
3. Donut chart: Job Postings by Role  
   Legend: job_title | Values: [Total Job Postings]
4. Bar chart: Average Salary by Experience Level  
   X: experience_level | Y: [Average Salary] | Sorted: Entry → Mid → Senior
5. Donut chart: Remote vs Hybrid vs Onsite  
   Legend: remote_type | Values: [Total Job Postings]
6. Bar chart: Top Skills (from powerbi_skills)  
   X: skill | Y: Count of skill rows

**Important note to add as text box:**  
"Job Postings (50,000 rows) = sample dataset. Market AI Jobs = country_ai_trends aggregate statistics. These are different populations."

---

### Page 2 — Salary Intelligence

**KPI Cards:**
- Average Salary, Median Salary, Min Salary, Max Salary, Salary Range, Senior/Entry Ratio

**Charts:**
1. Box plot or column: salary_mid by experience_level (sorted Entry → Mid → Senior)
2. Bar chart: salary_mid by job_title
3. Bar chart: salary_mid by country
4. Bar chart: salary_mid by industry
5. Bar chart: salary_mid by company_type
6. Bar chart: salary_mid by company_size
7. Bar chart: salary_mid by remote_type
8. Histogram: salary_mid distribution (use a bin column or PowerBI histogram visual)

**Slicers:** All dimension slicers (see Step 7)

---

### Page 3 — Job Market Trends

**Source: powerbi_country_trends (market-level data)**

**KPI Cards:**
- Total Market AI Jobs, Average Market Salary, Average Remote %

**Charts:**
1. Line chart: total_ai_jobs by year per country  
   (Use dashed/conditional format for period_type = 'Projected')
2. Stacked bar: total_ai_jobs by country per year
3. Line chart: avg_salary_usd by year per country
4. Line chart: remote_percentage by year per country
5. Matrix/heatmap: country × year → total_ai_jobs
6. Bar chart: YoY growth (calculated measure)

**Add text box:** "2025–2026 are projected/synthetic future years, not observed data."

---

### Page 4 — Skills Intelligence

**Source: powerbi_skills (independent — NOT joined to powerbi_jobs)**

**Charts:**
1. Bar chart: Count of skill by skill (top skills)
2. Donut chart: Count by skill_category
3. Donut chart: Count by skill_level
4. Matrix: skill × skill_category with count
5. Bar chart: top_skill from powerbi_country_trends by country (filter by year slicer)

**Add text box:**  
"⚠ Skills data is analyzed independently. The skills_demand.job_id column does not reliably match ai_jobs.job_id (only 4.1% overlap — dataset generation artifact). Job-level skill enrichment is not available."

---

### Page 5 — Work & Role Intelligence

**Charts:**
1. Donut: remote_type distribution
2. Bar: remote % by country
3. Bar: remote % by industry
4. Bar: remote % by experience_level
5. Bar: Job postings by role_category (Analytics vs Engineering)
6. Bar: Job postings by job_title
7. Bar: Top 15 cities (exclude city = 'Remote')
8. Treemap: industry × company_type

---

## Important Limitations to Display

Include a dedicated "Limitations" text page or tooltip:
1. Dataset is synthetically generated (uniform distributions).
2. skills_demand job_id does not reliably join to ai_jobs job_id.
3. 2025–2026 are projected/synthetic years.
4. employment_type = Full-time for all rows (excluded from analysis).
5. Salary variation is dominated by experience_level only.
6. Only 6 countries and 6 job titles covered.
7. country_ai_trends = market-level aggregates, not identical to the 50k sample.
