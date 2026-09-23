"""Data Explorer page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import io

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs, load_skills, load_country_trends

jobs   = load_jobs()
skills = load_skills()
ct     = load_country_trends()

st.title(":material/table: Data Explorer")
st.caption("Browse, filter, and download the processed datasets.")
st.divider()

dataset_choice = st.segmented_control(
    "Dataset",
    ["Jobs (50k)", "Skills (225k)", "Country Trends (42)"],
    default="Jobs (50k)",
    key="de_dataset"
)

# ---------------------------------------------------------------------------
# Jobs Explorer
# ---------------------------------------------------------------------------
if dataset_choice == "Jobs (50k)":
    with st.sidebar:
        st.subheader(":material/filter_list: Filters")
        f_country  = st.multiselect("Country",   sorted(jobs["country"].unique()))
        f_role     = st.multiselect("Job Role",  sorted(jobs["job_title"].unique()))
        f_exp      = st.multiselect("Experience",["Entry","Mid","Senior"])
        f_remote   = st.multiselect("Remote Type",["Remote","Hybrid","Onsite"])
        f_period   = st.segmented_control("Period", ["All","Historical","Projected"], default="All")
        f_ind      = st.multiselect("Industry",  sorted(jobs["industry"].unique()))

    df = jobs.copy()
    if f_country:  df = df[df["country"].isin(f_country)]
    if f_role:     df = df[df["job_title"].isin(f_role)]
    if f_exp:      df = df[df["experience_level"].isin(f_exp)]
    if f_remote:   df = df[df["remote_type"].isin(f_remote)]
    if f_period != "All": df = df[df["period_type"] == f_period]
    if f_ind:      df = df[df["industry"].isin(f_ind)]

    st.caption(f"Showing {len(df):,} of {len(jobs):,} rows")

    display_cols = [
        "job_id","job_title","role_category","company_type","industry",
        "country","city","remote_type","experience_level","salary_min_usd",
        "salary_mid","salary_max_usd","posted_year","period_type","company_size"
    ]
    st.dataframe(
        df[display_cols].reset_index(drop=True),
        hide_index=True,
        column_config={
            "salary_mid":     st.column_config.NumberColumn("Salary Mid", format="$%.0f"),
            "salary_min_usd": st.column_config.NumberColumn("Salary Min", format="$%d"),
            "salary_max_usd": st.column_config.NumberColumn("Salary Max", format="$%d"),
        },
        height=480,
    )

    csv_buf = io.StringIO()
    df[display_cols].to_csv(csv_buf, index=False)
    st.download_button(
        ":material/download: Download filtered CSV",
        data=csv_buf.getvalue(),
        file_name="ai_marketlens_jobs_filtered.csv",
        mime="text/csv",
        type="primary",
    )

# ---------------------------------------------------------------------------
# Skills Explorer
# ---------------------------------------------------------------------------
elif dataset_choice == "Skills (225k)":
    with st.sidebar:
        f_skill = st.multiselect("Skill", sorted(skills["skill"].unique()))
        f_cat   = st.multiselect("Category", sorted(skills["skill_category"].unique()))
        f_level = st.multiselect("Level", sorted(skills["skill_level"].unique()))

    df_sk = skills.copy()
    if f_skill: df_sk = df_sk[df_sk["skill"].isin(f_skill)]
    if f_cat:   df_sk = df_sk[df_sk["skill_category"].isin(f_cat)]
    if f_level: df_sk = df_sk[df_sk["skill_level"].isin(f_level)]

    st.caption(f"Showing {len(df_sk):,} of {len(skills):,} rows")
    st.warning(
        ":material/warning: skills_demand.job_id does NOT reliably match "
        "ai_jobs.job_id (4.1% overlap). "
        "The job_id column is shown for reference only."
    )

    st.dataframe(df_sk.head(5000).reset_index(drop=True), hide_index=True, height=480)
    st.caption("Showing first 5,000 rows of filtered result.")

    csv_buf2 = io.StringIO()
    df_sk.to_csv(csv_buf2, index=False)
    st.download_button(
        ":material/download: Download filtered skills CSV",
        data=csv_buf2.getvalue(),
        file_name="ai_marketlens_skills_filtered.csv",
        mime="text/csv",
        type="primary",
    )

# ---------------------------------------------------------------------------
# Country Trends Explorer
# ---------------------------------------------------------------------------
else:
    with st.sidebar:
        f_ct_country = st.multiselect("Country", sorted(ct["country"].unique()))
        f_ct_period  = st.segmented_control("Period", ["All","Historical","Projected"], default="All")

    df_ct = ct.copy()
    if f_ct_country: df_ct = df_ct[df_ct["country"].isin(f_ct_country)]
    if f_ct_period != "All": df_ct = df_ct[df_ct["period_type"] == f_ct_period]

    st.caption(f"Showing {len(df_ct)} of {len(ct)} rows")
    st.dataframe(df_ct.sort_values(["country","year"]).reset_index(drop=True),
                 hide_index=True)

    csv_buf3 = io.StringIO()
    df_ct.to_csv(csv_buf3, index=False)
    st.download_button(
        ":material/download: Download country trends CSV",
        data=csv_buf3.getvalue(),
        file_name="ai_marketlens_country_trends_filtered.csv",
        mime="text/csv",
        type="primary",
    )
