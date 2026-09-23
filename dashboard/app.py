"""
app.py — Main entry point for AI MarketLens Streamlit Dashboard.
Run from the dashboard/ directory: streamlit run app.py
Or from project root: streamlit run dashboard/app.py
"""
import sys
from pathlib import Path
import streamlit as st

# Ensure project root is on path
_APP_DIR     = Path(__file__).resolve().parent
_PROJECT_ROOT = _APP_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

st.set_page_config(
    page_title="AI MarketLens",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Multi-page navigation using st.navigation + st.Page
# ---------------------------------------------------------------------------
pages = [
    st.Page("app_pages/overview.py",      title="Overview",            icon=":material/dashboard:"),
    st.Page("app_pages/salary.py",        title="Salary Intelligence", icon=":material/payments:"),
    st.Page("app_pages/job_market.py",    title="Job Market",          icon=":material/work:"),
    st.Page("app_pages/skills.py",        title="Skills Intelligence", icon=":material/psychology:"),
    st.Page("app_pages/remote_work.py",   title="Remote Work",         icon=":material/home_work:"),
    st.Page("app_pages/ml_insights.py",   title="ML Insights",         icon=":material/model_training:"),
    st.Page("app_pages/data_explorer.py", title="Data Explorer",       icon=":material/table:"),
    st.Page("app_pages/methodology.py",   title="Methodology",         icon=":material/info:"),
]

pg = st.navigation(pages)

# Sidebar brand header
with st.sidebar:
    st.markdown("### :material/analytics: AI MarketLens")
    st.caption("AI-Powered Global Job Market Intelligence")
    st.divider()

pg.run()
