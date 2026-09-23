# AI MarketLens — Final Deliverable Manifest

**Project:** AI MarketLens — AI-Powered Global Data Science & AI Job Market Intelligence Platform  
**Student:** Ritusmita Dutta  
**Internship:** IBM SkillsBuild Data Analytics with AI | BharatCares × AICTE × IBM  
**Phase:** 4 — Finalization, QA, Documentation, Submission  
**Status:** ✅ COMPLETE

---

## Submission Package (4 files)

| File | Size | Description |
|------|------|-------------|
| `submission/Ritusmita_AI_MarketLens.ipynb` | ~52 KB | Master notebook — 72 cells, 26 sections, all phases |
| `submission/requirements.txt` | ~384 B | Pinned dependencies for full reproducibility |
| `submission/Ritusmita_AI_MarketLens_ProjectReport.docx` | ~46 KB | 15-section academic project report |
| `submission/README.md` | ~16 KB | Full project README with architecture, KPIs, run instructions |

---

## Full Project Deliverables

### Raw Data (NEVER MODIFIED)
| File | Rows | Columns | Role |
|------|------|---------|------|
| `data/raw/archive (1)/ai_jobs.csv` | 50,000 | 14 | Main fact table |
| `data/raw/archive (1)/skills_demand.csv` | 224,605 | 4 | Skills bridge |
| `data/raw/archive (1)/country_ai_trends.csv` | 42 | 6 | Country market aggregates |
| `data/raw/archive (1)/job_title_mapping.csv` | 6 | 3 | Role dimension |
| `data/raw/archive (1)/data_dictionary.csv` | 13 | 3 | Column metadata |

### Processed Data
| File | Description |
|------|-------------|
| `data/processed/jobs_clean.csv` | 50,000 × 17 — cleaned jobs with engineered features |
| `data/processed/jobs_country_enriched.csv` | 50,000 × 21 — jobs enriched with country market data |
| `data/processed/skills_clean.csv` | 224,605 × 4 — cleaned skills |
| `data/processed/skill_summary.csv` | 17 × 4 — skill frequency aggregates |
| `data/processed/country_trends_clean.csv` | 42 × 7 — cleaned country trends |

### Export Data (Dashboard-Ready)
| File | Description |
|------|-------------|
| `data/exports/powerbi_jobs.csv` | 50,000 × 21 — Power BI main table |
| `data/exports/powerbi_skills.csv` | 224,605 × 4 — Power BI skills table |
| `data/exports/powerbi_country_trends.csv` | 42 × 7 — Power BI country trends table |

### Notebook
| File | Description |
|------|-------------|
| `notebooks/AI_MarketLens_Master.ipynb` | 72 cells, 37 markdown, 35 code, 26 sections, 0 errors |
| `notebooks/AI_MarketLens_Master_executed.ipynb` | Executed copy with outputs (1,884 KB) |

### Source Modules (`src/`)
| File | Description |
|------|-------------|
| `src/__init__.py` | Package init |
| `src/data_loader.py` | Dataset loading utilities |
| `src/preprocessing.py` | Cleaning and feature engineering pipeline |
| `src/feature_engineering.py` | Advanced feature construction |
| `src/utils.py` | Shared helper functions |

### Streamlit Dashboard (`dashboard/`)
| File | Description |
|------|-------------|
| `dashboard/app.py` | Main Streamlit app entry point — 8 pages |
| `dashboard/.streamlit/config.toml` | Theme and layout configuration |
| `dashboard/utils/data.py` | Data loading utilities |
| `dashboard/utils/charts.py` | Chart helper functions |
| `dashboard/app_pages/overview.py` | Overview page |
| `dashboard/app_pages/salary.py` | Salary intelligence page |
| `dashboard/app_pages/job_market.py` | Job market page |
| `dashboard/app_pages/skills.py` | Skills demand page |
| `dashboard/app_pages/remote_work.py` | Remote work page |
| `dashboard/app_pages/ml_insights.py` | ML insights page |
| `dashboard/app_pages/data_explorer.py` | Data explorer page |
| `dashboard/app_pages/methodology.py` | Methodology page |
| `dashboard/README.md` | Dashboard run instructions |

### Web Dashboard (`web_dashboard/`)
| File | Description |
|------|-------------|
| `web_dashboard/index.html` | Standalone HTML/JS dashboard — 7 sections |
| `web_dashboard/css/style.css` | Dark theme CSS |
| `web_dashboard/js/charts.js` | Chart.js 4.4 chart definitions |
| `web_dashboard/js/app.js` | Application logic |
| `web_dashboard/data/kpis.json` | Authoritative KPI values |
| `web_dashboard/data/salary.json` | Salary aggregates |
| `web_dashboard/data/countries.json` | Country data |
| `web_dashboard/data/skills.json` | Skills data |
| `web_dashboard/data/roles.json` | Job roles data |
| `web_dashboard/data/remote.json` | Remote work data |
| `web_dashboard/data/trends.json` | Year trends data |
| `web_dashboard/README.md` | Dashboard run instructions |

### Power BI Documentation (`powerbi/`)
| File | Description |
|------|-------------|
| `powerbi/POWERBI_SETUP.md` | Step-by-step Power BI setup guide |
| `powerbi/POWERBI_DATA_MODEL.md` | Data model and relationships documentation |
| `powerbi/POWERBI_DAX_MEASURES.md` | 28 DAX measure definitions |
| `powerbi/powerbi_theme.json` | Professional colour theme JSON |

### Reports (`reports/`)
| File | Description |
|------|-------------|
| `reports/canonical_kpis.json` | Authoritative KPI values (source of truth) |
| `reports/notebook_validation.md` | Notebook quality audit — 0 errors, 0 warnings |
| `reports/Ritusmita_AI_MarketLens_ProjectReport.docx` | 15-section academic project report |
| `reports/FINAL_DELIVERABLE_MANIFEST.md` | This file |

### Root Files
| File | Description |
|------|-------------|
| `README.md` | Full project README |
| `requirements.txt` | Pinned Python dependencies |
| `reconcile_kpis.py` | KPI recalculation script |
| `build_report.py` | .docx report generation script |
| `audit_notebook.py` | Notebook validation script |
| `generate_dashboard_data.py` | Web dashboard JSON generation |
| `validate_phase2.py` | Phase 2 validation script |
| `validate_phase3.py` | Phase 3 validation script |
| `build_notebook.py` | Notebook construction script |
| `.gitignore` | Git ignore rules |

---

## Authoritative KPIs (from `reports/canonical_kpis.json`)

| KPI | Value |
|-----|-------|
| Total Job Postings | 50,000 |
| Historical Jobs (2020–2024) | 35,815 |
| Projected Jobs (2025–2026) | 14,185 |
| Mean Salary Midpoint | $110,864.89 |
| Median Salary Midpoint | $107,565.25 |
| Min Salary Midpoint | $57,607.50 |
| Max Salary Midpoint | $167,468.00 |
| Entry Avg Salary | $67,473.51 |
| Mid Avg Salary | $107,507.12 |
| Senior Avg Salary | $157,490.18 |
| Senior / Entry Ratio | 2.3341× |
| Remote Job % | 32.96% |
| Countries Covered | 6 |
| Job Roles | 6 |
| Skills Tracked | 11 |
| Top Country | UK |
| Top Job Role | MLOps Engineer |
| Top Skill | AWS |
| Total Market AI Jobs | 1,734,522 |
| Mean Market Avg Salary | $124,778 |
| Mean Market Remote % | 56.4% |

> **Definition:** `salary_mid = (salary_min_usd + salary_max_usd) / 2.0`  
> **Source:** Computed by `reconcile_kpis.py` from `data/exports/powerbi_jobs.csv`

---

## Phase Completion Summary

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Dataset audit (5 files, schema, relationships, quality, ML opportunities) | ✅ Complete |
| Phase 2 | Preprocessing pipeline, feature engineering, master notebook (26 sections) | ✅ Complete |
| Phase 3 | Power BI docs, Streamlit dashboard, HTML/JS dashboard | ✅ Complete |
| Phase 4 | KPI reconciliation, notebook audit, report, submission packaging | ✅ Complete |

---

*Generated by AI MarketLens Phase 4 Finalization — IBM SkillsBuild Internship Project*
