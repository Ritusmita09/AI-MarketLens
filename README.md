# AI MarketLens

## AI-Powered Global Data Science & AI Job Market Intelligence Platform

> **Academic Internship Project** — IBM SkillsBuild Data Analytics with AI  
> BharatCares × AICTE × IBM  
> **Author:** Ritusmita Dutta

---

## Overview

AI MarketLens is an end-to-end data analytics and machine learning project that analyses a global dataset of AI and Data Science job postings. The project covers the full analytics lifecycle: data ingestion, cleaning, feature engineering, exploratory data analysis, statistical testing, supervised machine learning, unsupervised clustering, and three interactive dashboards (Power BI, Streamlit, HTML/JS).

> ⚠️ **Important:** The dataset used in this project is **synthetically generated**. All categorical dimensions (country, industry, role, company type/size, remote type) show near-perfect uniform distributions. Findings should **not** be used for real-world career or business decisions.

---

## Problem Statement

Organisations and job seekers face uncertainty in the AI/Data Science labour market:
- Which roles and skills are in highest demand?
- How do salaries vary by experience, geography, and role?
- How is remote work adoption evolving?
- Which countries lead in AI job growth?

This project delivers a data-driven analytics platform to explore these questions using a structured synthetic dataset.

---

## Objectives

1. Perform a rigorous exploratory data analysis of the AI job market dataset.
2. Engineer meaningful analytical features from raw columns.
3. Conduct statistical hypothesis testing on salary determinants.
4. Build and compare salary regression models (Linear Regression, Random Forest, Gradient Boosting).
5. Apply unsupervised clustering to discover job profile segments.
6. Deliver three interactive dashboards: Power BI, Streamlit, and a standalone HTML/JS app.
7. Produce clean, reproducible, dashboard-ready processed datasets.

---

## Key Analytical Questions

- How has AI/Data Science job demand changed year over year (2020–2026)?
- Which job roles and role categories are most frequently posted?
- How does salary vary by experience level, country, industry, and remote type?
- Which skills are most in demand across the dataset?
- How does remote work adoption differ across countries and over time?
- What job profile segments emerge from unsupervised clustering?
- Which features most strongly predict salary?

---

## Dataset

**Source:** Kaggle synthetic dataset (5 CSV files)  
**Location in repository:** `data/raw/archive (1)/`

| File | Rows | Columns | Role |
|---|---|---|---|
| `ai_jobs.csv` | 50,000 | 14 | Main fact table — individual job postings |
| `skills_demand.csv` | 224,605 | 4 | Job–skill bridge table (see limitation below) |
| `country_ai_trends.csv` | 42 | 6 | Country-level market aggregate statistics |
| `job_title_mapping.csv` | 6 | 3 | Job title lookup / role category dimension |
| `data_dictionary.csv` | 13 | 3 | Column metadata |

### Dataset Characteristics

- **6 countries:** USA, UK, Germany, India, Canada, Australia
- **6 job titles:** MLOps Engineer, AI Researcher, Data Scientist, Applied Scientist, Data Analyst, Machine Learning Engineer
- **11 skills:** Python, R, SQL, AWS, GCP, Azure, TensorFlow, PyTorch, Scikit-learn, NLP, Computer Vision
- **Year range:** 2020–2026 (2025–2026 are projected/synthetic forward data)
- **Zero missing values; zero duplicate rows**

### ⚠️ Critical Data Limitation — Skills Join Failure

`skills_demand.job_id` matches `ai_jobs.job_id` for only **4.1% of records** (2,050 of 50,000). This is a dataset generation artifact, not a filtering decision. **No direct job-level skill join is performed anywhere in this project.** Skills are analysed as an independent dataset.

---

## Project Architecture

```
AI-Data-Science-Job-Market-Analytics/
│
├── data/
│   ├── raw/archive (1)/      ← Original Kaggle files (never modified)
│   ├── processed/            ← Cleaned + feature-engineered CSVs
│   └── exports/              ← Dashboard-ready exports
│
├── notebooks/
│   └── AI_MarketLens_Master.ipynb  ← Single master notebook (72 cells, 26 sections)
│
├── src/                      ← Reusable Python modules
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   └── utils.py
│
├── dashboard/                ← Streamlit multi-page app
│   ├── app.py
│   ├── app_pages/            ← 8 pages
│   └── utils/
│
├── web_dashboard/            ← Standalone HTML/CSS/JS dashboard
│   ├── index.html
│   ├── css/ js/ data/
│
├── powerbi/                  ← Power BI documentation + theme
├── reports/                  ← Validation reports + project report
├── submission/               ← Final internship submission files
└── requirements.txt
```

---

## Technologies

| Layer | Technologies |
|---|---|
| Data processing | Python 3.11+, Pandas, NumPy, Pathlib |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Statistics | SciPy (Kruskal-Wallis, D'Agostino-Pearson) |
| Machine learning | Scikit-learn (LinearRegression, RandomForest, GradientBoosting, KMeans) |
| Notebook | Jupyter Notebook / nbconvert |
| Streamlit dashboard | Streamlit 1.30+ |
| BI dashboard | Power BI Desktop (documented; PBIX built manually from provided spec) |
| Web dashboard | HTML5, CSS3, Vanilla JavaScript, Chart.js 4.4 |

---

## Data Processing

### Cleaning Steps
- Dropped `employment_type` (zero variance — all "Full-time")
- Retained `min_experience_years` as reference but excluded from ML when `experience_level` is a feature
- Labelled city = "Remote" rows as consistent with `remote_type = "Remote"`

### Feature Engineering
| Feature | Definition |
|---|---|
| `salary_mid` | `(salary_min_usd + salary_max_usd) / 2.0` |
| `salary_range` | `salary_max_usd - salary_min_usd` |
| `role_category` | Joined from `job_title_mapping.csv` (Analytics / Engineering) |
| `period_type` | `"Historical"` if `posted_year <= 2024`, else `"Projected"` |
| `experience_numeric` | Entry=0, Mid=1, Senior=2 |
| `remote_flag` | 1 if `remote_type == "Remote"`, else 0 |
| `company_size_numeric` | Small=1, Medium=2, Large=3 |

### Country Enrichment
`ai_jobs` is LEFT JOINed to `country_ai_trends` on `(country, posted_year == year)`.  
Market-level columns are prefixed `market_` to avoid confusion with job-level data.

### Skills Processing
Skills are processed independently from job records. The `job_id` join failure (4.1%) is documented and no join is attempted.

---

## Exploratory Data Analysis

The master notebook covers 26 analysis sections including:
- Job distributions by year, role, country, industry, company type/size
- Historical (2020–2024) vs Projected (2025–2026) comparisons
- Salary distributions (overall, by experience, country, role, industry, remote type)
- Country AI market trends (from `country_ai_trends`)
- Remote work adoption trends
- Skills demand, category, and level analysis
- Top skill per country per year heatmap

---

## Statistical Analysis

| Test | Factor | Method | Result |
|---|---|---|---|
| Normality | salary_mid | D'Agostino-Pearson | NOT normal — non-parametric tests used |
| Salary vs experience_level | salary_mid | Kruskal-Wallis | **Significant** (only meaningful factor) |
| Salary vs country | salary_mid | Kruskal-Wallis | Not significant |
| Salary vs industry | salary_mid | Kruskal-Wallis | Not significant |
| Salary vs remote_type | salary_mid | Kruskal-Wallis | Not significant |
| Salary vs role_category | salary_mid | Kruskal-Wallis | Not significant |
| Salary vs company_type | salary_mid | Kruskal-Wallis | Not significant |
| Salary vs company_size | salary_mid | Kruskal-Wallis | Not significant |

All tests used α = 0.05.

---

## Machine Learning

**Target:** `salary_mid` (regression)  
**Training data:** Historical rows only (2020–2024, ~35,815 rows)  
**Split:** 80/20 train/test, stratified on `experience_level`, `random_state=42`

### Models Compared

| Model | Feature Set | Notes |
|---|---|---|
| Linear Regression (baseline) | experience_level only | Establishes minimum baseline |
| Linear Regression (full) | All valid non-leaking features | Comparison with baseline |
| Random Forest | All valid non-leaking features | 100 estimators |
| Gradient Boosting | All valid non-leaking features | 100 estimators |

**Excluded features (leakage/redundancy):** `employment_type`, `city`, `min_experience_years` (when `experience_level` is present), `salary_min_usd`/`salary_max_usd`/`salary_range` (direct target components)

**Evaluation metrics:** MAE, RMSE, R²

> **Note:** Because the dataset is synthetically generated with uniform distributions, `experience_level` dominates salary prediction. Full-feature model R² is expected to be similar to the baseline. This is a correct finding, not a model failure.

### Clustering
- Algorithm: K-Means
- K tested: 2–8
- Features: `salary_mid`, `experience_numeric`, `remote_flag`, `company_size_numeric`
- Evaluation: Silhouette Score, Davies-Bouldin Index

---

## Dashboards

### Power BI (documented)
Five-page dashboard. Documentation in `powerbi/`.

| Page | Content |
|---|---|
| 1. Executive Overview | KPI cards, year trend, country, role, salary, skills |
| 2. Salary Intelligence | Salary by all dimensions |
| 3. Job Market Trends | Market-level country trends (from `country_ai_trends`) |
| 4. Skills Intelligence | Skill frequency, categories, levels (independent) |
| 5. Work & Role Intelligence | Remote work, role category, cities |

**Import files:** `data/exports/powerbi_jobs.csv`, `powerbi_skills.csv`, `powerbi_country_trends.csv`  
**Theme:** `powerbi/powerbi_theme.json`  
**DAX measures:** documented in `powerbi/POWERBI_DAX_MEASURES.md`

> No `.pbix` file is generated programmatically. Build the report in Power BI Desktop following `powerbi/POWERBI_SETUP.md`.

## Streamlit

Eight-page interactive dashboard for AI & Data Science job market intelligence.

### Live Demo
**[Launch AI MarketLens →](https://ai-marketlens.streamlit.app/)**

### Run Locally

```bash
streamlit run dashboard/app.py
```

### Web Dashboard (HTML/JS)

```bash
cd web_dashboard
python -m http.server 8080
# Open: http://localhost:8080
```

Seven sections, fully static. Loads pre-aggregated JSON from `web_dashboard/data/`.

---

## Project Structure (complete)

```
AI-Data-Science-Job-Market-Analytics/
├── data/
│   ├── raw/archive (1)/
│   │   ├── ai_jobs.csv                   ← DO NOT MODIFY
│   │   ├── skills_demand.csv             ← DO NOT MODIFY
│   │   ├── country_ai_trends.csv         ← DO NOT MODIFY
│   │   ├── job_title_mapping.csv         ← DO NOT MODIFY
│   │   └── data_dictionary.csv           ← DO NOT MODIFY
│   ├── processed/
│   │   ├── jobs_clean.csv                (50,000 rows × 17 cols)
│   │   ├── jobs_country_enriched.csv     (50,000 rows × 21 cols)
│   │   ├── skills_clean.csv              (224,605 rows × 4 cols)
│   │   ├── skill_summary.csv             (17 rows × 4 cols)
│   │   └── country_trends_clean.csv      (42 rows × 7 cols)
│   └── exports/
│       ├── powerbi_jobs.csv
│       ├── powerbi_skills.csv
│       └── powerbi_country_trends.csv
├── notebooks/
│   └── AI_MarketLens_Master.ipynb        (72 cells, 26 sections)
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   └── utils.py
├── dashboard/
│   ├── app.py
│   ├── .streamlit/config.toml
│   ├── utils/ (data.py, charts.py)
│   ├── app_pages/ (8 pages)
│   └── README.md
├── web_dashboard/
│   ├── index.html
│   ├── css/style.css
│   ├── js/ (charts.js, app.js)
│   ├── data/ (7 JSON files)
│   └── README.md
├── powerbi/
│   ├── POWERBI_SETUP.md
│   ├── POWERBI_DATA_MODEL.md
│   ├── POWERBI_DAX_MEASURES.md
│   └── powerbi_theme.json
├── reports/
│   ├── notebook_validation.md
│   ├── canonical_kpis.json
│   ├── FINAL_DELIVERABLE_MANIFEST.md
│   └── Ritusmita_AI_MarketLens_ProjectReport.docx
├── submission/
│   ├── Ritusmita_AI_MarketLens.ipynb
│   ├── requirements.txt
│   ├── Ritusmita_AI_MarketLens_ProjectReport.docx
│   └── README.md
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd AI-Data-Science-Job-Market-Analytics

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place the Kaggle dataset files in:
#    data/raw/archive (1)/
#    (ai_jobs.csv, skills_demand.csv, country_ai_trends.csv,
#     job_title_mapping.csv, data_dictionary.csv)

# 5. Run the preprocessing pipeline (generates data/processed/ and data/exports/)
python -c "
import sys; sys.path.insert(0,'.')
from src.data_loader import load_all
from src.preprocessing import run_full_pipeline
data = load_all()
run_full_pipeline(**{k: data[k] for k in ['ai_jobs','skills_demand','country_ai_trends','job_title_mapping']})
"

# 6. Generate web dashboard JSON data
python generate_dashboard_data.py

# 7. Open the master notebook
jupyter notebook notebooks/AI_MarketLens_Master.ipynb

# 8. Run the Streamlit dashboard
streamlit run dashboard/app.py

# 9. Run the web dashboard
cd web_dashboard
python -m http.server 8080
```

---

## Reproducibility

All processed datasets are generated deterministically from the raw source files using the `src/` Python modules. The pipeline is fully reproducible from step 5 above. Random seeds are set to `random_state=42` in all ML models and `train_test_split` calls.

---

## Key Findings (from processed data)

| KPI | Value |
|---|---|
| Total Job Postings | 50,000 |
| Mean Salary Midpoint | $110,864.89 |
| Median Salary Midpoint | $107,565.25 |
| Remote Job % | 32.96% |
| Entry Avg Salary | $67,473.51 |
| Senior Avg Salary | $157,490.18 |
| Senior/Entry Salary Ratio | 2.33× |
| Top Country (by postings) | UK |
| Top Job Role | MLOps Engineer |
| Top Skill (by frequency) | AWS |
| Historical Jobs (2020–2024) | 35,815 |
| Projected Jobs (2025–2026) | 14,185 |
| Market AI Jobs (total) | 1,734,522 |

---

## Limitations

1. **Synthetic data** — uniform distributions; real-world imbalances absent.
2. **Skills join failure** — 4.1% job_id overlap; no job-level skill analysis possible.
3. **Projected years** — 28.4% of rows are 2025–2026 synthetic forward data.
4. **employment_type** — constant "Full-time"; zero variance; excluded.
5. **Salary driver** — only `experience_level` produces statistically significant salary variation.
6. **Narrow scope** — 6 countries, 6 job titles, 11 skills only.
7. **Small time-series** — 7 years × 6 countries = 42 rows in `country_ai_trends`.
8. **No PBIX file** — Power BI dashboard is fully documented but must be built manually in Power BI Desktop.

---

## Future Improvements

- Replace synthetic data with real-world job posting data from APIs (LinkedIn, Indeed, Glassdoor).
- Expand to 50+ countries and hundreds of job titles.
- Fix the skills–job linkage for job-level skill enrichment.
- Add real-time data ingestion and automated pipeline refresh.
- Implement NLP-based job description analysis.
- Deploy Streamlit dashboard to Streamlit Community Cloud.
- Build a proper Power BI Service deployment.
- Add time-series forecasting with more historical data points.

---

## Author

**Ritusmita Dutta**  
IBM SkillsBuild Data Analytics with AI Internship  
BharatCares × AICTE × IBM

---

## License

This project is for academic and educational purposes.  
The underlying dataset is sourced from Kaggle and remains under its original Kaggle dataset licence.  
All project code (Python, HTML, CSS, JavaScript) in this repository is released under the MIT Licence.

---

## Data Source Acknowledgement

Dataset sourced from Kaggle.  
Raw data files are located at `data/raw/archive (1)/` and must not be modified.  
If the raw data directory is absent, download the dataset from Kaggle and place the five CSV files at that path before running the pipeline.
