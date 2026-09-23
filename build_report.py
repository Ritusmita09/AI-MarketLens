"""
build_report.py
---------------
Generates the internship project report as a .docx file.
Run from project root: python build_report.py
"""
import json
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

# Load canonical KPIs
kpis_path = Path("reports/canonical_kpis.json")
KPIS = json.loads(kpis_path.read_text(encoding="utf-8"))
S = KPIS["salary"]
J = KPIS["job_counts"]
D = KPIS["dimensions"]
M = KPIS["market_level"]

# ─────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────

def add_page_number(doc):
    """Add page numbers to footer."""
    section = doc.sections[0]
    footer  = section.footer
    para    = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def add_header_text(doc, text):
    section = doc.sections[0]
    header  = section.header
    para    = header.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = para.add_run(text)
    run.font.size  = Pt(9)
    run.font.color.rgb = RGBColor(0x57, 0x60, 0x6A)


def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)


def styled_table(doc, headers, rows, col_widths=None):
    """Build a styled table with header row."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].bold = True
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_bg(hdr_cells[i], 'D6E4FF')
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            row_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    if col_widths:
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                cell.width = Inches(col_widths[i])
    return table


# ─────────────────────────────────────────────────────────────
# Build document
# ─────────────────────────────────────────────────────────────

doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(2.8)
    section.right_margin  = Cm(2.5)

add_page_number(doc)
add_header_text(doc, "AI MarketLens — IBM SkillsBuild Internship Project")

# ──────────────────────────────────────────────────────────────
# COVER PAGE
# ──────────────────────────────────────────────────────────────
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("AI MarketLens")
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = sub.add_run("AI-Powered Global Data Science & AI Job Market Intelligence Platform")
run2.font.size = Pt(16)
run2.font.color.rgb = RGBColor(0x3B, 0x82, 0xF6)

doc.add_paragraph()
doc.add_paragraph()

for line in [
    "Academic Internship Project Report",
    "",
    "IBM SkillsBuild Data Analytics with AI Internship",
    "BharatCares × AICTE × IBM",
    "",
    "Submitted by:",
    "Ritusmita Dutta",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line)
    if line in ("Ritusmita Dutta", "Academic Internship Project Report"):
        r.bold = True
        r.font.size = Pt(14)
    elif line.startswith("IBM SkillsBuild"):
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x57, 0x60, 0x6A)
    else:
        r.font.size = Pt(12)

doc.add_page_break()

# ──────────────────────────────────────────────────────────────
# 1. EXECUTIVE SUMMARY
# ──────────────────────────────────────────────────────────────
doc.add_heading("1. Executive Summary", level=1)

doc.add_paragraph(
    "AI MarketLens is an end-to-end academic data analytics and machine learning project "
    "that examines a synthetic global dataset of AI and Data Science job postings. "
    "The project analyses 50,000 job records across 6 countries, 6 job titles, and 7 years "
    "(2020–2026), supplemented by a 224,605-row skills dataset and a 42-row country-level "
    "market aggregate table."
)
doc.add_paragraph(
    "The dataset is synthetically generated, which produces near-uniform distributions "
    "across all categorical dimensions. This is a fundamental dataset characteristic that "
    "limits real-world generalisation but provides an excellent structured environment for "
    "demonstrating a full analytics and ML pipeline."
)
doc.add_paragraph(
    "Key analytical findings include: (1) salary varies significantly only with "
    f"experience_level (Entry: ${S['entry_avg_salary']:,.0f} vs Senior: "
    f"${S['senior_avg_salary']:,.0f}, ratio {S['senior_entry_ratio']:.2f}×); "
    f"(2) {D['remote_job_pct']}% of postings are fully remote; "
    "(3) all other categorical factors produce negligible salary differences — a direct "
    "consequence of synthetic data generation. "
    "Statistical testing (Kruskal-Wallis, α=0.05) confirms that experience_level "
    "is the only statistically significant salary predictor."
)
doc.add_paragraph(
    "Three interactive dashboards were delivered: a Power BI documentation package "
    "(5 pages), an 8-page Streamlit application, and a standalone HTML/CSS/JavaScript "
    "dashboard. The master Jupyter notebook covers all 26 analytical sections."
)

# ──────────────────────────────────────────────────────────────
# 2. INTRODUCTION
# ──────────────────────────────────────────────────────────────
doc.add_heading("2. Introduction", level=1)
doc.add_paragraph(
    "The global AI and data science employment landscape is growing rapidly. "
    "Organisations require data-driven insights into salary benchmarks, in-demand skills, "
    "remote-work adoption, and geographic hiring patterns. This project simulates a "
    "market intelligence platform that provides such insights through structured analytics."
)
doc.add_paragraph(
    "All conclusions are framed specifically around the supplied synthetic dataset. "
    "No claims are made about the real global labour market that are not supported "
    "by the data."
)

# ──────────────────────────────────────────────────────────────
# 3. PROBLEM STATEMENT
# ──────────────────────────────────────────────────────────────
doc.add_heading("3. Problem Statement", level=1)
doc.add_paragraph(
    "Given a multi-table synthetic job market dataset, the analytical problem is to:"
)
for item in [
    "Identify the primary drivers of salary variation across job market dimensions.",
    "Quantify remote work adoption patterns over time and across geographies.",
    "Determine which skills are most demanded in the AI/Data Science job market.",
    "Build and evaluate salary regression models to demonstrate ML pipeline best practices.",
    "Discover natural job profile segments through unsupervised clustering.",
    "Deliver the findings through interactive dashboards accessible to non-technical stakeholders.",
]:
    p = doc.add_paragraph(item, style='List Bullet')

# ──────────────────────────────────────────────────────────────
# 4. OBJECTIVES
# ──────────────────────────────────────────────────────────────
doc.add_heading("4. Objectives", level=1)
objectives = [
    "Perform a rigorous exploratory data analysis across all five dataset tables.",
    "Engineer meaningful derived features (salary_mid, role_category, period_type, etc.).",
    "Conduct statistical hypothesis testing on salary determinants using Kruskal-Wallis.",
    "Compare salary regression models: baseline, Linear Regression, Random Forest, Gradient Boosting.",
    "Apply K-Means clustering to discover job profile segments.",
    "Produce clean, dashboard-ready processed datasets.",
    "Deliver Power BI documentation, Streamlit app, and HTML/JS dashboard.",
    "Package the project for academic internship submission.",
]
for obj in objectives:
    doc.add_paragraph(obj, style='List Number')

# ──────────────────────────────────────────────────────────────
# 5. DATASET DESCRIPTION
# ──────────────────────────────────────────────────────────────
doc.add_heading("5. Dataset Description", level=1)
doc.add_paragraph(
    "The dataset consists of five CSV files supplied as a Kaggle dataset. "
    "All files are located at data/raw/archive (1)/ and are never modified."
)

styled_table(doc,
    ["File", "Rows", "Columns", "Role"],
    [
        ["ai_jobs.csv",           "50,000",  "14", "Main fact table — individual job postings"],
        ["skills_demand.csv",     "224,605", "4",  "Job–skill bridge (job_id key mismatch — see §6)"],
        ["country_ai_trends.csv", "42",      "6",  "Country-level market aggregate statistics"],
        ["job_title_mapping.csv", "6",       "3",  "Job title lookup / role category dimension"],
        ["data_dictionary.csv",   "13",      "3",  "Column metadata"],
    ],
    col_widths=[1.8, 0.8, 0.7, 3.0]
)

doc.add_paragraph()
doc.add_heading("5.1 ai_jobs.csv — Key Columns", level=2)
styled_table(doc,
    ["Column", "Type", "Description"],
    [
        ["job_id",               "str",   "Unique 12-char job identifier (PK)"],
        ["job_title",            "str",   "6 job titles"],
        ["company_type",         "str",   "Startup / MNC / Research Lab"],
        ["industry",             "str",   "Tech / Healthcare / Retail / Finance / Education"],
        ["country",              "str",   "6 countries"],
        ["city",                 "str",   "City or 'Remote'"],
        ["remote_type",          "str",   "Remote / Hybrid / Onsite"],
        ["experience_level",     "str",   "Entry / Mid / Senior"],
        ["min_experience_years", "int",   "0/2/5 — redundant with experience_level"],
        ["salary_min_usd",       "int",   "Min annual salary (USD)"],
        ["salary_max_usd",       "int",   "Max annual salary (USD)"],
        ["employment_type",      "str",   "All Full-time — zero variance, EXCLUDED"],
        ["posted_year",          "int",   "2020–2026"],
        ["company_size",         "str",   "Small / Medium / Large"],
    ],
    col_widths=[1.9, 0.8, 3.6]
)

doc.add_paragraph()
doc.add_heading("5.2 Table Relationships", level=2)
doc.add_paragraph(
    "Three valid relationships were confirmed during the Phase 1 audit:"
)
styled_table(doc,
    ["From", "To", "Join Key", "Match Rate"],
    [
        ["ai_jobs.job_title",             "job_title_mapping.job_title",        "job_title",        "100%"],
        ["ai_jobs.(country+posted_year)", "country_ai_trends.(country+year)",   "country + year",   "100%"],
        ["skills_demand.job_id",          "ai_jobs.job_id",                     "job_id",           "4.1% — BROKEN"],
    ],
    col_widths=[1.8, 2.0, 1.5, 1.3]
)

# ──────────────────────────────────────────────────────────────
# 6. DATA QUALITY AND PREPROCESSING
# ──────────────────────────────────────────────────────────────
doc.add_heading("6. Data Quality and Preprocessing", level=1)

doc.add_heading("6.1 Data Quality Findings", level=2)
styled_table(doc,
    ["Finding", "Severity", "Resolution"],
    [
        ["Zero missing values across all 5 files",   "None",     "No action required"],
        ["Zero duplicate rows across all 5 files",   "None",     "No action required"],
        ["employment_type: all 'Full-time'",          "Medium",   "Column dropped from all analyses"],
        ["skills_demand job_id mismatch (4.1%)",      "Critical", "Skills analysed independently; no join performed"],
        ["posted_year 2025–2026 (28.4% of rows)",     "Medium",   "Labelled 'Projected'; separated from Historical"],
        ["Near-uniform category distributions",       "Critical", "Documented as synthetic data characteristic"],
        ["min_experience_years redundant",            "Medium",   "Excluded from ML when experience_level present"],
        ["city='Remote' overlaps remote_type='Remote'","Low",     "Noted; city excluded from remote-type prediction"],
    ],
    col_widths=[2.8, 1.0, 2.8]
)

doc.add_heading("6.2 Feature Engineering", level=2)
styled_table(doc,
    ["Feature", "Definition", "Usage"],
    [
        ["salary_mid",           "(salary_min_usd + salary_max_usd) / 2.0",       "Primary salary metric — all analyses"],
        ["salary_range",         "salary_max_usd − salary_min_usd",                "Salary band width"],
        ["role_category",        "Joined from job_title_mapping (Analytics/Eng.)", "Role segmentation"],
        ["period_type",          "Historical if year≤2024 else Projected",          "Temporal separation"],
        ["experience_numeric",   "Entry=0, Mid=1, Senior=2",                        "Ordinal encoding for clustering/ML"],
        ["remote_flag",          "1 if remote_type=='Remote' else 0",               "Binary remote feature"],
        ["company_size_numeric", "Small=1, Medium=2, Large=3",                      "Ordinal encoding"],
        ["market_* columns",     "Joined from country_ai_trends (LEFT JOIN)",        "Market-level context"],
    ],
    col_widths=[1.8, 2.5, 2.3]
)

# ──────────────────────────────────────────────────────────────
# 7. EXPLORATORY DATA ANALYSIS
# ──────────────────────────────────────────────────────────────
doc.add_heading("7. Exploratory Data Analysis", level=1)

doc.add_paragraph(
    "The master notebook (AI_MarketLens_Master.ipynb) performs EDA across 26 sections. "
    "The following summarises the most important findings."
)

doc.add_heading("7.1 Job Distribution", level=2)
doc.add_paragraph(
    f"The dataset contains {J['total_job_postings']:,} job postings. "
    f"{J['historical_jobs']:,} are Historical (2020–2024) and "
    f"{J['projected_jobs']:,} are Projected (2025–2026). "
    "All 7 years contain approximately 7,000–7,300 postings, consistent with synthetic uniform generation."
)

doc.add_heading("7.2 Salary Distribution", level=2)
styled_table(doc,
    ["Statistic", "Value"],
    [
        ["Definition",             "salary_mid = (salary_min_usd + salary_max_usd) / 2.0"],
        ["Mean salary_mid",        f"${S['mean_salary_mid']:,.2f}"],
        ["Median salary_mid",      f"${S['median_salary_mid']:,.2f}"],
        ["Min salary_mid",         f"${S['min_salary_mid']:,.2f}"],
        ["Max salary_mid",         f"${S['max_salary_mid']:,.2f}"],
        ["Min salary_min_usd",     f"${S['min_salary_min_usd']:,}"],
        ["Max salary_max_usd",     f"${S['max_salary_max_usd']:,}"],
        ["Entry avg salary_mid",   f"${S['entry_avg_salary']:,.2f}"],
        ["Mid avg salary_mid",     f"${S['mid_avg_salary']:,.2f}"],
        ["Senior avg salary_mid",  f"${S['senior_avg_salary']:,.2f}"],
        ["Senior / Entry ratio",   f"{S['senior_entry_ratio']:.4f}×"],
    ],
    col_widths=[2.5, 3.5]
)

doc.add_heading("7.3 Remote Work", level=2)
doc.add_paragraph(
    f"{D['remote_job_pct']}% of job postings are fully remote. "
    "Hybrid and Onsite account for approximately 34% and 33% respectively. "
    "Remote adoption is nearly uniform across countries, industries, and experience levels — "
    "consistent with synthetic data generation."
)

doc.add_heading("7.4 Country and Market Trends", level=2)
doc.add_paragraph(
    "Country AI market data (country_ai_trends.csv) covers 6 countries × 7 years = 42 records. "
    f"The total market-wide AI job count across all country-year pairs is {M['total_market_ai_jobs']:,}. "
    f"The mean market average salary is ${M['mean_market_avg_salary']:,.0f} USD. "
    f"The mean market remote percentage is {M['mean_market_remote_pct']}%."
)

doc.add_heading("7.5 Skills Demand", level=2)
doc.add_paragraph(
    "Skills are analysed from skills_demand.csv independently (224,605 rows, 11 unique skills). "
    "All 11 skills appear with near-equal frequency (~9% each), confirming synthetic generation. "
    f"The most frequent skill by count is {D['top_skill_by_frequency']}."
)

# ──────────────────────────────────────────────────────────────
# 8. STATISTICAL ANALYSIS
# ──────────────────────────────────────────────────────────────
doc.add_heading("8. Statistical Analysis", level=1)

doc.add_paragraph(
    "All statistical tests used α = 0.05 (5% significance level). "
    "The D'Agostino-Pearson normality test confirmed that salary_mid is NOT normally distributed, "
    "so the non-parametric Kruskal-Wallis H-test was used for group comparisons throughout."
)

styled_table(doc,
    ["Factor", "H0", "Test", "Result"],
    [
        ["experience_level", "Equal salary distributions across Entry/Mid/Senior", "Kruskal-Wallis", "REJECT H0 — SIGNIFICANT"],
        ["country",          "Equal salary distributions across 6 countries",       "Kruskal-Wallis", "Fail to reject H0"],
        ["industry",         "Equal salary distributions across 5 industries",      "Kruskal-Wallis", "Fail to reject H0"],
        ["remote_type",      "Equal salary distributions across Remote/Hybrid/Onsite", "Kruskal-Wallis", "Fail to reject H0"],
        ["role_category",    "Equal salary distributions across Analytics/Engineering","Kruskal-Wallis","Fail to reject H0"],
        ["company_type",     "Equal salary distributions across company types",     "Kruskal-Wallis", "Fail to reject H0"],
        ["company_size",     "Equal salary distributions across company sizes",     "Kruskal-Wallis", "Fail to reject H0"],
    ],
    col_widths=[1.4, 2.3, 1.3, 1.6]
)

doc.add_paragraph(
    "Interpretation: Only experience_level produces a statistically significant difference "
    "in salary distributions. This is expected given the synthetic uniform generation of all "
    "other categorical dimensions."
)

# ──────────────────────────────────────────────────────────────
# 9. MACHINE LEARNING
# ──────────────────────────────────────────────────────────────
doc.add_heading("9. Machine Learning", level=1)

doc.add_heading("9.1 Problem Formulation", level=2)
doc.add_paragraph(
    "Salary prediction is framed as a supervised regression problem. "
    "The target variable is salary_mid (USD). "
    "Models are trained on Historical data only (2020–2024) and evaluated on a 20% holdout set."
)

doc.add_heading("9.2 Feature Selection and Leakage Prevention", level=2)
styled_table(doc,
    ["Feature Set", "Columns"],
    [
        ["Baseline (leakage-free)", "experience_level (encoded as 0/1/2)"],
        ["Full features",           "experience_level, country, industry, company_type, company_size, remote_type, job_title, role_category, posted_year (all one-hot encoded)"],
        ["EXCLUDED (leakage)",      "salary_min_usd, salary_max_usd, salary_range, min_experience_years, city, employment_type, job_id"],
    ],
    col_widths=[1.8, 4.8]
)

doc.add_heading("9.3 Model Configuration", level=2)
styled_table(doc,
    ["Model", "Configuration"],
    [
        ["Linear Regression (baseline)", "sklearn.linear_model.LinearRegression, experience_level only"],
        ["Linear Regression (full)",     "sklearn.linear_model.LinearRegression, full feature set"],
        ["Random Forest",                "RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)"],
        ["Gradient Boosting",            "GradientBoostingRegressor(n_estimators=100, random_state=42)"],
    ],
    col_widths=[2.0, 4.6]
)

doc.add_heading("9.4 Evaluation Metrics", level=2)
doc.add_paragraph(
    "Models are evaluated using MAE (Mean Absolute Error), RMSE (Root Mean Squared Error), "
    "and R² (coefficient of determination). Exact metric values are generated at notebook "
    "execution time from the actual data and reported in the executed notebook output. "
    "They are not reproduced here to avoid any risk of stale hard-coded values."
)
doc.add_paragraph(
    "Expected pattern: the baseline model (experience_level only) will achieve R² close to "
    "the full-feature models, confirming that experience_level dominates salary prediction "
    "in this synthetic dataset. This is a correct finding, not a modelling failure."
)

doc.add_heading("9.5 Feature Importance", level=2)
doc.add_paragraph(
    "Random Forest feature importances are reported in the master notebook. "
    "Experience-level encoded features will dominate, with all other features contributing "
    "marginally — a direct consequence of synthetic uniform distributions."
)

doc.add_heading("9.6 Clustering", level=2)
doc.add_paragraph(
    "K-Means clustering (K=2 to 8) was applied to a 4-feature matrix: "
    "salary_mid, experience_numeric, remote_flag, and company_size_numeric. "
    "The optimal K was selected using Silhouette Score (primary) and Davies-Bouldin Index (secondary). "
    "The resulting clusters are primarily structured around experience level × salary, "
    "consistent with statistical findings."
)

doc.add_heading("9.7 ML Limitations", level=2)
doc.add_paragraph(
    "Because the dataset is synthetically generated, trained ML models demonstrate "
    "methodological correctness but should not be used for real-world salary prediction. "
    "All ML results represent educational demonstrations only."
)

# ──────────────────────────────────────────────────────────────
# 10. DASHBOARDS
# ──────────────────────────────────────────────────────────────
doc.add_heading("10. Dashboards", level=1)

doc.add_heading("10.1 Power BI (Documented)", level=2)
doc.add_paragraph(
    "A complete Power BI documentation package is provided in powerbi/. "
    "No .pbix file is generated programmatically — the report must be built in Power BI Desktop "
    "by following POWERBI_SETUP.md and importing the three export CSV files."
)
styled_table(doc,
    ["Page", "Content"],
    [
        ["1. Executive Overview",     "12 KPI cards, year trend, country bar, role donut, salary by experience, work mode donut, top skills"],
        ["2. Salary Intelligence",    "Salary by all 7 dimensions + histogram"],
        ["3. Job Market Trends",      "Market-level country trends from country_ai_trends (dashed = Projected)"],
        ["4. Skills Intelligence",    "Skill frequency, category donut, level donut, top skill per country-year"],
        ["5. Work & Role Intelligence","Remote split, remote by country/industry/experience, role category, cities"],
    ],
    col_widths=[1.8, 4.8]
)
doc.add_paragraph(
    "28 DAX measures are documented in POWERBI_DAX_MEASURES.md, including salary KPIs, "
    "remote work percentages, experience premium, YoY growth, and market-level measures."
)

doc.add_heading("10.2 Streamlit Dashboard", level=2)
doc.add_paragraph("Run command:  streamlit run dashboard/app.py")
doc.add_paragraph("Opens at: http://localhost:8501")
styled_table(doc,
    ["Page", "Features"],
    [
        ["Overview",             "12 KPI metric cards, 6 interactive charts, period filter"],
        ["Salary Intelligence",  "Full filter set (7 dimensions), 7 salary charts"],
        ["Job Market",           "3 tabs: Sample Jobs / Market Trends / Location"],
        ["Skills Intelligence",  "Skill frequency, category, level, top-skill heatmap"],
        ["Remote Work",          "Work mode donut, by country/industry/experience, market trend"],
        ["ML Insights",          "Model comparison table, predicted vs actual, feature importance, salary predictor"],
        ["Data Explorer",        "3-dataset browser with filter + CSV download"],
        ["Methodology",          "Full limitations documentation, data sources, project architecture"],
    ],
    col_widths=[1.8, 4.8]
)

doc.add_heading("10.3 HTML/CSS/JavaScript Dashboard", level=2)
doc.add_paragraph("Run command (from project root):  cd web_dashboard && python -m http.server 8080")
doc.add_paragraph("Opens at: http://localhost:8080")
doc.add_paragraph(
    "Standalone static dashboard using Chart.js 4.4. No backend required. "
    "Loads pre-aggregated JSON from web_dashboard/data/. Seven sections covering "
    "KPIs, job market, salary, skills, remote work, country trends, and role intelligence. "
    "Dark theme with professional navy/blue palette."
)

# ──────────────────────────────────────────────────────────────
# 11. KEY FINDINGS
# ──────────────────────────────────────────────────────────────
doc.add_heading("11. Key Findings", level=1)

doc.add_paragraph(
    "The following findings are derived from the processed data. "
    "They describe patterns within the supplied synthetic dataset only "
    "and do not represent the real global AI job market."
)

styled_table(doc,
    ["Finding", "Value / Interpretation"],
    [
        ["Total job postings",          f"{J['total_job_postings']:,}"],
        ["Historical jobs (2020–2024)", f"{J['historical_jobs']:,} (71.6%)"],
        ["Projected jobs (2025–2026)",  f"{J['projected_jobs']:,} (28.4%)"],
        ["Mean salary midpoint",        f"${S['mean_salary_mid']:,.2f}"],
        ["Median salary midpoint",      f"${S['median_salary_mid']:,.2f}"],
        ["Entry avg salary",            f"${S['entry_avg_salary']:,.2f}"],
        ["Senior avg salary",           f"${S['senior_avg_salary']:,.2f}"],
        ["Senior / Entry ratio",        f"{S['senior_entry_ratio']:.2f}×"],
        ["Remote job %",                f"{D['remote_job_pct']}%"],
        ["Top country (postings)",      D["top_country"]],
        ["Top job role",                D["top_job_role"]],
        ["Top skill (frequency)",       D["top_skill_by_frequency"]],
        ["Total market AI jobs",        f"{M['total_market_ai_jobs']:,}"],
        ["Mean market avg salary",      f"${M['mean_market_avg_salary']:,.0f}"],
        ["Salary driver",               "Only experience_level is statistically significant (Kruskal-Wallis)"],
        ["All other salary factors",    "Not significant — consistent with synthetic uniform data"],
    ],
    col_widths=[2.5, 4.1]
)

# ──────────────────────────────────────────────────────────────
# 12. LIMITATIONS
# ──────────────────────────────────────────────────────────────
doc.add_heading("12. Limitations", level=1)

limitations = [
    ("Synthetic data",        "Near-uniform distributions across all categorical dimensions. No real-world imbalances (e.g. US salary premium, Tech industry dominance). Findings do not represent the global AI job market."),
    ("Skills join failure",   "skills_demand.job_id matches ai_jobs.job_id for only 4.1% of records (2,050 / 50,000). This is a dataset generation artifact. No job-level skill enrichment is performed."),
    ("Projected years",       "28.4% of job postings have posted_year 2025–2026. These are synthetic forward-looking entries, not observed historical data. All dashboards clearly distinguish Historical from Projected."),
    ("employment_type",       "All 50,000 rows have employment_type = 'Full-time'. Zero variance. This column was excluded from all analyses and ML models."),
    ("Salary independence",   "Salary varies meaningfully only with experience_level. Country, industry, role, remote type, and company characteristics produce <$1,100 salary range — a consequence of synthetic generation."),
    ("Narrow scope",          "Only 6 countries, 6 job titles, and 11 skills are represented. Real-world AI job markets span hundreds of countries, thousands of titles, and many more skills."),
    ("Small time-series",     "country_ai_trends has only 42 rows (6 countries × 7 years). This is insufficient for robust time-series modelling."),
    ("No PBIX file",          "A Power BI .pbix file cannot be generated programmatically. Complete documentation is provided for manual construction in Power BI Desktop."),
]

for title, detail in limitations:
    p = doc.add_paragraph(style='List Number')
    run_t = p.add_run(f"{title}: ")
    run_t.bold = True
    p.add_run(detail)

# ──────────────────────────────────────────────────────────────
# 13. FUTURE ENHANCEMENTS
# ──────────────────────────────────────────────────────────────
doc.add_heading("13. Future Enhancements", level=1)

future = [
    "Replace synthetic data with real-world job postings from LinkedIn/Indeed/Glassdoor APIs.",
    "Expand geographic coverage to 50+ countries and hundreds of job titles.",
    "Fix the skills–job linkage to enable job-level skill enrichment and salary-by-skill analysis.",
    "Implement real-time data ingestion and automated pipeline refresh (Apache Airflow / Prefect).",
    "Add NLP-based job description analysis to extract richer skill and requirement signals.",
    "Deploy the Streamlit dashboard to Streamlit Community Cloud for public access.",
    "Build a Power BI Service report with scheduled data refresh.",
    "Add robust time-series forecasting with a longer historical time series.",
    "Implement a proper AB/testing framework for model comparison.",
]
for item in future:
    doc.add_paragraph(item, style='List Bullet')

# ──────────────────────────────────────────────────────────────
# 14. CONCLUSION
# ──────────────────────────────────────────────────────────────
doc.add_heading("14. Conclusion", level=1)

doc.add_paragraph(
    "AI MarketLens successfully demonstrates a complete end-to-end data analytics and "
    "machine learning pipeline applied to a structured job market dataset. "
    "The project covers all core analytical competencies: data ingestion and validation, "
    "preprocessing and feature engineering, exploratory data analysis, statistical hypothesis "
    "testing, supervised regression, unsupervised clustering, and multi-format dashboard delivery."
)
doc.add_paragraph(
    "The most important analytical finding is that salary varies significantly only with "
    "experience level in this dataset — a consequence of its synthetic uniform generation. "
    "This finding is consistent, reproducible, and correctly identified through statistical testing. "
    "It does not represent a modelling failure; it represents an honest characterisation of "
    "the available data."
)
doc.add_paragraph(
    "All four phases of the project — dataset audit, preprocessing and notebook, dashboards, "
    "and finalisation — were completed. The project is packaged for academic submission with "
    "a master notebook, processed datasets, three dashboard implementations, complete Power BI "
    "documentation, and this report."
)

# ──────────────────────────────────────────────────────────────
# 15. REFERENCES / DATA SOURCE
# ──────────────────────────────────────────────────────────────
doc.add_heading("15. References and Data Source", level=1)

doc.add_paragraph(
    "Dataset: AI & Data Science Job Market — Kaggle synthetic dataset "
    "(5 CSV files: ai_jobs.csv, skills_demand.csv, country_ai_trends.csv, "
    "job_title_mapping.csv, data_dictionary.csv). "
    "Located at: data/raw/archive (1)/ in this repository."
)
doc.add_paragraph(
    "Python libraries: pandas, numpy, matplotlib, seaborn, plotly, scikit-learn, "
    "scipy, streamlit, jupyter. All under their respective open-source licences."
)
doc.add_paragraph("Chart.js 4.4.0 — MIT Licence. https://www.chartjs.org/")
doc.add_paragraph(
    "IBM SkillsBuild Data Analytics with AI Internship — BharatCares × AICTE × IBM."
)

# ──────────────────────────────────────────────────────────────
# APPENDIX
# ──────────────────────────────────────────────────────────────
doc.add_heading("Appendix A — Authoritative KPI Reference", level=1)

doc.add_paragraph(
    "The following KPIs are calculated from data/exports/powerbi_jobs.csv "
    "using reconcile_kpis.py. Definition: salary_mid = (salary_min_usd + salary_max_usd) / 2.0"
)

styled_table(doc,
    ["KPI", "Definition", "Value"],
    [
        ["Total Job Postings",          "COUNT(job_id)",                              f"{J['total_job_postings']:,}"],
        ["Historical Jobs",             "posted_year <= 2024",                         f"{J['historical_jobs']:,}"],
        ["Projected Jobs",              "posted_year >= 2025",                         f"{J['projected_jobs']:,}"],
        ["Mean Salary Midpoint",        "MEAN(salary_mid)",                            f"${S['mean_salary_mid']:,.2f}"],
        ["Median Salary Midpoint",      "MEDIAN(salary_mid)",                          f"${S['median_salary_mid']:,.2f}"],
        ["Min Salary Midpoint",         "MIN(salary_mid)",                             f"${S['min_salary_mid']:,.2f}"],
        ["Max Salary Midpoint",         "MAX(salary_mid)",                             f"${S['max_salary_mid']:,.2f}"],
        ["Min salary_min_usd",          "MIN(salary_min_usd)",                         f"${S['min_salary_min_usd']:,}"],
        ["Max salary_max_usd",          "MAX(salary_max_usd)",                         f"${S['max_salary_max_usd']:,}"],
        ["Entry Avg Salary",            "MEAN(salary_mid WHERE experience='Entry')",    f"${S['entry_avg_salary']:,.2f}"],
        ["Mid Avg Salary",              "MEAN(salary_mid WHERE experience='Mid')",      f"${S['mid_avg_salary']:,.2f}"],
        ["Senior Avg Salary",           "MEAN(salary_mid WHERE experience='Senior')",  f"${S['senior_avg_salary']:,.2f}"],
        ["Senior/Entry Ratio",          "Senior Avg / Entry Avg",                       f"{S['senior_entry_ratio']:.4f}×"],
        ["Remote Job %",                "COUNT(remote_type='Remote') / COUNT(*) × 100", f"{D['remote_job_pct']}%"],
        ["Countries Covered",           "DISTINCT COUNT(country)",                      str(D['countries_covered'])],
        ["Job Roles",                   "DISTINCT COUNT(job_title)",                    str(D['unique_job_roles'])],
        ["Skills Tracked",              "DISTINCT COUNT(skill) in skills_demand",       str(D['skills_tracked'])],
        ["Top Country",                 "MODE(country)",                                D['top_country']],
        ["Top Job Role",                "MODE(job_title)",                              D['top_job_role']],
        ["Top Skill",                   "MODE(skill) in skills_demand",                 D['top_skill_by_frequency']],
        ["Total Market AI Jobs",        "SUM(total_ai_jobs) in country_ai_trends",      f"{M['total_market_ai_jobs']:,}"],
        ["Mean Market Avg Salary",      "MEAN(avg_salary_usd) in country_ai_trends",    f"${M['mean_market_avg_salary']:,.0f}"],
        ["Mean Market Remote %",        "MEAN(remote_percentage) in country_ai_trends", f"{M['mean_market_remote_pct']}%"],
    ],
    col_widths=[1.9, 2.4, 1.9]
)

doc.add_page_break()
doc.add_heading("Appendix B — Project Structure", level=1)
doc.add_paragraph("The complete project folder structure is documented in README.md.")

doc.add_heading("Appendix C — Data Dictionary (Key Columns)", level=1)
styled_table(doc,
    ["Column", "Source", "Type", "Description"],
    [
        ["job_id",           "ai_jobs",           "str",   "Unique 12-char job identifier (PK)"],
        ["salary_mid",       "engineered",         "float", "(salary_min_usd + salary_max_usd) / 2.0"],
        ["experience_level", "ai_jobs",           "str",   "Entry / Mid / Senior — primary salary driver"],
        ["period_type",      "engineered",         "str",   "Historical (<=2024) or Projected (2025-2026)"],
        ["role_category",    "job_title_mapping",  "str",   "Analytics or Engineering"],
        ["remote_flag",      "engineered",         "int",   "1 if remote_type=='Remote' else 0"],
        ["market_total_ai_jobs", "country_ai_trends", "int", "Market-wide AI job count (LEFT JOINed)"],
        ["top_skill",        "country_ai_trends",  "str",   "Most demanded skill per country-year"],
    ],
    col_widths=[1.6, 1.6, 0.7, 2.7]
)

# ─────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────
out = REPORTS_DIR / "Ritusmita_AI_MarketLens_ProjectReport.docx"
doc.save(out)
print(f"Report saved: {out}  ({out.stat().st_size // 1024} KB)")
