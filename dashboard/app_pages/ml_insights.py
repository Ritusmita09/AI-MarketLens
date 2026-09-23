"""ML Insights page — AI MarketLens Streamlit Dashboard."""
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from dashboard.utils.data import load_jobs

jobs = load_jobs()

st.title(":material/model_training: ML Insights")
st.divider()

st.warning(
    ":material/science: **Educational Demonstration:** "
    "This dataset is synthetically generated with near-uniform distributions. "
    "The models below demonstrate ML workflows on this data. "
    "Results should NOT be interpreted as real-world salary forecasts. "
    "Only `experience_level` carries meaningful salary signal in this dataset.",
)

# ---------------------------------------------------------------------------
# Prepare ML data
# ---------------------------------------------------------------------------
@st.cache_data
def prepare_ml_data():
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.preprocessing import LabelEncoder

    df = jobs[jobs["period_type"] == "Historical"].copy()

    TARGET = "salary_mid"

    # Feature columns (no leakage)
    cat_cols = ["experience_level","country","industry","company_type",
                "company_size","remote_type","job_title","role_category"]
    num_cols = ["posted_year"]

    X_df = df[cat_cols + num_cols].copy()
    for c in cat_cols:
        le = LabelEncoder()
        X_df[c] = le.fit_transform(X_df[c].astype(str))

    X = X_df.values
    y = df[TARGET].values
    feature_names = cat_cols + num_cols

    strat = df["experience_level"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=strat)

    # Baseline: experience only
    exp_map = {"Entry":0, "Mid":1, "Senior":2}
    X_base = df["experience_level"].map(exp_map).values.reshape(-1,1)
    X_base_tr, X_base_te, y_base_tr, y_base_te = train_test_split(
        X_base, y, test_size=0.2, random_state=42, stratify=strat)

    def fit_eval(model, Xtr, ytr, Xte, yte, name):
        model.fit(Xtr, ytr)
        preds = model.predict(Xte)
        return {
            "name":  name,
            "MAE":   round(mean_absolute_error(yte, preds), 0),
            "RMSE":  round(np.sqrt(mean_squared_error(yte, preds)), 0),
            "R2":    round(r2_score(yte, preds), 4),
            "preds": preds,
            "model": model,
        }

    results = [
        fit_eval(LinearRegression(), X_base_tr, y_base_tr, X_base_te, y_base_te,
                 "Linear Regression (baseline — experience only)"),
        fit_eval(LinearRegression(), X_train, y_train, X_test, y_test,
                 "Linear Regression (full features)"),
        fit_eval(RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
                 X_train, y_train, X_test, y_test, "Random Forest"),
        fit_eval(GradientBoostingRegressor(n_estimators=100, random_state=42),
                 X_train, y_train, X_test, y_test, "Gradient Boosting"),
    ]
    return results, y_test, feature_names

with st.spinner("Training salary models on historical data..."):
    try:
        ml_results, y_test_vals, feature_names = prepare_ml_data()
        ml_ok = True
    except Exception as e:
        st.error(f"ML training error: {e}")
        ml_ok = False

if ml_ok:
    # ---------------------------------------------------------------------------
    # Model comparison table
    # ---------------------------------------------------------------------------
    st.subheader("Model Comparison (trained on Historical 2020–2024 only)")
    comparison_df = pd.DataFrame([
        {"Model": r["name"], "MAE ($)": f"${r['MAE']:,.0f}",
         "RMSE ($)": f"${r['RMSE']:,.0f}", "R²": r["R2"]}
        for r in ml_results
    ])
    st.dataframe(comparison_df, hide_index=True)

    st.caption(
        "Baseline vs full-feature models are compared. "
        "If R² is similar between baseline and full models, "
        "it confirms that only experience_level carries meaningful salary signal."
    )

    # ---------------------------------------------------------------------------
    # Best model: Predicted vs Actual
    # ---------------------------------------------------------------------------
    best = ml_results[2]  # Random Forest
    st.subheader(f"Predicted vs Actual — {best['name']}")

    fig = px.scatter(
        x=y_test_vals, y=best["preds"],
        labels={"x": "Actual Salary (USD)", "y": "Predicted Salary (USD)"},
        opacity=0.3, title="Predicted vs Actual Salary Midpoint",
        color_discrete_sequence=["#3b82d4"],
        height=400,
    )
    lim = [min(y_test_vals.min(), best["preds"].min()),
           max(y_test_vals.max(), best["preds"].max())]
    fig.add_trace(go.Scatter(x=lim, y=lim, mode="lines",
                             line=dict(color="red", width=1.5, dash="dash"),
                             name="Perfect prediction"))
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(t=40,b=20))
    st.plotly_chart(fig, key="ml_scatter")

    # ---------------------------------------------------------------------------
    # Feature importance (Random Forest)
    # ---------------------------------------------------------------------------
    rf_model = best["model"]
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": rf_model.feature_importances_,
    }).sort_values("importance", ascending=True)

    st.subheader("Feature Importance (Random Forest)")
    fig2 = px.bar(
        importance_df, x="importance", y="feature", orientation="h",
        title="Feature Importance — Random Forest (salary_mid target)",
        color_discrete_sequence=["#3b82d4"], height=400,
    )
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(t=40,b=10))
    st.plotly_chart(fig2, key="ml_importance")

    st.info(
        ":material/info: In a synthetic uniformly-distributed dataset, "
        "experience_level will dominate feature importance. "
        "This is expected and does not reflect real-world complexity."
    )

    # ---------------------------------------------------------------------------
    # Salary predictor
    # ---------------------------------------------------------------------------
    st.subheader(":material/calculate: Salary Predictor (Educational)")
    st.caption("Uses Random Forest model trained on historical data.")

    col1, col2, col3 = st.columns(3)
    with col1:
        exp_input = st.selectbox("Experience Level", ["Entry","Mid","Senior"])
    with col2:
        country_input = st.selectbox("Country", sorted(jobs["country"].unique()))
    with col3:
        industry_input = st.selectbox("Industry", sorted(jobs["industry"].unique()))

    col4, col5, col6 = st.columns(3)
    with col4:
        ctype_input  = st.selectbox("Company Type", sorted(jobs["company_type"].unique()))
    with col5:
        csize_input  = st.selectbox("Company Size", sorted(jobs["company_size"].unique()))
    with col6:
        remote_input = st.selectbox("Remote Type", ["Remote","Hybrid","Onsite"])
    role_input  = st.selectbox("Job Role", sorted(jobs["job_title"].unique()))

    if st.button("Predict Salary", type="primary"):
        from sklearn.preprocessing import LabelEncoder
        from sklearn.ensemble import RandomForestRegressor

        @st.cache_resource
        def get_full_rf():
            df = jobs[jobs["period_type"] == "Historical"].copy()
            cat_cols = ["experience_level","country","industry","company_type",
                        "company_size","remote_type","job_title","role_category"]
            num_cols = ["posted_year"]
            encoders = {}
            X_df = df[cat_cols + num_cols].copy()
            for c in cat_cols:
                le = LabelEncoder().fit(df[c].astype(str))
                encoders[c] = le
                X_df[c] = le.transform(X_df[c].astype(str))
            model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            model.fit(X_df.values, df["salary_mid"].values)
            return model, encoders

        rf_prod, encs = get_full_rf()
        role_cat = jobs[jobs["job_title"]==role_input]["role_category"].iloc[0]
        input_vals = []
        cat_in = {
            "experience_level": exp_input,
            "country": country_input,
            "industry": industry_input,
            "company_type": ctype_input,
            "company_size": csize_input,
            "remote_type": remote_input,
            "job_title": role_input,
            "role_category": role_cat,
        }
        for c in ["experience_level","country","industry","company_type",
                  "company_size","remote_type","job_title","role_category"]:
            try:
                val = encs[c].transform([cat_in[c]])[0]
            except Exception:
                val = 0
            input_vals.append(val)
        input_vals.append(2022)  # median year
        pred = rf_prod.predict([input_vals])[0]
        st.success(f"**Predicted Salary Midpoint: ${pred:,.0f} USD**  "
                   f"(estimated range: ${pred*0.85:,.0f} – ${pred*1.15:,.0f})")
        st.caption(
            ":material/warning: This is a demonstration on synthetic data only. "
            "Do not use this as a real salary estimate."
        )
