/**
 * charts.js — Chart.js chart builders for AI MarketLens Web Dashboard
 * All data is loaded from web_dashboard/data/*.json
 */

"use strict";

// ============================================================
// Colour palette
// ============================================================
const PALETTE = [
  "#3b82f6","#f59e0b","#10b981","#ef4444",
  "#8b5cf6","#06b6d4","#f97316","#84cc16",
  "#ec4899","#6366f1","#14b8a6",
];
const HIST_COLOR = "#3b82f6";
const PROJ_COLOR = "#f59e0b";
const GRID_COLOR = "rgba(148,163,184,0.1)";
const TEXT_COLOR = "#94a3b8";

// ============================================================
// Default Chart.js global options
// ============================================================
const DEFAULTS = {
  plugins: {
    legend: {
      labels: { color: TEXT_COLOR, font: { family: "Segoe UI, sans-serif", size: 12 } }
    },
    tooltip: {
      backgroundColor: "#1e293b",
      titleColor: "#f1f5f9",
      bodyColor: "#94a3b8",
      borderColor: "#334155",
      borderWidth: 1,
    }
  },
  scales: {
    x: {
      grid: { color: GRID_COLOR },
      ticks: { color: TEXT_COLOR },
    },
    y: {
      grid: { color: GRID_COLOR },
      ticks: { color: TEXT_COLOR },
    },
  },
};

function mergeDefaults(opts) {
  // Deep merge helper (shallow for now, sufficient here)
  const base = JSON.parse(JSON.stringify(DEFAULTS));
  if (!opts) return base;
  if (opts.plugins) Object.assign(base.plugins, opts.plugins);
  if (opts.scales) Object.assign(base.scales, opts.scales);
  if (opts.indexAxis) base.indexAxis = opts.indexAxis;
  if (opts.responsive !== undefined) base.responsive = opts.responsive;
  base.maintainAspectRatio = false;
  return base;
}

// ============================================================
// KPI Cards
// ============================================================
function populateKPIs(kpis) {
  const set = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  };
  const usd = v => "$" + Number(v).toLocaleString("en-US", { maximumFractionDigits: 0 });
  const pct = v => v + "%";
  const num = v => Number(v).toLocaleString("en-US");

  set("kpi-total-jobs",    num(kpis.total_job_postings));
  set("kpi-avg-salary",    usd(kpis.avg_salary_usd));
  set("kpi-median-salary", usd(kpis.median_salary_usd));
  set("kpi-remote-pct",    pct(kpis.remote_job_pct));
  set("kpi-countries",     kpis.countries_covered);
  set("kpi-roles",         kpis.job_roles);
  set("kpi-skills",        kpis.skills_tracked);
  set("kpi-hist-jobs",     num(kpis.historical_jobs));
  set("kpi-proj-jobs",     num(kpis.projected_jobs));
  set("kpi-entry-sal",     usd(kpis.entry_avg_salary));
  set("kpi-senior-sal",    usd(kpis.senior_avg_salary));
  set("kpi-premium",       kpis.senior_premium_ratio + "x");
}

// ============================================================
// Bar chart (vertical)
// ============================================================
function makeBarChart(canvasId, labels, data, label, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label,
        data,
        backgroundColor: opts.colors || PALETTE[0],
        borderWidth: 0,
        borderRadius: 4,
      }],
    },
    options: mergeDefaults(opts.chartOpts),
  });
}

// ============================================================
// Horizontal bar chart
// ============================================================
function makeHBarChart(canvasId, labels, data, label, colors, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label,
        data,
        backgroundColor: colors || PALETTE,
        borderWidth: 0,
        borderRadius: 3,
      }],
    },
    options: mergeDefaults({
      indexAxis: "y",
      ...opts.chartOpts,
      scales: {
        x: { grid: { color: GRID_COLOR }, ticks: { color: TEXT_COLOR } },
        y: { grid: { color: "transparent" }, ticks: { color: TEXT_COLOR } },
      },
    }),
  });
}

// ============================================================
// Doughnut chart
// ============================================================
function makeDonutChart(canvasId, labels, data, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: opts.colors || PALETTE,
        borderWidth: 2,
        borderColor: "#1e293b",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "55%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: TEXT_COLOR, font: { size: 11 }, padding: 12 }
        },
        tooltip: DEFAULTS.plugins.tooltip,
      },
    },
  });
}

// ============================================================
// Multi-line chart (with optional dashed lines for Projected)
// ============================================================
function makeLineChart(canvasId, datasets, xLabels, opts = {}) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "line",
    data: { labels: xLabels, datasets },
    options: mergeDefaults({
      plugins: {},
      scales: {
        x: { grid: { color: GRID_COLOR }, ticks: { color: TEXT_COLOR } },
        y: { grid: { color: GRID_COLOR }, ticks: { color: TEXT_COLOR } },
      },
      ...opts.chartOpts,
    }),
  });
}

// ============================================================
// Grouped bar chart (salary by dimension)
// ============================================================
function makeSalaryBar(canvasId, items, labelKey, opts = {}) {
  const labels = items.map(d => d[labelKey]);
  const avgs   = items.map(d => Math.round(d.avg));
  const medians = items.map(d => Math.round(d.median));

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Average",
          data: avgs,
          backgroundColor: PALETTE[0],
          borderWidth: 0,
          borderRadius: 4,
        },
        {
          label: "Median",
          data: medians,
          backgroundColor: PALETTE[2],
          borderWidth: 0,
          borderRadius: 4,
        },
      ],
    },
    options: mergeDefaults({
      scales: {
        x: { grid: { color: GRID_COLOR }, ticks: { color: TEXT_COLOR } },
        y: {
          grid: { color: GRID_COLOR },
          ticks: {
            color: TEXT_COLOR,
            callback: v => "$" + (v / 1000).toFixed(0) + "k",
          },
        },
      },
    }),
  });
}

// ============================================================
// Country line chart (from country trends data)
// ============================================================
function makeCountryLineChart(canvasId, trendData, yKey, opts = {}) {
  const countries = [...new Set(trendData.map(d => d.country))];
  const allYears  = [...new Set(trendData.map(d => d.year))].sort();

  const datasets = countries.map((country, i) => {
    const countryData = trendData.filter(d => d.country === country);
    const points = allYears.map(yr => {
      const row = countryData.find(d => d.year === yr);
      return row ? row[yKey] : null;
    });
    // Build segments: dashed for projected years
    return {
      label: country,
      data: points,
      borderColor: PALETTE[i % PALETTE.length],
      backgroundColor: "transparent",
      pointRadius: 4,
      borderWidth: 2,
      tension: 0.2,
      segment: {
        borderDash: ctx2 => {
          const idx = ctx2.p1DataIndex;
          const yr  = allYears[idx];
          return yr >= 2025 ? [5, 3] : [];
        },
      },
    };
  });

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "line",
    data: { labels: allYears, datasets },
    options: mergeDefaults({
      scales: {
        x: { grid: { color: GRID_COLOR }, ticks: { color: TEXT_COLOR } },
        y: {
          grid: { color: GRID_COLOR },
          ticks: {
            color: TEXT_COLOR,
            callback: opts.yFormat || (v => v),
          },
        },
      },
    }),
  });
}
