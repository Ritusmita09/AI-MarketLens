"""Skills Intelligence page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_skills, load_country_trends
from dashboard.utils.charts import bar_chart, pie_chart, heatmap_chart

skills = load_skills()
ct     = load_country_trends()

with st.sidebar:
    sel_category = st.multiselect(
        "Skill Category", sorted(skills["skill_category"].unique()), key="sk_cat")
    sel_level = st.multiselect(
        "Skill Level", sorted(skills["skill_level"].unique()), key="sk_level")

df_sk = skills.copy()
if sel_category: df_sk = df_sk[df_sk["skill_category"].isin(sel_category)]
if sel_level:    df_sk = df_sk[df_sk["skill_level"].isin(sel_level)]

st.title(":material/psychology: Skills Intelligence")
st.divider()

st.warning(
    ":material/warning: **Data Limitation:** "
    "Skill demand is analysed as an independent dataset. "
    "The `skills_demand.job_id` column does not reliably match `ai_jobs.job_id` "
    "(only 4.1% overlap — dataset generation artifact). "
    "Job-level skill enrichment (e.g. 'skills by country' from job records) is not available. "
    "Country-level top-skill data comes from `country_ai_trends.top_skill`.",
)

# KPI row
with st.container(horizontal=True):
    st.metric("Total Skill Records", f"{len(df_sk):,}", border=True)
    st.metric("Unique Skills",       f"{df_sk['skill'].nunique()}", border=True)
    st.metric("Skill Categories",    f"{df_sk['skill_category'].nunique()}", border=True)
    st.metric("Skill Levels",        f"{df_sk['skill_level'].nunique()}", border=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Skill Demand (frequency)")
        skill_freq = df_sk["skill"].value_counts().reset_index()
        skill_freq.columns = ["skill","count"]
        fig = bar_chart(skill_freq.sort_values("count"), "count", "skill",
                        "Skill Frequency", orientation="h", height=380)
        st.plotly_chart(fig, key="sk_freq")

with col2:
    with st.container(border=True):
        st.subheader("Skill Category Distribution")
        cat_freq = df_sk["skill_category"].value_counts().reset_index()
        cat_freq.columns = ["category","count"]
        fig = pie_chart(cat_freq, "category", "count",
                        "Skill Category", height=380)
        st.plotly_chart(fig, key="sk_cat_pie")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("Skill Level Distribution")
        lvl_freq = df_sk["skill_level"].value_counts().reset_index()
        lvl_freq.columns = ["level","count"]
        fig = pie_chart(lvl_freq, "level", "count",
                        "Skill Level", height=340)
        st.plotly_chart(fig, key="sk_lvl_pie")

with col4:
    with st.container(border=True):
        st.subheader("Skill x Level Heatmap")
        cross = df_sk.groupby(["skill","skill_level"]).size().reset_index(name="count")
        fig = heatmap_chart(cross, "skill_level", "skill", "count",
                            "Skill x Level Count", height=340)
        st.plotly_chart(fig, key="sk_level_heatmap")

# Top skill by country/year
with st.container(border=True):
    st.subheader("Top Skill by Country & Year (from country_ai_trends)")
    st.caption("Source: country_ai_trends.top_skill — most demanded skill per country-year pair.")
    top_skill_pivot = ct.pivot_table(
        index="country", columns="year", values="top_skill", aggfunc="first"
    ).reset_index()

    st.dataframe(top_skill_pivot, hide_index=True)

    # Visualise as a stacked bar of top skill occurrences
    ts_freq = ct["top_skill"].value_counts().reset_index()
    ts_freq.columns = ["skill","appearances"]
    fig = bar_chart(ts_freq.sort_values("appearances"), "appearances", "skill",
                    "Top Skill Appearances Across Country-Year Pairs",
                    orientation="h", height=320)
    st.plotly_chart(fig, key="sk_topskill_bar")
