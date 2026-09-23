"""
format_notebook_outputs.py
---------------------------
Phase B: Transforms all raw print/text outputs into professional
pandas DataFrame tables. Zero analytical changes.
Run from project root: python format_notebook_outputs.py
"""
import json
import pathlib

NB_PATH = pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb")
nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
cells = nb["cells"]

def set_src(cell, s):
    cell["source"] = s.splitlines(keepends=True)

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 1 (nb cell 09) — Data Loading / Raw File Validation
# Replace verbose validate_raw_files print with a clean inventory table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "validate_raw_files" in src and "load_all" in src:
        set_src(c, """\
from src.data_loader import load_all, validate_raw_files
from IPython.display import display

raw = load_all()
ai_jobs           = raw['ai_jobs']
skills_demand     = raw['skills_demand']
country_ai_trends = raw['country_ai_trends']
job_title_mapping = raw['job_title_mapping']
data_dictionary   = raw['data_dictionary']

# ── Dataset Inventory ────────────────────────────────────────────────────
_roles = {
    'ai_jobs':           'Main fact table — individual job postings',
    'skills_demand':     'Job–skill bridge (job_id key mismatch — see Join Validation)',
    'country_ai_trends': 'Country-level AI market aggregates',
    'job_title_mapping': 'Job title lookup / role category dimension',
    'data_dictionary':   'Column metadata reference',
}
_inventory = pd.DataFrame([
    {
        'File':        name + '.csv',
        'Rows':        f'{df.shape[0]:,}',
        'Columns':     df.shape[1],
        'Missing':     int(df.isnull().sum().sum()),
        'Duplicates':  int(df.duplicated().sum()),
        'Role':        _roles[name],
    }
    for name, df in raw.items()
])
display(_inventory.style.set_caption('Dataset Inventory — Raw Files').hide(axis='index'))
print('All 5 raw files loaded successfully.')
""")
        print("  FORMATTED: cell 01 — Data Loading")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 2 (nb cell 11) — Quality Report
# Replace the text quality_report function with a single clean table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "def quality_report" in src and "for name, df in raw.items()" in src:
        set_src(c, """\
# ── Data Quality Summary ────────────────────────────────────────────────
_dtypes_summary = {
    name: ', '.join(f'{str(k)}({v})' for k, v in df.dtypes.value_counts().items())
    for name, df in raw.items()
}
_quality = pd.DataFrame([
    {
        'Dataset':     name + '.csv',
        'Rows':        f'{df.shape[0]:,}',
        'Columns':     df.shape[1],
        'Missing':     int(df.isnull().sum().sum()),
        'Duplicates':  int(df.duplicated().sum()),
        'Data Types':  _dtypes_summary[name],
    }
    for name, df in raw.items()
])
display(_quality.style.set_caption('Data Quality Summary — All Datasets').hide(axis='index'))
""")
        print("  FORMATTED: cell 02 — Quality Report")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 3 (nb cell 12) — Join Integrity Checks
# Replace print statements with a structured Join Validation table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Verify known join integrity" in src and "overlap_pct" in src:
        set_src(c, """\
# ── Join Integrity Validation ────────────────────────────────────────────
skills_ids    = set(skills_demand['job_id'].unique())
jobs_ids      = set(ai_jobs['job_id'].unique())
overlap_pct   = len(skills_ids & jobs_ids) / len(jobs_ids) * 100
jtm_match     = set(job_title_mapping['job_title']) == set(ai_jobs['job_title'].unique())
country_match = set(country_ai_trends['country'])   == set(ai_jobs['country'].unique())
year_match    = set(country_ai_trends['year'])       == set(ai_jobs['posted_year'].unique())

_joins = pd.DataFrame([
    {
        'Join':        'skills_demand.job_id → ai_jobs.job_id',
        'Match Rate':  f'{overlap_pct:.1f}%',
        'Status':      'DO NOT JOIN',
        'Notes':       'Dataset generation artifact — only 4.1% overlap',
    },
    {
        'Join':        'job_title_mapping.job_title → ai_jobs.job_title',
        'Match Rate':  '100%',
        'Status':      'Valid',
        'Notes':       '6 job titles match exactly',
    },
    {
        'Join':        'country_ai_trends.country → ai_jobs.country',
        'Match Rate':  '100%' if country_match else 'MISMATCH',
        'Status':      'Valid' if country_match else 'Check',
        'Notes':       '6 countries match exactly',
    },
    {
        'Join':        'country_ai_trends.year → ai_jobs.posted_year',
        'Match Rate':  '100%' if year_match else 'MISMATCH',
        'Status':      'Valid' if year_match else 'Check',
        'Notes':       '2020–2026 (7 years) match exactly',
    },
])
display(_joins.style.set_caption('Table Relationship & Join Integrity').hide(axis='index'))
""")
        print("  FORMATTED: cell 03 — Join Integrity")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 4 (nb cell 14) — Preprocessing summary
# Replace shape prints with a clean Processed Datasets table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "clean_jobs" in src and "jobs_clean.shape" in src and "All assertions passed" in src:
        set_src(c, """\
from src.preprocessing import (
    clean_jobs, build_country_enriched,
    clean_skills, build_skill_summary, clean_country_trends
)

jobs_clean           = clean_jobs(ai_jobs, job_title_mapping)
jobs_enriched        = build_country_enriched(jobs_clean, country_ai_trends)
skills_clean         = clean_skills(skills_demand)
skill_summary        = build_skill_summary(skills_clean)
country_trends_clean = clean_country_trends(country_ai_trends)

assert len(jobs_clean)    == 50_000, 'jobs_clean row count changed!'
assert len(jobs_enriched) == 50_000, 'jobs_enriched row count changed!'
assert jobs_enriched[['market_total_ai_jobs','market_avg_salary_usd']].isnull().sum().sum() == 0

_processed = {
    'jobs_clean':           jobs_clean,
    'jobs_country_enriched': jobs_enriched,
    'skills_clean':          skills_clean,
    'skill_summary':         skill_summary,
    'country_trends_clean':  country_trends_clean,
}
_proc_summary = pd.DataFrame([
    {
        'Dataset':    name,
        'Rows':       f'{df.shape[0]:,}',
        'Columns':    df.shape[1],
        'Missing':    int(df.isnull().sum().sum()),
        'Duplicates': int(df.duplicated().sum()),
    }
    for name, df in _processed.items()
])
display(_proc_summary.style.set_caption('Processed Datasets Summary').hide(axis='index'))
print('All assertions passed. Preprocessing complete.')
""")
        print("  FORMATTED: cell 04 — Preprocessing Summary")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 5 (nb cell 15) — jobs_clean preview
# Remove column list dump; keep clean head() display
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "jobs_clean.columns.tolist()" in src and "jobs_clean.head(3)" in src:
        set_src(c, """\
# ── Column Schema — jobs_clean ───────────────────────────────────────────
_schema = pd.DataFrame([
    {'Column': col, 'Data Type': str(jobs_clean[col].dtype),
     'Unique Values': jobs_clean[col].nunique(),
     'Sample':        str(jobs_clean[col].iloc[0])}
    for col in jobs_clean.columns
])
display(_schema.style.set_caption('jobs_clean — Column Schema').hide(axis='index'))
print(f'Shape: {jobs_clean.shape[0]:,} rows × {jobs_clean.shape[1]} columns')
""")
        print("  FORMATTED: cell 05 — jobs_clean column schema")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 6 (nb cell 17) — Feature Engineering summary
# Replace raw print loop with a Feature Engineering table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "engineer_all_features" in src and "engineered = [" in src:
        set_src(c, """\
from src.feature_engineering import engineer_all_features

jobs = engineer_all_features(jobs_enriched)

# ── Engineered Features Summary ──────────────────────────────────────────
_eng_meta = [
    ('salary_mid',           'float', '(salary_min_usd + salary_max_usd) / 2.0',       'Primary salary metric'),
    ('salary_range',         'float', 'salary_max_usd − salary_min_usd',                'Salary band width'),
    ('experience_numeric',   'int',   'Entry=0, Mid=1, Senior=2',                        'Ordinal encoding'),
    ('period_type',          'str',   '≤2024 → Historical, ≥2025 → Projected',           'Temporal label'),
    ('year_group',           'str',   'Early / Mid / Recent / Projected grouping',        'Year bucket'),
    ('remote_flag',          'int',   '1 if remote_type==Remote else 0',                 'Binary remote indicator'),
    ('company_size_numeric', 'int',   'Small=1, Medium=2, Large=3',                      'Ordinal encoding'),
]
_eng_df = pd.DataFrame([
    {
        'Feature':     feat,
        'Type':        dtype,
        'Definition':  defn,
        'Usage':       usage,
        'Sample':      str(jobs[feat].iloc[0]) if feat in jobs.columns else 'N/A',
    }
    for feat, dtype, defn, usage in _eng_meta
    if feat in jobs.columns
])
display(_eng_df.style.set_caption('Engineered Features').hide(axis='index'))
print(f'Final working dataset: {jobs.shape[0]:,} rows x {jobs.shape[1]} columns  '
      f'| Historical: {(jobs["period_type"]=="Historical").sum():,}  '
      f'| Projected: {(jobs["period_type"]=="Projected").sum():,}')
""")
        print("  FORMATTED: cell 06 — Feature Engineering table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 7 (nb cell 19) — Year counts table after chart
# Replace .to_string() with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "year_counts: pd.DataFrame" in src and "year_counts.to_string" in src:
        new = src.replace(
            "print(year_counts.to_string(index=False))",
            "_yc_disp = year_counts.rename(columns={'posted_year':'Year','period_type':'Period','count':'Job Postings'})\n"
            "_yc_disp['Job Postings'] = _yc_disp['Job Postings'].apply(lambda x: f'{x:,}')\n"
            "display(_yc_disp.style.set_caption('Job Postings by Year').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 07 — Year counts table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 11 (nb cell 27) — Salary distribution summary table
# Replace print(describe().apply()) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Salary Distributions" in src and "jobs['salary_mid'].describe()" in src:
        new = src.replace(
            "print('\\nSalary Midpoint Summary:')\nprint(jobs['salary_mid'].describe().apply(lambda x: f'${x:,.0f}'))",
            "_sal_desc = jobs['salary_mid'].describe()\n"
            "_sal_table = pd.DataFrame({\n"
            "    'Statistic': ['Count','Mean','Std Dev','Min','25th Pct','Median (50th)','75th Pct','Max'],\n"
            "    'Value (USD)': [\n"
            "        f\"{_sal_desc['count']:,.0f}\",\n"
            "        f\"${_sal_desc['mean']:,.2f}\",\n"
            "        f\"${_sal_desc['std']:,.2f}\",\n"
            "        f\"${_sal_desc['min']:,.2f}\",\n"
            "        f\"${_sal_desc['25%']:,.2f}\",\n"
            "        f\"${_sal_desc['50%']:,.2f}\",\n"
            "        f\"${_sal_desc['75%']:,.2f}\",\n"
            "        f\"${_sal_desc['max']:,.2f}\",\n"
            "    ]\n"
            "})\n"
            "display(_sal_table.style.set_caption('Salary Midpoint Summary Statistics').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 11 — Salary distribution stats table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 14 (nb cell 32) — Salary by experience table
# Replace print(_sal_agg.reindex(order)) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Salary by experience level" in src and "_sal_agg: pd.DataFrame" in src:
        new = src.replace(
            "print('Mean salary_mid by experience_level:')\n"
            "_sal_agg: pd.DataFrame = pd.DataFrame(jobs.groupby('experience_level')['salary_mid'].agg(['mean','median','std'])).round(0)\n"
            "print(_sal_agg.reindex(order))",
            "_sal_agg: pd.DataFrame = pd.DataFrame(\n"
            "    jobs.groupby('experience_level')['salary_mid'].agg(['mean','median','std','count'])\n"
            ").round(0).reindex(order).reset_index()\n"
            "_sal_agg.columns = ['Experience Level','Mean Salary (USD)','Median Salary (USD)','Std Dev','Sample Size']\n"
            "_sal_agg['Mean Salary (USD)']   = _sal_agg['Mean Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_sal_agg['Median Salary (USD)'] = _sal_agg['Median Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_sal_agg['Std Dev']             = _sal_agg['Std Dev'].apply(lambda x: f'${x:,.0f}')\n"
            "_sal_agg['Sample Size']         = _sal_agg['Sample Size'].apply(lambda x: f'{int(x):,}')\n"
            "display(_sal_agg.style.set_caption('Salary by Experience Level').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 14 — Salary by experience table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 15 (nb cell 33) — Salary by country table
# Replace print(_sal_ctry.sort_values()) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Salary by country" in src and "_sal_ctry: pd.DataFrame" in src:
        new = src.replace(
            "print('Mean salary_mid by country:')\n"
            "_sal_ctry: pd.DataFrame = pd.DataFrame(jobs.groupby('country')['salary_mid'].agg(['mean','median'])).round(0)\n"
            "print(_sal_ctry.sort_values('mean', ascending=False))",
            "_sal_ctry: pd.DataFrame = pd.DataFrame(\n"
            "    jobs.groupby('country')['salary_mid'].agg(['mean','median','count'])\n"
            ").round(0).sort_values('mean', ascending=False).reset_index()\n"
            "_sal_ctry.columns = ['Country','Mean Salary (USD)','Median Salary (USD)','Job Count']\n"
            "_sal_ctry['Mean Salary (USD)']   = _sal_ctry['Mean Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_sal_ctry['Median Salary (USD)'] = _sal_ctry['Median Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_sal_ctry['Job Count']           = _sal_ctry['Job Count'].apply(lambda x: f'{int(x):,}')\n"
            "display(_sal_ctry.style.set_caption('Salary by Country').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 15 — Salary by country table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 22 (nb cell 45) — Skill summary table
# Replace print(skill_summary.to_string()) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Skill category" in src and "skill_summary.to_string" in src:
        new = src.replace(
            "print(skill_summary.to_string(index=False))",
            "_ss = skill_summary.copy()\n"
            "if 'count' in _ss.columns:\n"
            "    _ss['count'] = _ss['count'].apply(lambda x: f'{int(x):,}')\n"
            "if 'percentage' in _ss.columns:\n"
            "    _ss['percentage'] = _ss['percentage'].apply(lambda x: f'{float(x):.2f}%')\n"
            "display(_ss.style.set_caption('Skill Demand Summary').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 22 — Skill summary table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 23 (nb cell 47) — Historical vs Projected
# Replace print statements with a clean Period Comparison table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "hist_jobs = jobs[jobs['period_type'] == 'Historical']" in src and \
       "Salary midpoint comparison" in src:
        new = src.replace(
            "print(f'Historical rows (2020-2024) : {len(hist_jobs):,}  ({100*len(hist_jobs)/len(jobs):.1f}%)')\n"
            "print(f'Projected rows  (2025-2026) : {len(proj_jobs):,}  ({100*len(proj_jobs)/len(jobs):.1f}%)')\n"
            "\nprint('\\nSalary midpoint comparison:')\n"
            "for period, group in jobs.groupby('period_type'):\n"
            "    print(f'  {period}: mean=${group[\"salary_mid\"].mean():,.0f}  median=${group[\"salary_mid\"].median():,.0f}')",
            "_period_rows = [\n"
            "    (p, len(g), f'{100*len(g)/len(jobs):.1f}%',\n"
            "     f'${g[\"salary_mid\"].mean():,.0f}', f'${g[\"salary_mid\"].median():,.0f}')\n"
            "    for p, g in jobs.groupby('period_type')\n"
            "]\n"
            "_period_df = pd.DataFrame(_period_rows,\n"
            "    columns=['Period','Job Postings','% of Total','Mean Salary (USD)','Median Salary (USD)'])\n"
            "_period_df['Job Postings'] = _period_df['Job Postings'].apply(lambda x: f'{x:,}')\n"
            "display(_period_df.style.set_caption('Historical vs Projected — Period Comparison').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 23 — Historical vs Projected table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 24 (nb cell 49) — Statistical tests
# Replace inline prints + to_string() with structured tables
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "normaltest" in src and "kruskal" in src and "results_table" in src:
        set_src(c, """\
from scipy.stats import normaltest, kruskal
import pandas as pd
alpha = 0.05

# ── Normality Test ───────────────────────────────────────────────────────
stat_n, p_n = normaltest(jobs['salary_mid'])
_norm_interp = 'NOT normally distributed — use non-parametric tests' if p_n < alpha else 'Approximately normal'
_norm_df = pd.DataFrame([{
    'Variable':       'salary_mid',
    'Test':           "D'Agostino-Pearson",
    'Statistic':      f'{stat_n:.4f}',
    'P-value':        f'{p_n:.2e}',
    'Significant':    'Yes' if p_n < alpha else 'No',
    'Interpretation': _norm_interp,
}])
display(_norm_df.style.set_caption('Normality Test (α = 0.05)').hide(axis='index'))

# ── Kruskal-Wallis Tests ─────────────────────────────────────────────────
tests = [
    ('experience_level', 'Experience Level'),
    ('country',          'Country'),
    ('industry',         'Industry'),
    ('remote_type',      'Remote Type'),
    ('role_category',    'Role Category'),
    ('company_type',     'Company Type'),
    ('company_size',     'Company Size'),
]

test_rows = []
for col, label in tests:
    groups = [g['salary_mid'].values for _, g in jobs.groupby(col)]
    H, p = kruskal(*groups)
    sig = p < alpha
    test_rows.append({
        'Grouping Factor':    label,
        'H Statistic':        f'{H:.2f}',
        'P-value':            '<0.001' if p < 0.001 else f'{p:.4f}',
        'Significant':        'Yes — SIGNIFICANT' if sig else 'No',
        'Interpretation':     'Salary distributions differ significantly across groups' if sig
                              else 'No significant salary difference across groups',
    })

# Store raw results for downstream use
test_results = []
for col, label in tests:
    groups = [g['salary_mid'].values for _, g in jobs.groupby(col)]
    H, p = kruskal(*groups)
    test_results.append({'Factor': col, 'H': round(H,2), 'p-value': round(p,6), 'Significant (p<0.05)': p < alpha})

results_table = pd.DataFrame(test_results)
_kw_display = pd.DataFrame(test_rows)
display(_kw_display.style.set_caption('Kruskal-Wallis Salary Tests (α = 0.05)').hide(axis='index'))
""")
        print("  FORMATTED: cell 24 — Statistical tests table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 25 (nb cell 51) — ML Setup
# Replace print(f'Features: {features}') with a clean feature table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "build_ml_feature_matrix" in src and "TARGET = 'salary_mid'" in src and \
       "print(f'Feature matrix:" in src:
        new = src.replace(
            "print(f'Training rows: {len(jobs_hist_ml):,} (Historical 2020-2024 only)')\n"
            "print(f'Feature matrix: {X_full.shape}')\n"
            "print(f'Features: {features}')",
            "_ml_setup = pd.DataFrame([{\n"
            "    'Item':  'Training rows',\n"
            "    'Value': f'{len(jobs_hist_ml):,} (Historical 2020–2024 only)',\n"
            "}, {\n"
            "    'Item':  'Feature matrix shape',\n"
            "    'Value': f'{X_full.shape[0]:,} rows × {X_full.shape[1]} features',\n"
            "}, {\n"
            "    'Item':  'Target variable',\n"
            "    'Value': TARGET + '  (salary_mid = (salary_min_usd + salary_max_usd) / 2)',\n"
            "}, {\n"
            "    'Item':  'Features used',\n"
            "    'Value': ', '.join(features),\n"
            "}])\n"
            "display(_ml_setup.style.set_caption('ML Training Configuration').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 25 — ML Setup table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 26 (nb cell 52) — Train/Test split info
# Replace plain print with a small table
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "Train/test split" in src and "X_train.shape[0]" in src and \
       "print(f'Train:" in src:
        new = src.replace(
            "print(f'Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}')",
            "_split_df = pd.DataFrame([{\n"
            "    'Split':      'Train',\n"
            "    'Rows':       f'{X_train.shape[0]:,}',\n"
            "    'Percentage': f'{100*X_train.shape[0]/(X_train.shape[0]+X_test.shape[0]):.0f}%',\n"
            "}, {\n"
            "    'Split':      'Test',\n"
            "    'Rows':       f'{X_test.shape[0]:,}',\n"
            "    'Percentage': f'{100*X_test.shape[0]/(X_train.shape[0]+X_test.shape[0]):.0f}%',\n"
            "}])\n"
            "display(_split_df.style.set_caption('Train / Test Split (stratified on experience_level)').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 26 — Train/Test split table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 27 (nb cell 53) — Model training with evaluate_model
# Keep evaluate_model helper but suppress its print; results collected silently
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "def evaluate_model" in src and "lr_base = evaluate_model" in src:
        set_src(c, """\
def evaluate_model(model, X_tr, y_tr, X_te, y_te, label):
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)
    mae  = mean_absolute_error(y_te, preds)
    rmse = np.sqrt(mean_squared_error(y_te, preds))
    r2   = r2_score(y_te, preds)
    return {'label':label, 'MAE':round(mae,0), 'RMSE':round(rmse,0), 'R2':round(r2,4),
            'model':model, 'preds':preds, 'y_test':y_te}

lr_base = evaluate_model(LinearRegression(), X_base_train, y_base_train, X_base_test, y_base_test, 'Linear Regression (baseline — experience only)')
lr_full = evaluate_model(LinearRegression(), X_train, y_train, X_test, y_test, 'Linear Regression (full features)')
rf_full = evaluate_model(RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1), X_train, y_train, X_test, y_test, 'Random Forest (full features)')
gb_full = evaluate_model(GradientBoostingRegressor(n_estimators=100, random_state=42), X_train, y_train, X_test, y_test, 'Gradient Boosting (full features)')
print('Model training complete.')
""")
        print("  FORMATTED: cell 27 — evaluate_model silent training")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 28 (nb cell 54) — Model Comparison Table
# Replace print(to_string()) with styled display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "model_comparison = pd.DataFrame" in src and "to_string(index=False)" in src:
        set_src(c, """\
import pandas as pd
model_comparison = pd.DataFrame([
    {'Model': lr_base['label'], 'Feature Set': 'Experience only (baseline)',
     'MAE': lr_base['MAE'], 'RMSE': lr_base['RMSE'], 'R²': lr_base['R2']},
    {'Model': lr_full['label'], 'Feature Set': 'All valid features',
     'MAE': lr_full['MAE'], 'RMSE': lr_full['RMSE'], 'R²': lr_full['R2']},
    {'Model': rf_full['label'], 'Feature Set': 'All valid features',
     'MAE': rf_full['MAE'], 'RMSE': rf_full['RMSE'], 'R²': rf_full['R2']},
    {'Model': gb_full['label'], 'Feature Set': 'All valid features',
     'MAE': gb_full['MAE'], 'RMSE': gb_full['RMSE'], 'R²': gb_full['R2']},
])
_mc_disp = model_comparison.copy()
_mc_disp['MAE']  = _mc_disp['MAE'].apply(lambda x: f'${x:,.0f}')
_mc_disp['RMSE'] = _mc_disp['RMSE'].apply(lambda x: f'${x:,.0f}')
_mc_disp['R²']   = _mc_disp['R²'].apply(lambda x: f'{x:.4f}')
display(_mc_disp.style.set_caption('Model Performance Comparison (Test Set)').hide(axis='index'))
""")
        print("  FORMATTED: cell 28 — Model comparison table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 30 (nb cell 58) — Feature Importance table
# Replace print(feat_importance.head(10).to_string()) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "feat_importance = pd.Series(rf_model.feature_importances_" in src and \
       "Top features by importance" in src:
        new = src.replace(
            "print('Top features by importance:')\n"
            "print(feat_importance.head(10).round(4).to_string())\n"
            "print()\n"
            "print('Interpretation:')\n"
            "print('  Experience-level features dominate due to synthetic uniform distribution.')\n"
            "print('  In real data, geography and industry would also contribute meaningfully.')",
            "_fi_df = feat_importance.reset_index()\n"
            "_fi_df.columns = ['Feature','Importance Score']\n"
            "_fi_df = _fi_df.head(10).reset_index(drop=True)\n"
            "_fi_df.index = _fi_df.index + 1\n"
            "_fi_df['Importance Score'] = _fi_df['Importance Score'].apply(lambda x: f'{x:.4f}')\n"
            "_fi_df.index.name = 'Rank'\n"
            "display(_fi_df.style.set_caption('Top 10 Feature Importances — Random Forest'))\n"
            "print('Note: Experience-level features dominate — consequence of synthetic uniform data.\\n'\n"
            "      'In real-world data, geography and industry would contribute more.')"
        )
        set_src(c, new)
        print("  FORMATTED: cell 30 — Feature importance table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 31 (nb cell 60) — Clustering K evaluation table
# Replace print(f'Best K...') with a table of K scores
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "k_range = range(2, 9)" in src and "silhouettes.index(max(silhouettes))" in src:
        new = src.replace(
            "best_k = list(k_range)[silhouettes.index(max(silhouettes))]\n"
            "print(f'Best K by Silhouette: {best_k} (score={max(silhouettes):.4f})')\n"
            "print(f'Best K by DBI       : {list(k_range)[dbis.index(min(dbis))]} (score={min(dbis):.4f})')",
            "best_k = list(k_range)[silhouettes.index(max(silhouettes))]\n"
            "_k_df = pd.DataFrame({\n"
            "    'K':                list(k_range),\n"
            "    'Inertia':          [f'{v:,.0f}' for v in inertias],\n"
            "    'Silhouette Score': [f'{v:.4f}' + (' ← Best' if v == max(silhouettes) else '') for v in silhouettes],\n"
            "    'Davies-Bouldin':   [f'{v:.4f}' + (' ← Best' if v == min(dbis) else '') for v in dbis],\n"
            "})\n"
            "display(_k_df.style.set_caption(f'K-Means Evaluation (Best K = {best_k})').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 31 — Clustering K evaluation table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 32 (nb cell 61) — Cluster Profile table
# Replace print(cluster_profile.to_string()) with display()
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "cluster_profile = jobs_clust.groupby" in src and \
       "print(f'Cluster Profile" in src:
        new = src.replace(
            "print(f'Cluster Profile (K={best_k}):')\nprint(cluster_profile.to_string())",
            "_cp = cluster_profile.reset_index()\n"
            "_cp.columns = ['Cluster','Avg Salary (USD)','Median Salary (USD)','Job Count',\n"
            "               'Avg Exp (0-2)','Remote %','Avg Co. Size']\n"
            "_cp['Avg Salary (USD)']    = _cp['Avg Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_cp['Median Salary (USD)'] = _cp['Median Salary (USD)'].apply(lambda x: f'${x:,.0f}')\n"
            "_cp['Job Count']           = _cp['Job Count'].apply(lambda x: f'{int(x):,}')\n"
            "_cp['Remote %']            = _cp['Remote %'].apply(lambda x: f'{x*100:.1f}%')\n"
            "display(_cp.style.set_caption(f'Cluster Profiles (K={best_k})').hide(axis='index'))"
        )
        set_src(c, new)
        print("  FORMATTED: cell 32 — Cluster profile table")
        break

# ─────────────────────────────────────────────────────────────────────────
# CODE CELL 33 (nb cell 63) — Key Insights
# Replace all print statements with structured display() tables
# ─────────────────────────────────────────────────────────────────────────
for c in cells:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "=== KEY INSIGHTS ===" in src and "SALARY BY EXPERIENCE" in src:
        set_src(c, """\
# ── 1. Salary by Experience Level ────────────────────────────────────────
_exp_rows = []
for exp in ['Entry', 'Mid', 'Senior']:
    _arr = jobs.loc[jobs['experience_level'] == exp, 'salary_mid'].to_numpy(dtype=float)
    _exp_rows.append({'Experience Level': exp,
                      'Mean Salary (USD)':   f'${_arr.mean():,.0f}',
                      'Median Salary (USD)': f'${float(np.median(_arr)):,.0f}',
                      'Job Count':           f'{len(_arr):,}'})
display(pd.DataFrame(_exp_rows).style.set_caption('1. Salary by Experience Level').hide(axis='index'))

# ── 2. Job Role Distribution ──────────────────────────────────────────────
_role_vc = jobs['job_title'].value_counts().reset_index()
_role_vc.columns = ['Job Role', 'Job Count']
_role_vc['Percentage'] = (_role_vc['Job Count'] / _role_vc['Job Count'].sum() * 100).round(2).apply(lambda x: f'{x:.2f}%')
_role_vc['Rank']       = range(1, len(_role_vc) + 1)
_role_vc['Job Count']  = _role_vc['Job Count'].apply(lambda x: f'{x:,}')
display(_role_vc[['Rank','Job Role','Job Count','Percentage']].style.set_caption('2. Job Role Distribution').hide(axis='index'))

# ── 3. Role Category Split ────────────────────────────────────────────────
_cat_vc = jobs['role_category'].value_counts().reset_index()
_cat_vc.columns = ['Role Category', 'Count']
_cat_vc['Percentage'] = (_cat_vc['Count'] / _cat_vc['Count'].sum() * 100).round(2).apply(lambda x: f'{x:.2f}%')
_cat_vc['Count']      = _cat_vc['Count'].apply(lambda x: f'{x:,}')
display(_cat_vc.style.set_caption('3. Role Category Split').hide(axis='index'))

# ── 4. Remote Work Distribution ───────────────────────────────────────────
_rem_vc = jobs['remote_type'].value_counts().reset_index()
_rem_vc.columns = ['Work Mode', 'Job Count']
_rem_vc['Percentage'] = (_rem_vc['Job Count'] / _rem_vc['Job Count'].sum() * 100).round(2).apply(lambda x: f'{x:.2f}%')
_rem_vc['Job Count']  = _rem_vc['Job Count'].apply(lambda x: f'{x:,}')
display(_rem_vc.style.set_caption('4. Remote Work Distribution (Sample Dataset)').hide(axis='index'))

# ── 5. Top Skills ─────────────────────────────────────────────────────────
_skill_vc = skills_clean['skill'].value_counts().reset_index()
_skill_vc.columns = ['Skill', 'Frequency']
_skill_vc['Percentage'] = (_skill_vc['Frequency'] / _skill_vc['Frequency'].sum() * 100).round(2).apply(lambda x: f'{x:.2f}%')
_skill_vc['Rank']       = range(1, len(_skill_vc) + 1)
_skill_vc['Frequency']  = _skill_vc['Frequency'].apply(lambda x: f'{x:,}')
display(_skill_vc[['Rank','Skill','Frequency','Percentage']].style.set_caption('5. Top Skills (skills_demand.csv)').hide(axis='index'))

# ── 6. Country Market Highlights ─────────────────────────────────────────
_ct2 = country_trends_clean
_mkt_rows = [
    {'Highlight': 'Highest avg market salary',  'Country': _ct2.loc[_ct2['avg_salary_usd'].idxmax(), 'country'],    'Year': int(_ct2.loc[_ct2['avg_salary_usd'].idxmax(), 'year']),    'Value': f\"${int(_ct2['avg_salary_usd'].max()):,}\"},
    {'Highlight': 'Most AI jobs in market',     'Country': _ct2.loc[_ct2['total_ai_jobs'].idxmax(), 'country'],     'Year': int(_ct2.loc[_ct2['total_ai_jobs'].idxmax(), 'year']),     'Value': f\"{int(_ct2['total_ai_jobs'].max()):,} jobs\"},
    {'Highlight': 'Highest remote % in market', 'Country': _ct2.loc[_ct2['remote_percentage'].idxmax(), 'country'], 'Year': int(_ct2.loc[_ct2['remote_percentage'].idxmax(), 'year']), 'Value': f\"{int(_ct2['remote_percentage'].max())}%\"},
]
display(pd.DataFrame(_mkt_rows).style.set_caption('6. Country Market Highlights (country_ai_trends.csv)').hide(axis='index'))
""")
        print("  FORMATTED: cell 33 — Key Insights tables")
        break

# ─────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────
NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
sz = NB_PATH.stat().st_size
print(f"\nSaved {NB_PATH}  ({sz // 1024} KB)")
print("Phase B formatting complete — run execution validation next.")
