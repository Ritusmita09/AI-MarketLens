# Power BI DAX Measures Reference
## AI MarketLens — AI-Powered Global Data Science & AI Job Market Intelligence Platform

All measures reference the **powerbi_jobs** table unless stated otherwise.  
Create these in a dedicated `_Measures` table for clean organisation.

---

## Job Count Measures

```dax
Total Job Postings =
COUNTROWS('powerbi_jobs')

Historical Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[period_type] = "Historical"
)

Projected Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[period_type] = "Projected"
)

Countries Covered =
DISTINCTCOUNT('powerbi_jobs'[country])

Job Roles Count =
DISTINCTCOUNT('powerbi_jobs'[job_title])

Skills Tracked =
DISTINCTCOUNT('powerbi_skills'[skill])
```

---

## Salary Measures

```dax
Average Salary =
AVERAGE('powerbi_jobs'[salary_mid])

Median Salary =
MEDIAN('powerbi_jobs'[salary_mid])

Min Salary =
MIN('powerbi_jobs'[salary_min_usd])

Max Salary =
MAX('powerbi_jobs'[salary_max_usd])

Salary Range =
[Max Salary] - [Min Salary]

Entry Average Salary =
CALCULATE(
    AVERAGE('powerbi_jobs'[salary_mid]),
    'powerbi_jobs'[experience_level] = "Entry"
)

Mid Average Salary =
CALCULATE(
    AVERAGE('powerbi_jobs'[salary_mid]),
    'powerbi_jobs'[experience_level] = "Mid"
)

Senior Average Salary =
CALCULATE(
    AVERAGE('powerbi_jobs'[salary_mid]),
    'powerbi_jobs'[experience_level] = "Senior"
)

Senior vs Entry Salary Ratio =
DIVIDE(
    [Senior Average Salary],
    [Entry Average Salary],
    BLANK()
)

Senior Premium % =
([Senior Average Salary] - [Entry Average Salary]) / [Entry Average Salary] * 100
```

---

## Remote Work Measures

```dax
Remote Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[remote_type] = "Remote"
)

Hybrid Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[remote_type] = "Hybrid"
)

Onsite Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[remote_type] = "Onsite"
)

Remote Job Pct =
DIVIDE([Remote Jobs], [Total Job Postings], 0) * 100

Hybrid Job Pct =
DIVIDE([Hybrid Jobs], [Total Job Postings], 0) * 100

Onsite Job Pct =
DIVIDE([Onsite Jobs], [Total Job Postings], 0) * 100
```

---

## Role Category Measures

```dax
Analytics Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[role_category] = "Analytics"
)

Engineering Jobs =
CALCULATE(
    COUNTROWS('powerbi_jobs'),
    'powerbi_jobs'[role_category] = "Engineering"
)

Analytics Role Pct =
DIVIDE([Analytics Jobs], [Total Job Postings], 0) * 100

Engineering Role Pct =
DIVIDE([Engineering Jobs], [Total Job Postings], 0) * 100
```

---

## Market-Level Measures (from powerbi_country_trends)

```dax
Total Market AI Jobs =
SUM('powerbi_country_trends'[total_ai_jobs])

Average Market Salary =
AVERAGE('powerbi_country_trends'[avg_salary_usd])

Average Market Remote Pct =
AVERAGE('powerbi_country_trends'[remote_percentage])

Historical Market Jobs =
CALCULATE(
    SUM('powerbi_country_trends'[total_ai_jobs]),
    'powerbi_country_trends'[period_type] = "Historical"
)

Projected Market Jobs =
CALCULATE(
    SUM('powerbi_country_trends'[total_ai_jobs]),
    'powerbi_country_trends'[period_type] = "Projected"
)
```

---

## Year-over-Year Measures (using powerbi_country_trends)

```dax
-- YoY growth for a selected year vs prior year (for country_trends table)
Market Jobs Prior Year =
CALCULATE(
    SUM('powerbi_country_trends'[total_ai_jobs]),
    DATEADD('powerbi_country_trends'[year], -1, YEAR)
)
```

> **Note:** Because `year` is an integer (not a date), YoY calculations
> require either a Date table or a calculated RANKX approach.
> The simplest approach is to add a calculated column:
>
> ```dax
> Prior Year Jobs (column) =
> VAR CurrentYear = 'powerbi_country_trends'[year]
> VAR CurrentCountry = 'powerbi_country_trends'[country]
> RETURN
> CALCULATE(
>     SUM('powerbi_country_trends'[total_ai_jobs]),
>     FILTER(
>         'powerbi_country_trends',
>         'powerbi_country_trends'[year] = CurrentYear - 1
>         && 'powerbi_country_trends'[country] = CurrentCountry
>     )
> )
>
> YoY Growth Pct (column) =
> DIVIDE(
>     'powerbi_country_trends'[total_ai_jobs] - 'powerbi_country_trends'[Prior Year Jobs (column)],
>     'powerbi_country_trends'[Prior Year Jobs (column)],
>     BLANK()
> ) * 100
> ```

---

## Top N Measures

```dax
Top Country =
CALCULATE(
    SELECTEDVALUE('powerbi_jobs'[country]),
    TOPN(1,
         SUMMARIZE('powerbi_jobs', 'powerbi_jobs'[country],
                   "Cnt", COUNTROWS('powerbi_jobs')),
         [Cnt], DESC)
)

Top Job Role =
CALCULATE(
    SELECTEDVALUE('powerbi_jobs'[job_title]),
    TOPN(1,
         SUMMARIZE('powerbi_jobs', 'powerbi_jobs'[job_title],
                   "Cnt", COUNTROWS('powerbi_jobs')),
         [Cnt], DESC)
)

Top Skill (from skills table) =
CALCULATE(
    SELECTEDVALUE('powerbi_skills'[skill]),
    TOPN(1,
         SUMMARIZE('powerbi_skills', 'powerbi_skills'[skill],
                   "Cnt", COUNTROWS('powerbi_skills')),
         [Cnt], DESC)
)
```

---

## Conditional Formatting Helpers

```dax
-- Returns 1 for projected years, 0 for historical (use in conditional formatting)
Is Projected Year =
IF(
    SELECTEDVALUE('powerbi_country_trends'[period_type]) = "Projected",
    1,
    0
)

Is Projected Job =
IF(
    SELECTEDVALUE('powerbi_jobs'[period_type]) = "Projected",
    1,
    0
)
```

---

## Notes

- **salary_mid** = (salary_min_usd + salary_max_usd) / 2 — pre-computed in the export.
- **role_category** — joined from job_title_mapping in pre-processing; no join needed in Power BI.
- **powerbi_skills** is NOT joined to powerbi_jobs — the job_id overlap is only 4.1%. Use skills independently.
- All salary figures are in **USD**.
- **period_type** distinguishes Historical (2020–2024) from Projected (2025–2026).
