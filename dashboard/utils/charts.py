"""
charts.py — Shared Plotly chart builders for the AI MarketLens Streamlit app.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

HIST_COLOR  = "#3b82d4"
PROJ_COLOR  = "#f59e0b"
PALETTE     = px.colors.qualitative.Set2
PERIOD_MAP  = {"Historical": HIST_COLOR, "Projected": PROJ_COLOR}


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str,
              color_col: str = None, orientation: str = "v",
              height: int = 350) -> go.Figure:
    """Horizontal or vertical bar chart with consistent styling."""
    fig = px.bar(
        df, x=x, y=y, title=title, color=color_col,
        color_discrete_sequence=PALETTE,
        orientation=orientation,
        height=height,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
        showlegend=color_col is not None,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="#e5e7eb"),
    )
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str, color: str,
               title: str, height: int = 380,
               period_dashes: bool = False) -> go.Figure:
    """Multi-series line chart. Optional dashed lines for Projected."""
    if period_dashes and "period_type" in df.columns:
        fig = go.Figure()
        for grp, sub in df.groupby(color):
            for period, psub in sub.groupby("period_type"):
                dash = "dot" if period == "Projected" else "solid"
                show_legend = period == "Historical"
                fig.add_trace(go.Scatter(
                    x=psub[x], y=psub[y],
                    mode="lines+markers",
                    name=f"{grp}",
                    line=dict(dash=dash, width=2),
                    showlegend=show_legend,
                    legendgroup=grp,
                    marker=dict(size=6),
                ))
        fig.update_layout(title=title, height=height)
    else:
        fig = px.line(df, x=x, y=y, color=color, title=title,
                      markers=True, height=height,
                      color_discrete_sequence=PALETTE)

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#e5e7eb"),
    )
    return fig


def pie_chart(df: pd.DataFrame, names: str, values: str,
              title: str, height: int = 350) -> go.Figure:
    """Donut chart."""
    fig = px.pie(df, names=names, values=values, title=title,
                 hole=0.45, height=height,
                 color_discrete_sequence=PALETTE)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
        legend=dict(orientation="h", y=-0.15),
    )
    return fig


def histogram_chart(series: pd.Series, title: str,
                    height: int = 350, color: str = HIST_COLOR) -> go.Figure:
    """Salary distribution histogram."""
    fig = px.histogram(series, title=title, nbins=50, height=height)
    fig.update_traces(marker_color=color, marker_line_color="white",
                      marker_line_width=0.5)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
        xaxis=dict(title="Salary (USD)", showgrid=False),
        yaxis=dict(title="Count", gridcolor="#e5e7eb"),
        showlegend=False,
    )
    return fig


def heatmap_chart(df: pd.DataFrame, x: str, y: str, z: str,
                  title: str, height: int = 380) -> go.Figure:
    """Pivot heatmap (e.g. country × year)."""
    pivot = df.pivot_table(index=y, columns=x, values=z, aggfunc="sum")
    fig = px.imshow(pivot, title=title, height=height,
                    color_continuous_scale="Blues",
                    text_auto=True)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
    )
    return fig


def scatter_chart(df: pd.DataFrame, x: str, y: str, color: str,
                  title: str, height: int = 400) -> go.Figure:
    """Scatter plot."""
    fig = px.scatter(df, x=x, y=y, color=color, title=title,
                     height=height, opacity=0.5, size_max=6,
                     color_discrete_sequence=PALETTE)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_family="Segoe UI",
        margin=dict(t=40, b=20, l=10, r=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#e5e7eb"),
    )
    return fig
