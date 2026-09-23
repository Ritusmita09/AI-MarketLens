"""Job Market page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs, load_country_trends
from dashboard.utils.charts import bar_chart, line_chart, heatmap_chart

jobs = load_jobs()
ct   = load_country_trends()

with st.sidebar:
    st.subheader(":material/filter_list: Filters")
    sel_period = st.segmented_control(
        "Period", ["All", "Historical", "Projected"], default="All", key="jm_period")
    sel_countries = st.multiselect(
        "Country", sorted(jobs["country"].unique()), key="jm_country")
    sel_roles = st.multiselect(
        "Job Role", sorted(jobs["job_title"].unique()), key="jm_role")
    sel_industry = st.multiselect(
        "Industry", sorted(jobs["industry"].unique()), key="jm_industry")

df = jobs.copy()
if sel_period != "All":    df = df[df["period_type"] == sel_period]
if sel_countries:          df = df[df["country"].isin(sel_countries)]
if sel_roles:              df = df[df["job_title"].isin(sel_roles)]
if sel_industry:           df = df[df["industry"].isin(sel_industry)]

ct_filtered = ct.copy()
if sel_countries:          ct_filtered = ct_filtered[ct_filtered["country"].isin(sel_countries)]
if sel_period != "All":    ct_filtered = ct_filtered[ct_filtered["period_type"] == sel_period]

st.title(":material/work: Job Market")
st.caption(f"Sample dataset: {len(df):,} rows | Market data: {len(ct_filtered)} country-year rows")
st.divider()

st.info(
    ":material/info: **Two data sources are shown:**  \n"
    "**Sample Jobs** (50,000 rows) — individual job postings.  \n"
    "**Market Data** (country_ai_trends) — broader market aggregate statistics. "
    "These are different populations. Dashed lines = Projected (2025–2026).",
)

tab1, tab2, tab3 = st.tabs(["Sample Jobs", "Market Trends", "Location"])

# ---------------------------------------------------------------------------
# Tab 1 — Sample Jobs
# ---------------------------------------------------------------------------
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("Postings by Year")
            year_data = df.groupby(["posted_year","period_type"]).size().reset_index(name="count")
            fig = px.bar(year_data, x="posted_year", y="count",
                         color="period_type",
                         color_discrete_map={"Historical":"#3b82d4","Projected":"#f59e0b"},
                         height=330)
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                              margin=dict(t=30,b=10), xaxis_title="Year",
                              legend_title="Period")
            st.plotly_chart(fig, key="jm_year_bar")

    with col2:
        with st.container(border=True):
            st.subheader("Postings by Role")
            role_data = df["job_title"].value_counts().reset_index()
            role_data.columns = ["role","count"]
            fig = bar_chart(role_data.sort_values("count"), "count", "role",
                            "Postings by Job Role", orientation="h", height=330)
            st.plotly_chart(fig, key="jm_role_bar")

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            st.subheader("By Industry")
            ind_data = df["industry"].value_counts().reset_index()
            ind_data.columns = ["industry","count"]
            fig = bar_chart(ind_data.sort_values("count"), "count", "industry",
                            "Postings by Industry", orientation="h", height=330)
            st.plotly_chart(fig, key="jm_ind_bar")

    with col4:
        with st.container(border=True):
            st.subheader("By Company Type")
            ct_data = df["company_type"].value_counts().reset_index()
            ct_data.columns = ["company_type","count"]
            fig = bar_chart(ct_data.sort_values("count"), "count", "company_type",
                            "Postings by Company Type", orientation="h", height=330)
            st.plotly_chart(fig, key="jm_ctype_bar")

    with st.container(border=True):
        st.subheader("Country x Year Heatmap (sample postings)")
        pivot = df.groupby(["country","posted_year"]).size().reset_index(name="count")
        fig = heatmap_chart(pivot, "posted_year", "country", "count",
                            "Job Postings by Country x Year", height=350)
        st.plotly_chart(fig, key="jm_heatmap")

# ---------------------------------------------------------------------------
# Tab 2 — Market Trends
# ---------------------------------------------------------------------------
with tab2:
    st.caption("Source: country_ai_trends.csv — market-level aggregates. "
               "Dashed = Projected. NOT identical to 50k sample.")

    col5, col6 = st.columns(2)
    with col5:
        with st.container(border=True):
            st.subheader("Total Market AI Jobs by Country & Year")
            fig = line_chart(ct_filtered, "year", "total_ai_jobs", "country",
                             "Market AI Jobs Trend", height=360, period_dashes=True)
            st.plotly_chart(fig, key="jm_mkt_jobs")

    with col6:
        with st.container(border=True):
            st.subheader("Market Avg Salary by Country & Year")
            fig = line_chart(ct_filtered, "year", "avg_salary_usd", "country",
                             "Market Avg Salary Trend", height=360, period_dashes=True)
            st.plotly_chart(fig, key="jm_mkt_sal")

    with st.container(border=True):
        st.subheader("Market Data Table")
        st.dataframe(
            ct_filtered[["country","year","total_ai_jobs","avg_salary_usd",
                          "remote_percentage","top_skill","period_type"]]
            .sort_values(["country","year"]),
            hide_index=True
        )

# ---------------------------------------------------------------------------
# Tab 3 — Location
# ---------------------------------------------------------------------------
with tab3:
    col7, col8 = st.columns(2)
    with col7:
        with st.container(border=True):
            st.subheader("Top 15 Cities (Onsite + Hybrid)")
            city_data = (
                df[df["city"] != "Remote"]["city"]
                .value_counts().head(15).reset_index()
            )
            city_data.columns = ["city","count"]
            fig = bar_chart(city_data.sort_values("count"), "count", "city",
                            "Top Cities", orientation="h", height=400)
            st.plotly_chart(fig, key="jm_city_bar")

    with col8:
        with st.container(border=True):
            st.subheader("Postings by Country")
            cnt_data = df["country"].value_counts().reset_index()
            cnt_data.columns = ["country","count"]
            fig = bar_chart(cnt_data.sort_values("count"), "count", "country",
                            "Sample Postings by Country", orientation="h", height=400)
            st.plotly_chart(fig, key="jm_cnt_bar")
