# AI MarketLens — Streamlit Dashboard

## Run Instructions

### From the project root:
```bash
streamlit run dashboard/app.py
```

### From the dashboard/ directory:
```bash
cd dashboard
streamlit run app.py
```

The app will open at: http://localhost:8501

---

## Prerequisites

```bash
pip install -r requirements.txt
```

Required packages: `streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`

---

## Structure

```
dashboard/
├── app.py                   ← Main entry point (st.navigation)
├── .streamlit/
│   └── config.toml          ← Theme configuration
├── utils/
│   ├── data.py              ← Cached data loading functions
│   └── charts.py            ← Shared Plotly chart builders
└── app_pages/
    ├── overview.py          ← Page 1: Executive overview + KPIs
    ├── salary.py            ← Page 2: Salary intelligence
    ├── job_market.py        ← Page 3: Job market analysis
    ├── skills.py            ← Page 4: Skills intelligence
    ├── remote_work.py       ← Page 5: Remote work analysis
    ├── ml_insights.py       ← Page 6: ML models + predictions
    ├── data_explorer.py     ← Page 7: Data browsing + downloads
    └── methodology.py       ← Page 8: Methods + limitations
```

---

## Data Sources

All data loaded from `data/exports/` (Phase 2 outputs):

| File | Rows | Used For |
|---|---|---|
| powerbi_jobs.csv | 50,000 | Main analysis |
| powerbi_skills.csv | 224,605 | Skills intelligence |
| powerbi_country_trends.csv | 42 | Market trends |

---

## Key Notes

- All pages include **Historical (2020–2024)** vs **Projected (2025–2026)** segmentation.
- Skills are analysed independently — direct job-level skill join is not available.
- ML models are trained on Historical data only.
- The dataset is synthetic — ML results are educational demonstrations only.
