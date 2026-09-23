/**
 * app.js — Main application logic for AI MarketLens Web Dashboard
 * Loads JSON data and wires up all charts and interactions.
 */

"use strict";

// ============================================================
// State
// ============================================================
let DATA = {};
let CHARTS = {};

// ============================================================
// Data loading
// ============================================================
async function loadAllData() {
  const files = ["kpis", "salary", "countries", "skills", "roles", "remote", "trends"];
  const results = await Promise.all(
    files.map(f =>
      fetch(`data/${f}.json`)
        .then(r => { if (!r.ok) throw new Error(`${f}.json: ${r.status}`); return r.json(); })
        .then(d => [f, d])
    )
  );
  results.forEach(([key, val]) => { DATA[key] = val; });
}

// ============================================================
// Section navigation
// ============================================================
function initNav() {
  const links  = document.querySelectorAll(".nav-link[data-section]");
  const sections = document.querySelectorAll(".section[id]");

  links.forEach(link => {
    link.addEventListener("click", () => {
      const target = link.dataset.section;
      links.forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      const el = document.getElementById(target);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // Highlight active nav on scroll
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove("active"));
        const link = document.querySelector(`.nav-link[data-section="${entry.target.id}"]`);
        if (link) link.classList.add("active");
      }
    });
  }, { threshold: 0.3 });

  sections.forEach(s => observer.observe(s));
}

// ============================================================
// KPI section
// ============================================================
function buildKPIs() {
  populateKPIs(DATA.kpis);
}

// ============================================================
// Section 1 — Global Job Market
// ============================================================
function buildJobMarket() {
  const trends = DATA.trends;
  const roles  = DATA.roles;

  // Postings by year (sample)
  const yearGroups = {};
  trends.jobs_by_year.forEach(d => {
    yearGroups[d.posted_year] = (yearGroups[d.posted_year] || 0) + d.count;
  });
  const yearLabels = Object.keys(yearGroups).sort();
  const yearCounts = yearLabels.map(y => yearGroups[y]);
  const yearColors = yearLabels.map(y => Number(y) >= 2025 ? PROJ_COLOR : HIST_COLOR);

  makeBarChart("chart-jobs-by-year", yearLabels, yearCounts,
    "Job Postings", { colors: yearColors });

  // Postings by role
  const roleItems = roles.job_title_counts.slice(0, 10);
  makeHBarChart("chart-jobs-by-role",
    roleItems.map(d => d.role),
    roleItems.map(d => d.count),
    "Count",
    PALETTE.slice(0, roleItems.length)
  );
}

// ============================================================
// Section 2 — Salary Intelligence
// ============================================================
function buildSalary() {
  const salary = DATA.salary;

  // Salary by experience (sorted Entry→Mid→Senior)
  const expOrder = ["Entry", "Mid", "Senior"];
  const expData  = expOrder.map(e => salary.by_experience.find(d => d.experience_level === e));
  makeSalaryBar("chart-salary-exp",
    expData.filter(Boolean),
    "experience_level"
  );

  // Salary by country
  makeSalaryBar("chart-salary-country",
    salary.by_country.sort((a, b) => b.avg - a.avg),
    "country"
  );

  // Salary by role
  makeSalaryBar("chart-salary-role",
    salary.by_job_title.sort((a, b) => b.avg - a.avg),
    "job_title"
  );

  // Salary by industry
  makeSalaryBar("chart-salary-industry",
    salary.by_industry.sort((a, b) => b.avg - a.avg),
    "industry"
  );

  // Salary by remote type
  makeSalaryBar("chart-salary-remote",
    salary.by_remote_type,
    "remote_type"
  );
}

// ============================================================
// Section 3 — Skills Intelligence
// ============================================================
function buildSkills() {
  const skills = DATA.skills;

  // Skill frequency (horizontal bar)
  const sortedSkills = [...skills.skill_frequency].sort((a, b) => b.count - a.count);
  makeHBarChart("chart-skill-freq",
    sortedSkills.map(d => d.skill),
    sortedSkills.map(d => d.count),
    "Count",
    PALETTE
  );

  // Skill category donut
  makeDonutChart("chart-skill-cat",
    skills.category_frequency.map(d => d.category),
    skills.category_frequency.map(d => d.count)
  );

  // Skill level donut
  makeDonutChart("chart-skill-level",
    skills.level_frequency.map(d => d.level),
    skills.level_frequency.map(d => d.count)
  );
}

// ============================================================
// Section 4 — Remote Work
// ============================================================
function buildRemote() {
  const remote = DATA.remote;

  // Overall donut
  makeDonutChart("chart-remote-overall",
    remote.overall.map(d => d.remote_type),
    remote.overall.map(d => d.count),
    { colors: [HIST_COLOR, PROJ_COLOR, "#10b981"] }
  );

  // Remote % by country
  const byCt = {};
  remote.by_country.forEach(d => {
    if (!byCt[d.country]) byCt[d.country] = {};
    byCt[d.country][d.remote_type] = d.pct;
  });
  const ctKeys = Object.keys(byCt);
  const ctRemotePct = ctKeys.map(c => byCt[c]["Remote"] || 0);

  makeHBarChart("chart-remote-country",
    ctKeys, ctRemotePct, "Remote %",
    PALETTE.slice(0, ctKeys.length)
  );

  // Remote % by experience
  const byExp = remote.by_experience;
  makeBarChart("chart-remote-exp",
    byExp.map(d => d.experience_level),
    byExp.map(d => d.remote_pct),
    "Remote %",
    { colors: PALETTE[0] }
  );
}

// ============================================================
// Section 5 — Country Trends
// ============================================================
function buildCountryTrends() {
  const ct = DATA.countries.market_by_country_year;

  makeCountryLineChart("chart-market-jobs", ct, "total_ai_jobs", {
    yFormat: v => (v / 1000).toFixed(0) + "k",
  });

  makeCountryLineChart("chart-market-salary", ct, "avg_salary_usd", {
    yFormat: v => "$" + (v / 1000).toFixed(0) + "k",
  });

  makeCountryLineChart("chart-market-remote", ct, "remote_percentage", {
    yFormat: v => v + "%",
  });
}

// ============================================================
// Section 6 — Role Intelligence
// ============================================================
function buildRoles() {
  const roles = DATA.roles;

  // Role category donut
  makeDonutChart("chart-role-cat",
    roles.role_category_counts.map(d => d.category),
    roles.role_category_counts.map(d => d.count)
  );

  // Industry distribution
  makeHBarChart("chart-industry",
    roles.industry_counts.map(d => d.industry),
    roles.industry_counts.map(d => d.count),
    "Count",
    PALETTE
  );

  // Top cities
  const cities = roles.top_cities.slice(0, 12);
  makeHBarChart("chart-cities",
    cities.map(d => d.city),
    cities.map(d => d.count),
    "Count",
    PALETTE
  );

  // Company type
  makeDonutChart("chart-company-type",
    roles.company_type_counts.map(d => d.company_type),
    roles.company_type_counts.map(d => d.count)
  );
}

// ============================================================
// Entry point
// ============================================================
async function init() {
  const loader = document.getElementById("loading-overlay");
  try {
    await loadAllData();
    buildKPIs();
    buildJobMarket();
    buildSalary();
    buildSkills();
    buildRemote();
    buildCountryTrends();
    buildRoles();
    initNav();
    if (loader) loader.style.display = "none";
  } catch (err) {
    console.error("Dashboard init error:", err);
    if (loader) {
      loader.innerHTML = `<div style="color:#f87171;text-align:center;padding:40px">
        <strong>Error loading dashboard data</strong><br>
        ${err.message}<br><br>
        <small>Make sure to open index.html via a local server (not file://)<br>
        Run: <code>python -m http.server 8080</code> from the web_dashboard/ folder</small>
      </div>`;
    }
  }
}

document.addEventListener("DOMContentLoaded", init);
