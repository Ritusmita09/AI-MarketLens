"""Salary Intelligence page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs
from dashboard.utils.charts import bar_chart, histogram_chart

import plotly.express as px

jobs = load_jobs()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader(":material/filter_list: Filters")
    sel_exp = st.multiselect(
        "Experience Level", ["Entry", "Mid", "Senior"],
        default=["Entry", "Mid", "Senior"], key="sal_exp")
    sel_countries = st.multiselect(
        "Country", sorted(jobs["country"].unique()), key="sal_country")
    sel_roles = st.multiselect(
        "Job Role", sorted(jobs["job_title"].unique()), key="sal_role")
    sel_industry = st.multiselect(
        "Industry", sorted(jobs["industry"].unique()), key="sal_industry")
    sel_remote = st.multiselect(
        "Remote Type", ["Remote", "Hybrid", "Onsite"], key="sal_remote")
    sel_ctype = st.multiselect(
        "Company Type", sorted(jobs["company_type"].unique()), key="sal_ctype")
    sel_csize = st.multiselect(
        "Company Size", sorted(jobs["company_size"].unique()), key="sal_csize")
    sel_period = st.segmented_control(
        "Period", ["All", "Historical", "Projected"], default="All", key="sal_period")

df = jobs.copy()
if sel_exp:        df = df[df["experience_level"].isin(sel_exp)]
if sel_countries:  df = df[df["country"].isin(sel_countries)]
if sel_roles:      df = df[df["job_title"].isin(sel_roles)]
if sel_industry:   df = df[df["industry"].isin(sel_industry)]
if sel_remote:     df = df[df["remote_type"].isin(sel_remote)]
if sel_ctype:      df = df[df["company_type"].isin(sel_ctype)]
if sel_csize:      df = df[df["company_size"].isin(sel_csize)]
if sel_period != "All": df = df[df["period_type"] == sel_period]

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.title(":material/payments: Salary Intelligence")
st.caption(f"Showing {len(df):,} job records | salary_mid = (min + max) / 2")
st.divider()

# KPI cards
with st.container(horizontal=True):
    st.metric("Average Salary",    f"${df['salary_mid'].mean():,.0f}",    border=True)
    st.metric("Median Salary",     f"${df['salary_mid'].median():,.0f}",   border=True)
    st.metric("Min Salary",        f"${df['salary_min_usd'].min():,}",     border=True)
    st.metric("Max Salary",        f"${df['salary_max_usd'].max():,}",     border=True)
    st.metric("Salary Range",      f"${int(df['salary_max_usd'].max() - df['salary_min_usd'].min()):,}", border=True)
    sr = df[df["experience_level"]=="Senior"]["salary_mid"].mean() / df[df["experience_level"]=="Entry"]["salary_mid"].mean() if df[df["experience_level"]=="Entry"]["salary_mid"].mean() > 0 else 0
    st.metric("Senior/Entry Ratio", f"{sr:.2f}x", border=True)

# ---------------------------------------------------------------------------
# Salary distribution
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.subheader("Salary Midpoint Distribution")
    fig = histogram_chart(df["salary_mid"], "Salary Midpoint (USD)", height=300)
    st.plotly_chart(fig, key="sal_hist")

# ---------------------------------------------------------------------------
# By dimension
# ---------------------------------------------------------------------------
dims = [
    ("experience_level", "Salary by Experience Level", ["Entry", "Mid", "Senior"]),
    ("country",          "Salary by Country",          None),
    ("job_title",        "Salary by Job Role",         None),
    ("industry",         "Salary by Industry",         None),
    ("remote_type",      "Salary by Remote Type",      None),
    ("company_type",     "Salary by Company Type",     None),
    ("company_size",     "Salary by Company Size",     None),
]

for i in range(0, len(dims), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i + j >= len(dims):
            break
        col_name, title, order = dims[i + j]
        with col:
            with st.container(border=True):
                st.subheader(title)
                agg = (
                    df.groupby(col_name)["salary_mid"]
                    .agg(avg="mean", median="median")
                    .round(0).reset_index()
                )
                if order:
                    agg = agg.set_index(col_name).reindex(order).reset_index()
                agg = agg.sort_values("avg", ascending=True)
                fig = px.bar(
                    agg, x="avg", y=col_name, orientation="h",
                    title=f"Average Salary — {title}",
                    labels={"avg": "Avg Salary (USD)", col_name: ""},
                    color_discrete_sequence=["#3b82d4"],
                    height=300,
                )
                fig.update_layout(
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(t=30, b=10, l=10, r=10),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor="#e5e7eb"),
                )
                st.plotly_chart(fig, key=f"sal_chart_{col_name}")

# ---------------------------------------------------------------------------
# Salary by year
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.subheader("Average Salary by Year")
    sal_year = (
        df.groupby(["posted_year", "period_type"])["salary_mid"]
        .mean().round(0).reset_index()
    )
    fig = px.line(
        sal_year, x="posted_year", y="salary_mid",
        color="period_type", markers=True,
        title="Average Salary Midpoint by Year",
        color_discrete_map={"Historical": "#3b82d4", "Projected": "#f59e0b"},
        height=350,
    )
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=40, b=20),
        xaxis_title="Year", yaxis_title="Avg Salary (USD)",
    )
    st.plotly_chart(fig, key="sal_year")
    st.caption(":material/warning: Salary varies only minimally by year in this synthetic dataset.")
