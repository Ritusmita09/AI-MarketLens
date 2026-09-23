"""Methodology page — AI MarketLens Streamlit Dashboard."""
import streamlit as st

st.title(":material/info: Methodology & Limitations")
st.divider()

st.markdown("""
## Project Overview

**AI MarketLens** is an academic internship project analysing a synthetic global AI and Data Science job market dataset.

| Property | Value |
|---|---|
| Dataset source | Kaggle (synthetic) |
| Job postings | 50,000 |
| Countries | 6 (USA, UK, Germany, India, Canada, Australia) |
| Job titles | 6 (MLOps Engineer, AI Researcher, Data Scientist, Applied Scientist, Data Analyst, Machine Learning Engineer) |
| Skills | 11 (Python, R, SQL, AWS, GCP, Azure, TensorFlow, PyTorch, Scikit-learn, NLP, Computer Vision) |
| Year range | 2020–2026 (2025–2026 = projected/synthetic) |
| Market data | country_ai_trends.csv — 42 rows (6 countries × 7 years) |
""")

st.divider()

st.subheader(":material/warning: Data Limitations")
st.error(
    "**Critical:** This dataset is synthetically generated. "
    "All categorical dimensions show near-uniform distributions. "
    "Findings should NOT be used for real-world career or business decisions."
)

limitations = [
    ("1. Synthetic Data",
     "The dataset was generated synthetically. All categorical dimensions "
     "(country, industry, job title, company type/size, remote type) show near-perfect "
     "uniform distributions (~16.7% each for 6 countries, ~20% each for 5 industries, etc.). "
     "Real-world imbalances are absent."),
    ("2. Skills Join Failure",
     "skills_demand.job_id does NOT reliably match ai_jobs.job_id. Only 4.1% of IDs overlap "
     "(2,050 of 50,000). This is a dataset generation artifact. Skills are therefore analysed "
     "as an independent dataset. Job-level skill enrichment (salary by skill, country by skill) "
     "is not available from job records."),
    ("3. Projected Years",
     "28.4% of job postings (14,185 rows) have posted_year = 2025 or 2026. "
     "These are projected/synthetic forward entries, not observed historical data. "
     "All dashboards distinguish 'Historical' (2020–2024) from 'Projected' (2025–2026)."),
    ("4. Employment Type",
     "All 50,000 rows have employment_type = 'Full-time'. This column has zero variance "
     "and was excluded from all analysis and modelling."),
    ("5. Salary Independence",
     "Salary varies meaningfully ONLY with experience_level (Entry ~$67k, Mid ~$107k, "
     "Senior ~$157k). Variation by country, industry, role, remote type, and company "
     "characteristics is negligible (~$1,000 range) — a consequence of synthetic generation. "
     "ML salary models will converge primarily on experience_level."),
    ("6. Narrow Scope",
     "Only 6 countries, 6 job titles, and 11 skills are represented. "
     "These do not capture the full global AI job market."),
    ("7. Two Data Populations",
     "The 50,000-row jobs dataset and the country_ai_trends dataset are independent. "
     "country_ai_trends represents market-level aggregates (4,000–78,139 jobs/year/country). "
     "These numbers are NOT the same as counts from the 50k sample (~1,100–1,300/year/country)."),
]

for title, detail in limitations:
    with st.expander(title):
        st.write(detail)

st.divider()
st.subheader(":material/science: Analytical Methods")

st.markdown("""
### Data Processing
- **Preprocessing:** salary_mid, salary_range, role_category, period_type computed in Phase 2
- **Join:** ai_jobs LEFT JOINed to country_ai_trends on (country, posted_year) → market columns prefixed with `market_`
- **Skills:** analysed independently (no job_id join)

### Statistical Analysis
- **Normality:** D'Agostino-Pearson test on salary_mid
- **Group comparisons:** Kruskal-Wallis H-test (non-parametric) at α = 0.05
- **Result:** Only experience_level shows statistically significant salary variation

### Machine Learning
- **Target:** salary_mid (regression)
- **Models:** Linear Regression (baseline + full), Random Forest, Gradient Boosting
- **Split:** 80/20 train/test, stratified on experience_level
- **Metrics:** MAE, RMSE, R²
- **Training data:** Historical only (2020–2024)

### Clustering
- **Algorithm:** K-Means (K = 2–8)
- **Features:** salary_mid, experience_numeric, remote_flag, company_size_numeric
- **Evaluation:** Silhouette Score, Davies-Bouldin Index
""")

st.divider()
st.subheader(":material/folder: Project Architecture")

st.code("""
AI-Data-Science-Job-Market-Analytics/
├── data/
│   ├── raw/archive (1)/    ← original source files (NEVER modified)
│   ├── processed/          ← cleaned + feature-engineered CSVs
│   └── exports/            ← Power BI / dashboard-ready files
├── notebooks/              ← Master Jupyter notebook (26 sections)
├── src/                    ← Python modules (data_loader, preprocessing,
│                              feature_engineering, utils)
├── dashboard/              ← THIS Streamlit app
├── web_dashboard/          ← HTML/CSS/JS dashboard
├── powerbi/                ← Power BI docs + theme
└── reports/                ← Generated reports
""", language="")
