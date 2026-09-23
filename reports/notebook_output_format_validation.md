# Notebook Output Format Validation Report — Phase B

**Project:** AI MarketLens  
**Notebook:** `submission/Ritusmita_AI_MarketLens.ipynb`  
**Phase:** B — Output Formatting and Presentation Cleanup  
**Date:** 2026-09-23

---

## Summary

| Metric | Value |
|--------|-------|
| Total cells reviewed | 72 |
| Code cells | 35 |
| Markdown cells | 37 |
| Cells reformatted | **21** |
| Raw print/text outputs converted to tables | **21** |
| Raw list/dict/Series dumps removed | **21** |
| Styled DataFrame tables now displayed | **26** |
| Charts/visualisations preserved | **22** |
| Stream outputs (short status messages only) | 13 |
| Runtime errors after reformatting | **0** |
| Static analysis errors (pyright) | **0** |
| Clean-kernel Run-All result | **PASS** |

---

## Clean-Run Validation

| Check | Result |
|-------|--------|
| Restart kernel + Run All | PASS |
| Code cells executed | 35 / 35 |
| Runtime errors | 0 |
| Display outputs rendered | 48 |
| Charts rendered | 22 |
| Tables rendered | 26 |
| Execution time | ~230 seconds |
| pyright errors | 0 |

---

## Cells Reformatted (21 total)

| Cell | Section | Before | After |
|------|---------|--------|-------|
| 01 — Data Loading | §7 Data Loading | Raw `validate_raw_files` text block | **Dataset Inventory** table (File, Rows, Columns, Missing, Duplicates, Role) |
| 02 — Quality Report | §8 Data Quality | `quality_report()` print loop per file | **Data Quality Summary** table (all 5 files in one table) |
| 03 — Join Integrity | §8 Data Quality | 4 raw print statements | **Join Integrity Validation** table (Join, Match Rate, Status, Notes) |
| 04 — Preprocessing | §9 Preprocessing | `print(shape)` for each dataset | **Processed Datasets Summary** table (5 datasets, rows/cols/missing/dupes) |
| 05 — Column Schema | §9 Preprocessing | `print(columns.tolist())` | **jobs_clean Column Schema** table (Column, Data Type, Unique Values, Sample) |
| 06 — Feature Eng. | §10 Feature Engineering | Loop printing `feature: sample` | **Engineered Features** table (Feature, Type, Definition, Usage, Sample) |
| 07 — Year Counts | §11 EDA | `print(year_counts.to_string())` | Styled **Job Postings by Year** table (Year, Period, Job Postings) |
| 11 — Salary Dist. | §11 EDA | `print(describe().apply(...))` | **Salary Midpoint Summary Statistics** table (8-row describe table, formatted USD) |
| 14 — Salary by Exp | §13 Salary | `print(_sal_agg.reindex(order))` | **Salary by Experience Level** table (Experience, Mean, Median, Std Dev, Sample Size) |
| 15 — Salary by Ctry | §13 Salary | `print(_sal_ctry.sort_values())` | **Salary by Country** table (Country, Mean, Median, Job Count, formatted USD) |
| 22 — Skill Summary | §16 Skills | `print(skill_summary.to_string())` | Styled **Skill Demand Summary** table |
| 23 — Hist/Proj | §17 Historical | `print()` comparison lines | **Period Comparison** table (Period, Job Postings, %, Mean/Median Salary) |
| 24 — Stat Tests | §18 Statistics | Inline prints + `results_table.to_string()` | **Normality Test** table + **Kruskal-Wallis** table (H, p-value, Significant, Interpretation) |
| 25 — ML Setup | §19 ML | `print(f'Feature matrix: ...')` | **ML Training Configuration** table (Training rows, shape, target, features) |
| 26 — Train/Test | §19 ML | `print(f'Train: ... Test: ...')` | **Train/Test Split** table (Split, Rows, Percentage) |
| 27 — Model Training | §19 ML | Console output per model during training | Silent training — single `print('Model training complete.')` |
| 28 — Model Compare | §20 Model Eval | `print(model_comparison.to_string())` | Styled **Model Performance Comparison** table (Model, Feature Set, MAE, RMSE, R²) |
| 30 — Feature Imp. | §21 Feature Imp. | `print(feat_importance.head(10).to_string())` | Ranked **Top 10 Feature Importances** table with Rank index |
| 31 — K Evaluation | §22 Clustering | `print(f'Best K by Silhouette...')` | **K-Means Evaluation** table (K, Inertia, Silhouette Score, Davies-Bouldin) with best-K markers |
| 32 — Cluster Profile | §22 Clustering | `print(cluster_profile.to_string())` | Styled **Cluster Profiles** table (Cluster, Avg/Median Salary, Count, Exp, Remote %, Co.Size) |
| 33 — Key Insights | §23 Key Insights | 6 print-loop blocks | **6 structured tables**: Salary by Experience, Job Role Distribution, Role Category Split, Remote Work Distribution, Top Skills, Country Market Highlights |

---

## Output Classification (Final State)

| Cell | Classification |
|------|---------------|
| 07 — Imports | D. Short status message |
| 09 — Data Loading | C. Structured table + D. Status |
| 11 — Quality Report | C. Structured table |
| 12 — Join Integrity | C. Structured table |
| 14 — Preprocessing | C. Structured table + D. Status |
| 15 — Column Schema | C. Structured table + D. Status |
| 17 — Feature Eng. | C. Structured table + D. Status |
| 19 — Year Chart | B. Visualization + C. Structured table |
| 21 — Role Charts | B. Visualization |
| 23 — Dim Charts | B. Visualization |
| 25 — Remote/Exp Charts | B. Visualization |
| 27 — Salary Histograms | B. Visualization + C. Structured table |
| 29 — Country Heatmap | B. Visualization |
| 30 — City Chart | B. Visualization |
| 32 — Salary/Exp Charts | B. Visualization + C. Structured table |
| 33 — Salary/Country | B. Visualization + C. Structured table |
| 34 — Multi-dim Salary | B. Visualization |
| 36 — Country Trends | B. Visualization |
| 38 — Remote Trends | B. Visualization |
| 40 — Top Skill Grid | B. Visualization |
| 42 — Remote Work | B. Visualization |
| 44 — Skills Chart | B. Visualization |
| 45 — Skill Cats | B. Visualization + C. Structured table |
| 47 — Hist/Proj | B. Visualization + C. Structured table |
| 49 — Stat Tests | F. Statistical result table |
| 51 — ML Setup | C. Structured table |
| 52 — Train/Test | C. Structured table |
| 53 — Model Training | D. Short status message |
| 54 — Model Comparison | E. Model result table |
| 56 — Residuals | B. Visualization |
| 58 — Feature Imp. | B. Visualization + E. Model result table |
| 60 — Clustering K | B. Visualization + C. Structured table |
| 61 — Cluster Profile | B. Visualization + C. Structured table |
| 63 — Key Insights | C. Structured tables ×6 |
| 71 — Export | D. Short status messages |

---

## Formatting Conventions Applied

| Convention | Applied |
|------------|---------|
| Currency: `$110,864.89` | All salary columns |
| Large counts: `50,000` | All row/job counts |
| Percentages: `32.96%` | All pct columns |
| P-values: `<0.001` or `0.0342` | Statistical results |
| R²: `0.9876` (4 d.p.) | Model metrics |
| `display()` for all tables | Yes — no `print(df)` |
| `.style.set_caption()` for all tables | Yes |
| `.hide(axis='index')` where index not meaningful | Yes |
| `print()` retained only for status messages | Yes |

---

## Files Changed

| File | Change |
|------|--------|
| `submission/Ritusmita_AI_MarketLens.ipynb` | 21 cells reformatted + clean execution |
| `notebooks/AI_MarketLens_Master.ipynb` | Synced from submission |
| `format_notebook_outputs.py` | Format script created |
| `reports/notebook_output_format_validation.md` | This file |
