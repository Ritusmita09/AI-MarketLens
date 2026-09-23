"""Remote Work page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs, load_country_trends
from dashboard.utils.charts import bar_chart, pie_chart, line_chart

jobs = load_jobs()
ct   = load_country_trends()

with st.sidebar:
    st.subheader(":material/filter_list: Filters")
    sel_period = st.segmented_control(
        "Period", ["All", "Historical", "Projected"], default="All", key="rw_period")
    sel_countries = st.multiselect(
        "Country", sorted(jobs["country"].unique()), key="rw_country")
    sel_industry = st.multiselect(
        "Industry", sorted(jobs["industry"].unique()), key="rw_industry")
    sel_exp = st.multiselect(
        "Experience Level", ["Entry","Mid","Senior"],
        default=["Entry","Mid","Senior"], key="rw_exp")

df = jobs.copy()
if sel_period != "All":  df = df[df["period_type"] == sel_period]
if sel_countries:        df = df[df["country"].isin(sel_countries)]
if sel_industry:         df = df[df["industry"].isin(sel_industry)]
if sel_exp:              df = df[df["experience_level"].isin(sel_exp)]

st.title(":material/home_work: Remote Work Analysis")
st.caption(f"Showing {len(df):,} job records")
st.divider()

# KPI row
remote_pct  = round((df["remote_type"] == "Remote").mean() * 100, 1)
hybrid_pct  = round((df["remote_type"] == "Hybrid").mean() * 100, 1)
onsite_pct  = round((df["remote_type"] == "Onsite").mean() * 100, 1)
market_rem  = round(ct["remote_percentage"].mean(), 1)

with st.container(horizontal=True):
    st.metric("Remote %",          f"{remote_pct}%", border=True)
    st.metric("Hybrid %",          f"{hybrid_pct}%", border=True)
    st.metric("Onsite %",          f"{onsite_pct}%", border=True)
    st.metric("Market Remote % (avg)", f"{market_rem}%", border=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Work Mode Distribution")
        rd = df["remote_type"].value_counts().reset_index()
        rd.columns = ["type","count"]
        fig = pie_chart(rd, "type", "count", "Remote / Hybrid / Onsite", height=340)
        st.plotly_chart(fig, key="rw_pie")

with col2:
    with st.container(border=True):
        st.subheader("Remote % by Country (sample)")
        by_country = (
            df.groupby("country")["remote_flag"]
            .mean().mul(100).round(1).reset_index(name="remote_pct")
            .sort_values("remote_pct")
        )
        fig = bar_chart(by_country, "remote_pct", "country",
                        "Remote % by Country", orientation="h", height=340)
        st.plotly_chart(fig, key="rw_country_bar")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("Remote % by Industry")
        by_ind = (
            df.groupby("industry")["remote_flag"]
            .mean().mul(100).round(1).reset_index(name="remote_pct")
            .sort_values("remote_pct")
        )
        fig = bar_chart(by_ind, "remote_pct", "industry",
                        "Remote % by Industry", orientation="h", height=300)
        st.plotly_chart(fig, key="rw_ind_bar")

with col4:
    with st.container(border=True):
        st.subheader("Remote % by Experience Level")
        by_exp = (
            df.groupby("experience_level")["remote_flag"]
            .mean().mul(100).round(1).reset_index(name="remote_pct")
        )
        fig = bar_chart(by_exp, "experience_level", "remote_pct",
                        "Remote % by Experience", height=300)
        st.plotly_chart(fig, key="rw_exp_bar")

# Market remote trend
with st.container(border=True):
    st.subheader("Market Remote % by Country & Year (country_ai_trends)")
    st.caption("Market-level remote % from country_ai_trends. Dashed = Projected (2025–2026).")
    fig = line_chart(ct, "year", "remote_percentage", "country",
                     "Market Remote % Trend", height=380, period_dashes=True)
    st.plotly_chart(fig, key="rw_mkt_line")

# Trend by year (sample)
with st.container(border=True):
    st.subheader("Remote Jobs % by Year (sample dataset)")
    by_year = (
        df.groupby(["posted_year","period_type"])["remote_flag"]
        .mean().mul(100).round(1).reset_index(name="remote_pct")
    )
    fig = px.line(by_year, x="posted_year", y="remote_pct",
                  color="period_type",
                  color_discrete_map={"Historical":"#3b82d4","Projected":"#f59e0b"},
                  markers=True, height=320,
                  title="Remote % by Year (sample)")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="Year", yaxis_title="Remote %")
    st.plotly_chart(fig, key="rw_year_line")
