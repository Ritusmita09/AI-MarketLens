"""
build_notebook.py
-----------------
Script that appends sections 12-26 to the master notebook.
Run from project root: python build_notebook.py
"""
import json
from pathlib import Path

nb_path = Path("notebooks/AI_MarketLens_Master.ipynb")
nb = json.loads(nb_path.read_text(encoding="utf-8"))


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [source],
    }


new_cells = []

# ============================================================
# Section 12 — Job Market Analysis
# ============================================================
new_cells.append(md(
    "---\n## 12. Job Market Analysis\n\n### Postings by Country and Year (Heatmap)"
))
new_cells.append(code(
    "country_year = jobs.groupby(['country','posted_year']).size().reset_index(name='count')\n"
    "pivot = country_year.pivot(index='country', columns='posted_year', values='count')\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(12, 4))\n"
    "sns.heatmap(pivot, annot=True, fmt=',d', cmap='Blues', linewidths=0.5, ax=ax,\n"
    "            cbar_kws={'label':'Job Count'})\n"
    "ax.set_title('Job Postings by Country and Year', fontweight='bold')\n"
    "plt.tight_layout(); plt.show()\n"
))
new_cells.append(code(
    "# P. City distribution (excluding city='Remote' entries)\n"
    "city_counts = jobs[jobs['city'] != 'Remote']['city'].value_counts().head(20)\n"
    "fig, ax = plt.subplots(figsize=(10, 6))\n"
    "city_counts.sort_values().plot.barh(ax=ax, color=HIST_COLOR)\n"
    "ax.set_title('P. Top 20 Cities by Job Postings (Onsite/Hybrid only)', fontweight='bold')\n"
    "ax.set_xlabel('Count')\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 13 — Salary Analysis
# ============================================================
new_cells.append(md("---\n## 13. Salary Analysis"))
new_cells.append(code(
    "# K. Salary by experience level\n"
    "order = ['Entry','Mid','Senior']\n"
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n"
    "\n"
    "jobs.boxplot(column='salary_mid', by='experience_level', ax=axes[0], order=order)\n"
    "axes[0].set_title('K. Salary by Experience Level', fontweight='bold')\n"
    "axes[0].set_xlabel('Experience Level')\n"
    "axes[0].set_ylabel('Salary Midpoint (USD)')\n"
    "axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "plt.sca(axes[0]); plt.title('K. Salary by Experience Level')\n"
    "\n"
    "salary_exp = jobs.groupby('experience_level')['salary_mid'].mean().reindex(order)\n"
    "axes[1].bar(salary_exp.index, salary_exp.values, color=[PROJ_COLOR, HIST_COLOR, '#7c5cd8'])\n"
    "axes[1].set_title('Mean Salary by Experience Level', fontweight='bold')\n"
    "axes[1].set_ylabel('Mean Salary Midpoint (USD)')\n"
    "axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "for i,(label,val) in enumerate(salary_exp.items()):\n"
    "    axes[1].text(i, val+500, f'${val:,.0f}', ha='center', fontsize=10)\n"
    "\n"
    "plt.suptitle('')\n"
    "plt.tight_layout(); plt.show()\n"
    "\n"
    "print('Mean salary_mid by experience_level:')\n"
    "print(jobs.groupby('experience_level')['salary_mid'].agg(['mean','median','std']).round(0).reindex(order))\n"
))
new_cells.append(code(
    "# L. Salary by country\n"
    "order_c = jobs.groupby('country')['salary_mid'].median().sort_values(ascending=False).index\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "jobs.boxplot(column='salary_mid', by='country', ax=ax, order=order_c)\n"
    "ax.set_title('L. Salary by Country', fontweight='bold')\n"
    "ax.set_xlabel('Country'); ax.set_ylabel('Salary Midpoint (USD)')\n"
    "ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "plt.suptitle(''); plt.tight_layout(); plt.show()\n"
    "print('Mean salary_mid by country:')\n"
    "print(jobs.groupby('country')['salary_mid'].agg(['mean','median']).round(0).sort_values('mean',ascending=False))\n"
))
new_cells.append(code(
    "# M. Salary by job role  N. Salary by industry  O. Salary by remote type\n"
    "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n"
    "for ax, col, title in [\n"
    "    (axes[0], 'job_title',   'M. Salary by Role'),\n"
    "    (axes[1], 'industry',    'N. Salary by Industry'),\n"
    "    (axes[2], 'remote_type', 'O. Salary by Remote Type'),\n"
    "]:\n"
    "    order_v = jobs.groupby(col)['salary_mid'].median().sort_values(ascending=False).index\n"
    "    jobs.boxplot(column='salary_mid', by=col, ax=ax, order=order_v)\n"
    "    ax.set_title(title, fontweight='bold')\n"
    "    ax.set_xlabel('')\n"
    "    ax.set_ylabel('Salary Midpoint (USD)')\n"
    "    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "    plt.setp(ax.xaxis.get_ticklabels(), rotation=20, ha='right')\n"
    "plt.suptitle(''); plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 14 — Country Analysis
# ============================================================
new_cells.append(md("---\n## 14. Country Analysis\n\n### T. Country AI Market Trends"))
new_cells.append(code(
    "ct = country_trends_clean.copy()\n"
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
    "\n"
    "for country_name in ct['country'].unique():\n"
    "    sub = ct[ct['country']==country_name].sort_values('year')\n"
    "    hist_sub = sub[sub['period_type']=='Historical']\n"
    "    proj_sub = sub[sub['period_type']=='Projected']\n"
    "    line = axes[0].plot(hist_sub['year'], hist_sub['total_ai_jobs'], marker='o', label=country_name)\n"
    "    col = line[0].get_color()\n"
    "    axes[0].plot(proj_sub['year'], proj_sub['total_ai_jobs'], marker='s', linestyle='--', color=col)\n"
    "\n"
    "axes[0].set_title('T. Total AI Jobs by Country & Year', fontweight='bold')\n"
    "axes[0].set_xlabel('Year'); axes[0].set_ylabel('Total AI Jobs')\n"
    "axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x/1000)}k'))\n"
    "axes[0].legend(fontsize=8)\n"
    "\n"
    "for country_name in ct['country'].unique():\n"
    "    sub = ct[ct['country']==country_name].sort_values('year')\n"
    "    hist_sub = sub[sub['period_type']=='Historical']\n"
    "    proj_sub = sub[sub['period_type']=='Projected']\n"
    "    line = axes[1].plot(hist_sub['year'], hist_sub['avg_salary_usd'], marker='o', label=country_name)\n"
    "    col = line[0].get_color()\n"
    "    axes[1].plot(proj_sub['year'], proj_sub['avg_salary_usd'], marker='s', linestyle='--', color=col)\n"
    "\n"
    "axes[1].set_title('Country Avg Salary by Year', fontweight='bold')\n"
    "axes[1].set_xlabel('Year'); axes[1].set_ylabel('Avg Salary (USD)')\n"
    "axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "axes[1].legend(fontsize=8)\n"
    "plt.tight_layout(); plt.show()\n"
))
new_cells.append(md("### U. Remote Work % by Country and Year"))
new_cells.append(code(
    "fig, ax = plt.subplots(figsize=(11, 5))\n"
    "for country_name in ct['country'].unique():\n"
    "    sub = ct[ct['country']==country_name].sort_values('year')\n"
    "    hist_sub = sub[sub['period_type']=='Historical']\n"
    "    proj_sub = sub[sub['period_type']=='Projected']\n"
    "    line = ax.plot(hist_sub['year'], hist_sub['remote_percentage'], marker='o', label=country_name)\n"
    "    col = line[0].get_color()\n"
    "    ax.plot(proj_sub['year'], proj_sub['remote_percentage'], marker='s', linestyle='--', color=col)\n"
    "ax.set_title('U. Remote Work % by Country & Year (dashed = Projected)', fontweight='bold')\n"
    "ax.set_xlabel('Year'); ax.set_ylabel('Remote %'); ax.set_ylim(0,100)\n"
    "ax.legend(); plt.tight_layout(); plt.show()\n"
    "\n"
    "pivot_r = ct.pivot(index='country', columns='year', values='remote_percentage')\n"
    "fig, ax = plt.subplots(figsize=(11, 4))\n"
    "sns.heatmap(pivot_r, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5, ax=ax)\n"
    "ax.set_title('Remote % Heatmap by Country x Year', fontweight='bold')\n"
    "plt.tight_layout(); plt.show()\n"
))
new_cells.append(md("### V. Top Skill by Country and Year"))
new_cells.append(code(
    "top_skill_pivot = ct.pivot(index='country', columns='year', values='top_skill')\n"
    "fig, ax = plt.subplots(figsize=(13, 4))\n"
    "ax.set_xlim(0, len(top_skill_pivot.columns))\n"
    "ax.set_ylim(0, len(top_skill_pivot.index))\n"
    "ax.set_xticks([i+0.5 for i in range(len(top_skill_pivot.columns))])\n"
    "ax.set_xticklabels(top_skill_pivot.columns)\n"
    "ax.set_yticks([i+0.5 for i in range(len(top_skill_pivot.index))])\n"
    "ax.set_yticklabels(top_skill_pivot.index)\n"
    "for i, country_name in enumerate(top_skill_pivot.index):\n"
    "    for j, year_val in enumerate(top_skill_pivot.columns):\n"
    "        skill_val = top_skill_pivot.loc[country_name, year_val]\n"
    "        ax.text(j+0.5, i+0.5, str(skill_val), ha='center', va='center', fontsize=9, fontweight='bold')\n"
    "        ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True,\n"
    "                     facecolor='#eff6ff', edgecolor='#e5e7eb', linewidth=0.5))\n"
    "ax.set_title('V. Top Skill by Country and Year', fontweight='bold')\n"
    "ax.set_xlabel('Year'); ax.set_ylabel('Country')\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 15 — Remote Work Analysis
# ============================================================
new_cells.append(md("---\n## 15. Remote Work Analysis"))
new_cells.append(code(
    "fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n"
    "\n"
    "remote_year = jobs.groupby('posted_year')['remote_flag'].mean().mul(100)\n"
    "axes[0].plot(remote_year.index, remote_year.values, marker='o', color=HIST_COLOR)\n"
    "axes[0].axvline(2024.5, color='red', linestyle='--', alpha=0.5, label='Hist/Proj boundary')\n"
    "axes[0].set_title('Remote Jobs % by Year (sample)', fontweight='bold')\n"
    "axes[0].set_ylabel('% Remote'); axes[0].legend()\n"
    "\n"
    "remote_country = jobs.groupby('country')['remote_flag'].mean().mul(100).sort_values(ascending=False)\n"
    "axes[1].bar(remote_country.index, remote_country.values, color=HIST_COLOR)\n"
    "axes[1].set_title('Remote Jobs % by Country', fontweight='bold')\n"
    "axes[1].set_ylabel('% Remote')\n"
    "\n"
    "remote_exp = jobs.groupby('experience_level')['remote_flag'].mean().mul(100).reindex(['Entry','Mid','Senior'])\n"
    "axes[2].bar(remote_exp.index, remote_exp.values, color=PROJ_COLOR)\n"
    "axes[2].set_title('Remote Jobs % by Experience', fontweight='bold')\n"
    "axes[2].set_ylabel('% Remote')\n"
    "\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 16 — Skills Intelligence
# ============================================================
new_cells.append(md(
    "---\n## 16. Skills Intelligence\n\n"
    "> **Note:** skills_demand cannot be directly joined to ai_jobs (only 4.1% job_id overlap — dataset artifact). "
    "Skills are analysed as an independent dataset."
))
new_cells.append(code(
    "# Q. Skill frequency\n"
    "skill_freq = skills_clean['skill'].value_counts()\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "skill_freq.sort_values().plot.barh(ax=ax, color=HIST_COLOR)\n"
    "ax.set_title('Q. Skill Demand (skills_demand — independent)', fontweight='bold')\n"
    "ax.set_xlabel('Count')\n"
    "for i, v in enumerate(skill_freq.sort_values().values):\n"
    "    ax.text(v+100, i, f'{v:,}', va='center', fontsize=9)\n"
    "plt.tight_layout(); plt.show()\n"
))
new_cells.append(code(
    "# R. Skill category  S. Skill level\n"
    "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n"
    "for ax, col, title in [\n"
    "    (axes[0], 'skill_category', 'R. Skill Category Distribution'),\n"
    "    (axes[1], 'skill_level',    'S. Skill Level Distribution'),\n"
    "]:\n"
    "    counts = skills_clean[col].value_counts()\n"
    "    ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%',\n"
    "           colors=sns.color_palette('tab10', len(counts)), startangle=90)\n"
    "    ax.set_title(title, fontweight='bold')\n"
    "plt.tight_layout(); plt.show()\n"
    "print(skill_summary.to_string(index=False))\n"
))

# ============================================================
# Section 17 — Historical vs Projected
# ============================================================
new_cells.append(md("---\n## 17. Historical vs Projected Analysis"))
new_cells.append(code(
    "hist_jobs = jobs[jobs['period_type'] == 'Historical']\n"
    "proj_jobs  = jobs[jobs['period_type'] == 'Projected']\n"
    "\n"
    "print(f'Historical rows (2020-2024) : {len(hist_jobs):,}  ({100*len(hist_jobs)/len(jobs):.1f}%)')\n"
    "print(f'Projected rows  (2025-2026) : {len(proj_jobs):,}  ({100*len(proj_jobs)/len(jobs):.1f}%)')\n"
    "\n"
    "print('\\nSalary midpoint comparison:')\n"
    "for period, group in jobs.groupby('period_type'):\n"
    "    print(f'  {period}: mean=${group[\"salary_mid\"].mean():,.0f}  median=${group[\"salary_mid\"].median():,.0f}')\n"
    "\n"
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n"
    "for ax, period, color in [(axes[0],'Historical',HIST_COLOR),(axes[1],'Projected',PROJ_COLOR)]:\n"
    "    subset = jobs[jobs['period_type']==period]\n"
    "    counts = subset['job_title'].value_counts().sort_values()\n"
    "    ax.barh(counts.index, counts.values, color=color)\n"
    "    ax.set_title(f'Job Role Distribution - {period}', fontweight='bold')\n"
    "    ax.set_xlabel('Count')\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 18 — Statistical Analysis
# ============================================================
new_cells.append(md("---\n## 18. Statistical Analysis\n\nAll tests use alpha = 0.05."))
new_cells.append(code(
    "from scipy.stats import normaltest, kruskal\n"
    "import pandas as pd\n"
    "alpha = 0.05\n"
    "\n"
    "stat_n, p_n = normaltest(jobs['salary_mid'])\n"
    "print(\"1. Normality (D'Agostino-Pearson) on salary_mid:\")\n"
    "print(f'   stat={stat_n:.2f}, p={p_n:.4e}')\n"
    "print(f'   -> salary_mid is {\"NOT normally distributed\" if p_n<alpha else \"approximately normal\"}')\n"
    "print('   -> Using Kruskal-Wallis (non-parametric) for group comparisons.\\n')\n"
    "\n"
    "tests = [\n"
    "    ('experience_level', 'Salary vs Experience Level'),\n"
    "    ('country',          'Salary vs Country'),\n"
    "    ('industry',         'Salary vs Industry'),\n"
    "    ('remote_type',      'Salary vs Remote Type'),\n"
    "    ('role_category',    'Salary vs Role Category'),\n"
    "    ('company_type',     'Salary vs Company Type'),\n"
    "    ('company_size',     'Salary vs Company Size'),\n"
    "]\n"
    "\n"
    "test_results = []\n"
    "for col, label in tests:\n"
    "    groups = [g['salary_mid'].values for _, g in jobs.groupby(col)]\n"
    "    H, p = kruskal(*groups)\n"
    "    sig = p < alpha\n"
    "    result_str = 'SIGNIFICANT' if sig else 'not significant'\n"
    "    print(f'{label:<35} H={H:8.2f}  p={p:.4e}  [{result_str}]')\n"
    "    test_results.append({'Factor': label, 'H': round(H,2), 'p-value': round(p,6), 'Significant (p<0.05)': sig})\n"
    "\n"
    "results_table = pd.DataFrame(test_results)\n"
    "print()\n"
    "print(results_table.to_string(index=False))\n"
))

# ============================================================
# Section 19 — Machine Learning — Salary Regression
# ============================================================
new_cells.append(md(
    "---\n## 19. Machine Learning\n\n### A. Salary Regression\n\n"
    "> **Educational Note:** This dataset is synthetically generated. Only `experience_level` "
    "carries meaningful salary signal. All models serve as demonstrations."
))
new_cells.append(code(
    "from src.feature_engineering import build_ml_feature_matrix, add_salary_features, add_experience_numeric, add_period_type\n"
    "from sklearn.model_selection import train_test_split\n"
    "from sklearn.linear_model import LinearRegression\n"
    "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n"
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n"
    "import numpy as np\n"
    "\n"
    "# Prepare ML dataset from historical data only\n"
    "jobs_ml = jobs_clean.copy()\n"
    "jobs_ml = add_salary_features(jobs_ml)\n"
    "jobs_ml = add_experience_numeric(jobs_ml)\n"
    "jobs_ml = add_period_type(jobs_ml)\n"
    "jobs_hist_ml = jobs_ml[jobs_ml['period_type'] == 'Historical'].copy()\n"
    "TARGET = 'salary_mid'\n"
    "\n"
    "X_full, y, features = build_ml_feature_matrix(jobs_hist_ml, target=TARGET)\n"
    "print(f'Training rows: {len(jobs_hist_ml):,} (Historical 2020-2024 only)')\n"
    "print(f'Feature matrix: {X_full.shape}')\n"
    "print(f'Features: {features}')\n"
))
new_cells.append(code(
    "# Train/test split — stratify on experience_level for balance\n"
    "strat_col = jobs_hist_ml['experience_level'].values\n"
    "X_train, X_test, y_train, y_test = train_test_split(\n"
    "    X_full, y, test_size=0.2, random_state=42, stratify=strat_col)\n"
    "\n"
    "# BASELINE: experience_level encoded as 0/1/2 only\n"
    "exp_map = {'Entry':0,'Mid':1,'Senior':2}\n"
    "X_base = jobs_hist_ml['experience_level'].map(exp_map).values.reshape(-1,1)\n"
    "X_base_train, X_base_test, y_base_train, y_base_test = train_test_split(\n"
    "    X_base, y, test_size=0.2, random_state=42, stratify=strat_col)\n"
    "\n"
    "print(f'Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}')\n"
))
new_cells.append(code(
    "def evaluate_model(model, X_tr, y_tr, X_te, y_te, label):\n"
    "    model.fit(X_tr, y_tr)\n"
    "    preds = model.predict(X_te)\n"
    "    mae  = mean_absolute_error(y_te, preds)\n"
    "    rmse = np.sqrt(mean_squared_error(y_te, preds))\n"
    "    r2   = r2_score(y_te, preds)\n"
    "    print(f'  {label:<42} MAE=${mae:>8,.0f}  RMSE=${rmse:>8,.0f}  R2={r2:.4f}')\n"
    "    return {'label':label, 'MAE':round(mae,0), 'RMSE':round(rmse,0), 'R2':round(r2,4),\n"
    "            'model':model, 'preds':preds, 'y_test':y_te}\n"
    "\n"
    "print('=== BASELINE: experience_level only ===')\n"
    "lr_base = evaluate_model(LinearRegression(), X_base_train, y_base_train, X_base_test, y_base_test, 'LinearRegression (baseline)')\n"
    "\n"
    "print()\n"
    "print('=== FULL FEATURE MODELS ===')\n"
    "lr_full = evaluate_model(LinearRegression(),                                        X_train, y_train, X_test, y_test, 'LinearRegression (full features)')\n"
    "rf_full = evaluate_model(RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=-1), X_train, y_train, X_test, y_test, 'RandomForest (full features)')\n"
    "gb_full = evaluate_model(GradientBoostingRegressor(n_estimators=100,random_state=42),       X_train, y_train, X_test, y_test, 'GradientBoosting (full features)')\n"
))
new_cells.append(code(
    "import pandas as pd\n"
    "model_comparison = pd.DataFrame([\n"
    "    {'Model': lr_base['label'], 'Feature Set': 'experience only', 'MAE': lr_base['MAE'], 'RMSE': lr_base['RMSE'], 'R2': lr_base['R2']},\n"
    "    {'Model': lr_full['label'], 'Feature Set': 'all valid features', 'MAE': lr_full['MAE'], 'RMSE': lr_full['RMSE'], 'R2': lr_full['R2']},\n"
    "    {'Model': rf_full['label'], 'Feature Set': 'all valid features', 'MAE': rf_full['MAE'], 'RMSE': rf_full['RMSE'], 'R2': rf_full['R2']},\n"
    "    {'Model': gb_full['label'], 'Feature Set': 'all valid features', 'MAE': gb_full['MAE'], 'RMSE': gb_full['RMSE'], 'R2': gb_full['R2']},\n"
    "])\n"
    "print('Model Comparison:')\n"
    "print(model_comparison[['Model','Feature Set','MAE','RMSE','R2']].to_string(index=False))\n"
))

# ============================================================
# Section 20 — Model Evaluation
# ============================================================
new_cells.append(md("---\n## 20. Model Evaluation — Residual Analysis"))
new_cells.append(code(
    "best_model_result = rf_full\n"
    "y_pred_best  = best_model_result['preds']\n"
    "y_test_vals  = best_model_result['y_test'].values\n"
    "residuals    = y_test_vals - y_pred_best\n"
    "\n"
    "fig, axes = plt.subplots(1, 3, figsize=(16, 4))\n"
    "\n"
    "# Predicted vs Actual\n"
    "axes[0].scatter(y_test_vals, y_pred_best, alpha=0.3, color=HIST_COLOR, s=5)\n"
    "lim = [min(y_test_vals.min(), y_pred_best.min()), max(y_test_vals.max(), y_pred_best.max())]\n"
    "axes[0].plot(lim, lim, color='red', linewidth=1.5)\n"
    "axes[0].set_title('Predicted vs Actual (Random Forest)', fontweight='bold')\n"
    "axes[0].set_xlabel('Actual'); axes[0].set_ylabel('Predicted')\n"
    "axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "\n"
    "# Residuals histogram\n"
    "axes[1].hist(residuals, bins=60, color=HIST_COLOR, edgecolor='white', alpha=0.85)\n"
    "axes[1].axvline(0, color='red', linewidth=1.5)\n"
    "axes[1].set_title('Residual Distribution', fontweight='bold')\n"
    "axes[1].set_xlabel('Residual'); axes[1].set_ylabel('Count')\n"
    "axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "\n"
    "# Residuals by experience level\n"
    "exp_col = jobs_hist_ml.loc[best_model_result['y_test'].index, 'experience_level']\n"
    "exp_order = ['Entry','Mid','Senior']\n"
    "for i, exp in enumerate(exp_order):\n"
    "    mask = exp_col == exp\n"
    "    if mask.sum() > 0:\n"
    "        axes[2].scatter([i]*mask.sum(), residuals[mask.values], alpha=0.3, s=5, label=exp)\n"
    "axes[2].axhline(0, color='red', linewidth=1)\n"
    "axes[2].set_xticks([0,1,2]); axes[2].set_xticklabels(exp_order)\n"
    "axes[2].set_title('Residuals by Experience Level', fontweight='bold')\n"
    "axes[2].set_ylabel('Residual')\n"
    "axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 21 — Feature Importance
# ============================================================
new_cells.append(md("---\n## 21. Feature Importance / Model Interpretation"))
new_cells.append(code(
    "rf_model = rf_full['model']\n"
    "feat_importance = pd.Series(rf_model.feature_importances_, index=features).sort_values(ascending=False)\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(10, max(4, len(feat_importance)*0.38)))\n"
    "feat_importance.sort_values().plot.barh(ax=ax, color=HIST_COLOR)\n"
    "ax.set_title('Random Forest Feature Importance (target: salary_mid)', fontweight='bold')\n"
    "ax.set_xlabel('Importance Score')\n"
    "plt.tight_layout(); plt.show()\n"
    "\n"
    "print('Top features by importance:')\n"
    "print(feat_importance.head(10).round(4).to_string())\n"
    "print()\n"
    "print('Interpretation:')\n"
    "print('  Experience-level features dominate due to synthetic uniform distribution.')\n"
    "print('  In real data, geography and industry would also contribute meaningfully.')\n"
))

# ============================================================
# Section 22 — Clustering
# ============================================================
new_cells.append(md("---\n## 22. Clustering\n\n### B. Unsupervised Clustering — Job Profile Segmentation"))
new_cells.append(code(
    "from sklearn.cluster import KMeans\n"
    "from sklearn.preprocessing import StandardScaler\n"
    "from sklearn.metrics import silhouette_score, davies_bouldin_score\n"
    "\n"
    "cluster_features = ['salary_mid', 'experience_numeric', 'remote_flag', 'company_size_numeric']\n"
    "X_clust_raw = jobs[cluster_features].dropna()\n"
    "\n"
    "scaler = StandardScaler()\n"
    "X_clust = scaler.fit_transform(X_clust_raw)\n"
    "\n"
    "k_range = range(2, 9)\n"
    "inertias, silhouettes, dbis = [], [], []\n"
    "\n"
    "for k in k_range:\n"
    "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n"
    "    labels = km.fit_predict(X_clust)\n"
    "    inertias.append(km.inertia_)\n"
    "    silhouettes.append(silhouette_score(X_clust, labels))\n"
    "    dbis.append(davies_bouldin_score(X_clust, labels))\n"
    "\n"
    "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n"
    "axes[0].plot(list(k_range), inertias, marker='o', color=HIST_COLOR)\n"
    "axes[0].set_title('Elbow Method (Inertia)', fontweight='bold')\n"
    "axes[0].set_xlabel('K'); axes[0].set_ylabel('Inertia')\n"
    "\n"
    "axes[1].plot(list(k_range), silhouettes, marker='o', color=PROJ_COLOR)\n"
    "axes[1].set_title('Silhouette Score (higher is better)', fontweight='bold')\n"
    "axes[1].set_xlabel('K'); axes[1].set_ylabel('Silhouette Score')\n"
    "\n"
    "axes[2].plot(list(k_range), dbis, marker='o', color=NEUTRAL)\n"
    "axes[2].set_title('Davies-Bouldin Index (lower is better)', fontweight='bold')\n"
    "axes[2].set_xlabel('K'); axes[2].set_ylabel('DBI')\n"
    "\n"
    "plt.tight_layout(); plt.show()\n"
    "\n"
    "best_k = list(k_range)[silhouettes.index(max(silhouettes))]\n"
    "print(f'Best K by Silhouette: {best_k} (score={max(silhouettes):.4f})')\n"
    "print(f'Best K by DBI       : {list(k_range)[dbis.index(min(dbis))]} (score={min(dbis):.4f})')\n"
))
new_cells.append(code(
    "km_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)\n"
    "cluster_labels = km_final.fit_predict(X_clust)\n"
    "\n"
    "jobs_clust = X_clust_raw.copy()\n"
    "jobs_clust['cluster'] = cluster_labels\n"
    "jobs_clust['experience_level'] = jobs.loc[X_clust_raw.index, 'experience_level'].values\n"
    "\n"
    "cluster_profile = jobs_clust.groupby('cluster').agg(\n"
    "    salary_mean=('salary_mid','mean'),\n"
    "    salary_median=('salary_mid','median'),\n"
    "    count=('salary_mid','count'),\n"
    "    avg_exp=('experience_numeric','mean'),\n"
    "    remote_pct=('remote_flag','mean'),\n"
    "    avg_company_size=('company_size_numeric','mean')\n"
    ").round(2)\n"
    "\n"
    "print(f'Cluster Profile (K={best_k}):')\n"
    "print(cluster_profile.to_string())\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(9, 6))\n"
    "scatter = ax.scatter(\n"
    "    X_clust_raw['salary_mid'], X_clust_raw['experience_numeric'],\n"
    "    c=cluster_labels, cmap='tab10', alpha=0.4, s=5)\n"
    "ax.set_xlabel('Salary Midpoint (USD)')\n"
    "ax.set_ylabel('Experience (0=Entry, 1=Mid, 2=Senior)')\n"
    "ax.set_title(f'Job Clusters (K={best_k}) — Salary vs Experience', fontweight='bold')\n"
    "ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${int(x/1000)}k'))\n"
    "plt.colorbar(scatter, label='Cluster', ax=ax)\n"
    "plt.tight_layout(); plt.show()\n"
))

# ============================================================
# Section 23 — Key Insights
# ============================================================
new_cells.append(md("---\n## 23. Key Insights"))
new_cells.append(code(
    "print('=== KEY INSIGHTS ===')\n"
    "print()\n"
    "print('1. SALARY BY EXPERIENCE')\n"
    "for exp in ['Entry','Mid','Senior']:\n"
    "    grp = jobs[jobs['experience_level']==exp]\n"
    "    print(f'   {exp:<8}: mean=${grp[\"salary_mid\"].mean():>9,.0f}  median=${grp[\"salary_mid\"].median():>9,.0f}')\n"
    "\n"
    "print()\n"
    "print('2. JOB ROLE DISTRIBUTION')\n"
    "for role, pct in jobs['job_title'].value_counts(normalize=True).mul(100).items():\n"
    "    print(f'   {role:<30}: {pct:.1f}%')\n"
    "\n"
    "print()\n"
    "print('3. ROLE CATEGORY SPLIT')\n"
    "for cat, pct in jobs['role_category'].value_counts(normalize=True).mul(100).items():\n"
    "    print(f'   {cat}: {pct:.1f}%')\n"
    "\n"
    "print()\n"
    "print('4. REMOTE WORK (sample dataset)')\n"
    "for rt, pct in jobs['remote_type'].value_counts(normalize=True).mul(100).items():\n"
    "    print(f'   {rt}: {pct:.1f}%')\n"
    "\n"
    "print()\n"
    "print('5. TOP SKILLS (skills_demand)')\n"
    "for skill, cnt in skills_clean['skill'].value_counts().head(5).items():\n"
    "    print(f'   {skill:<20}: {cnt:,}')\n"
    "\n"
    "print()\n"
    "print('6. COUNTRY MARKET HIGHLIGHTS (country_ai_trends)')\n"
    "ct2 = country_trends_clean\n"
    "best_sal = ct2.loc[ct2['avg_salary_usd'].idxmax()]\n"
    "best_jobs = ct2.loc[ct2['total_ai_jobs'].idxmax()]\n"
    "best_rem = ct2.loc[ct2['remote_percentage'].idxmax()]\n"
    "print(f'   Highest avg salary  : {best_sal[\"country\"]} ({best_sal[\"year\"]}) = ${best_sal[\"avg_salary_usd\"]:,}')\n"
    "print(f'   Most AI jobs        : {best_jobs[\"country\"]} ({best_jobs[\"year\"]}) = {best_jobs[\"total_ai_jobs\"]:,}')\n"
    "print(f'   Highest remote %    : {best_rem[\"country\"]} ({best_rem[\"year\"]}) = {best_rem[\"remote_percentage\"]}%')\n"
))

# ============================================================
# Section 24 — Business Recommendations
# ============================================================
new_cells.append(md("---\n## 24. Business Recommendations"))
new_cells.append(md(
    "Based on the analysis, the following recommendations are proposed.\n\n"
    "> **Caveat:** Derived from a synthetic dataset. Validate with real labour market data before operational use.\n\n"
    "**For Job Seekers:**\n"
    "- Advancing from Entry to Senior level is the single most impactful salary lever (~2.3x premium). Invest in experience accumulation.\n"
    "- Cloud skills (AWS, GCP, Azure) and ML frameworks (TensorFlow, PyTorch, Scikit-learn) show equal demand — build breadth across categories.\n"
    "- Remote and Hybrid opportunities are roughly equally available (~33% each), providing significant flexibility.\n\n"
    "**For Employers:**\n"
    "- Offer competitive Senior-level packages. The Senior premium over Entry is approximately 133%.\n"
    "- Hiring talent across all 6 represented countries shows roughly equal supply volumes.\n"
    "- No single industry dominates AI hiring (all 5 industries ~20% each), suggesting broad cross-sector demand.\n\n"
    "**For Policy/Research:**\n"
    "- Country-level AI job growth trends vary year-on-year with no single dominant country.\n"
    "- Remote work market-level adoption averages 56% but fluctuates widely by country and year (25%–84%).\n"
    "- The gap between Projected (2025-2026) and Historical (2020-2024) salary distributions is negligible in this dataset — projections appear to follow the same synthetic generation process."
))

# ============================================================
# Section 25 — Limitations
# ============================================================
new_cells.append(md("---\n## 25. Limitations"))
new_cells.append(md(
    "1. **Synthetic data** — near-uniform distributions reduce real-world applicability of all findings.\n"
    "2. **skills_demand join failure** — only 4.1% job_id overlap; skill-level analysis cannot be enriched with salary/experience/country features.\n"
    "3. **employment_type zero variance** — contract/part-time dynamics unavailable.\n"
    "4. **Future years 2025-2026** — 28.4% of rows are projected synthetic data, not observed.\n"
    "5. **Salary independence** — salary varies meaningfully only with experience_level; geographic and industry effects undetectable.\n"
    "6. **country_ai_trends** — only 42 rows (6 countries x 7 years); insufficient for robust time-series ML.\n"
    "7. **Narrow scope** — 6 countries, 6 roles, 11 skills do not represent the full global AI job market."
))

# ============================================================
# Section 26 — Conclusion
# ============================================================
new_cells.append(md("---\n## 26. Conclusion"))
new_cells.append(md(
    "This notebook completed a full end-to-end analysis pipeline for the AI MarketLens platform:\n\n"
    "- **50,000 job postings** cleaned, feature-engineered, and analysed across 6 countries, 6 roles, 7 years.\n"
    "- **Statistical testing** confirmed `experience_level` is the only significant salary driver in this dataset; country, industry, remote type, and role category effects are not statistically detectable.\n"
    "- **Three regression models** (Linear Regression, Random Forest, Gradient Boosting) were built and compared on historical data.\n"
    "- **Clustering** (K-Means, K=2-8) explored job profile segments primarily structured by salary and experience.\n"
    "- **Skills analysis** (224,605 rows, independent) revealed 11 equally-demanded skills across 3 categories.\n"
    "- **Country market trends** visualised total AI jobs, average salary, remote %, and top skill per country-year.\n\n"
    "Processed datasets are saved to `data/processed/` and `data/exports/` and are ready for Phase 3 dashboard development.\n\n"
    "> **Phase 2 complete.** Next step: Phase 3 — Streamlit and Power BI dashboards."
))

# Validation export section
new_cells.append(md("---\n## Appendix: Export Processed Datasets"))
new_cells.append(code(
    "from src.preprocessing import save_processed, save_exports\n"
    "\n"
    "print('Saving processed datasets...')\n"
    "save_processed(jobs_clean, jobs_enriched, skills_clean, skill_summary, country_trends_clean, verbose=True)\n"
    "\n"
    "print()\n"
    "print('Saving export datasets...')\n"
    "save_exports(jobs_enriched, skills_clean, country_trends_clean, verbose=True)\n"
    "\n"
    "print()\n"
    "print('All datasets saved successfully.')\n"
))

# ============================================================
# Append all cells and save
# ============================================================
nb["cells"].extend(new_cells)
nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"Notebook complete: {len(nb['cells'])} total cells written.")
