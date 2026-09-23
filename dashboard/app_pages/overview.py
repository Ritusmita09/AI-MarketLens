"""Overview page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs, load_skills, load_country_trends, compute_kpis
from dashboard.utils.charts import bar_chart, line_chart, pie_chart

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
jobs   = load_jobs()
skills = load_skills()
ct     = load_country_trends()
kpis   = compute_kpis(jobs, skills, ct)

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader(":material/filter_list: Filters")
    sel_period = st.segmented_control(
        "Period", ["All", "Historical", "Projected"], default="All", key="ov_period")
    sel_countries = st.multiselect(
        "Country", sorted(jobs["country"].unique()), key="ov_country")
    sel_industries = st.multiselect(
        "Industry", sorted(jobs["industry"].unique()), key="ov_industry")

# Apply filters
df = jobs.copy()
if sel_period != "All":
    df = df[df["period_type"] == sel_period]
if sel_countries:
    df = df[df["country"].isin(sel_countries)]
if sel_industries:
    df = df[df["industry"].isin(sel_industries)]

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title(":material/analytics: AI MarketLens")
st.caption("AI-Powered Global Data Science & AI Job Market Intelligence Platform")
st.divider()

# ---------------------------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------------------------
st.subheader("Key Performance Indicators")

with st.container(horizontal=True):
    st.metric("Total Job Postings",  f"{len(df):,}", border=True)
    st.metric("Average Salary",      f"${kpis['avg_salary']:,.0f}", border=True)
    st.metric("Median Salary",       f"${kpis['median_salary']:,.0f}", border=True)
    st.metric("Remote Job %",        f"{kpis['remote_job_pct']}%", border=True)
    st.metric("Countries",           f"{kpis['countries_covered']}", border=True)
    st.metric("Skills Tracked",      f"{kpis['skills_tracked']}", border=True)

with st.container(horizontal=True):
    st.metric("Historical Jobs",     f"{kpis['historical_jobs']:,}", border=True)
    st.metric("Projected Jobs",      f"{kpis['projected_jobs']:,}", border=True)
    st.metric("Entry Avg Salary",    f"${kpis['entry_avg_salary']:,.0f}", border=True)
    st.metric("Senior Avg Salary",   f"${kpis['senior_avg_salary']:,.0f}", border=True)
    st.metric("Senior/Entry Ratio",  f"{kpis['senior_premium_ratio']}x", border=True)
    st.metric("Market AI Jobs",      f"{kpis['total_market_ai_jobs']:,}", border=True)

st.info(
    ":material/info: **Note:** 'Total Job Postings' is the 50,000-row sample dataset. "
    "'Market AI Jobs' is the broader market aggregate from country_ai_trends. These are different populations.",
    icon=None
)

# ---------------------------------------------------------------------------
# Charts Row 1
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Job Postings by Year")
        year_data = (
            df.groupby(["posted_year", "period_type"])
            .size().reset_index(name="count")
        )
        fig = bar_chart(year_data, "posted_year", "count",
                        "Job Postings by Year",
                        color_col="period_type", height=340)
        fig.update_layout(
            colorway=["#3b82d4", "#f59e0b"],
            legend_title_text="Period"
        )
        st.plotly_chart(fig, key="ov_year_bar")

with col2:
    with st.container(border=True):
        st.subheader("Job Postings by Country")
        country_data = df["country"].value_counts().reset_index()
        country_data.columns = ["country", "count"]
        fig = bar_chart(country_data.sort_values("count"), "count", "country",
                        "Job Postings by Country", orientation="h", height=340)
        st.plotly_chart(fig, key="ov_country_bar")

# ---------------------------------------------------------------------------
# Charts Row 2
# ---------------------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("Job Postings by Role")
        role_data = df["job_title"].value_counts().reset_index()
        role_data.columns = ["role", "count"]
        fig = pie_chart(role_data, "role", "count", "Job Role Distribution", height=340)
        st.plotly_chart(fig, key="ov_role_pie")

with col4:
    with st.container(border=True):
        st.subheader("Remote / Hybrid / Onsite")
        remote_data = df["remote_type"].value_counts().reset_index()
        remote_data.columns = ["type", "count"]
        fig = pie_chart(remote_data, "type", "count", "Work Mode Distribution", height=340)
        st.plotly_chart(fig, key="ov_remote_pie")

# ---------------------------------------------------------------------------
# Charts Row 3
# ---------------------------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    with st.container(border=True):
        st.subheader("Average Salary by Experience Level")
        sal_exp = (
            df.groupby("experience_level")["salary_mid"]
            .mean().round(0).reset_index()
        )
        sal_exp.columns = ["experience_level", "avg_salary"]
        order = ["Entry", "Mid", "Senior"]
        sal_exp = sal_exp.set_index("experience_level").reindex(order).reset_index()
        fig = bar_chart(sal_exp, "experience_level", "avg_salary",
                        "Avg Salary by Experience", height=340)
        st.plotly_chart(fig, key="ov_sal_exp")

with col6:
    with st.container(border=True):
        st.subheader("Top Skills (Skills Dataset)")
        skill_data = (
            skills["skill"].value_counts().reset_index()
        )
        skill_data.columns = ["skill", "count"]
        fig = bar_chart(
            skill_data.sort_values("count"),
            "count", "skill",
            "Skill Demand (independent dataset)",
            orientation="h", height=340
        )
        st.plotly_chart(fig, key="ov_skills_bar")

# ---------------------------------------------------------------------------
# Market trend chart
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.subheader("Market AI Jobs by Country and Year (country_ai_trends — market level)")
    st.caption(
        "Source: country_ai_trends.csv — market-wide aggregate statistics. "
        "Dashed lines = Projected (2025–2026). NOT the same as the 50k job sample."
    )
    fig = line_chart(ct, "year", "total_ai_jobs", "country",
                     "Total Market AI Jobs by Country & Year",
                     height=400, period_dashes=True)
    st.plotly_chart(fig, key="ov_market_trend")
