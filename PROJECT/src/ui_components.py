import streamlit as st
import altair as alt
import pandas as pd
from .utils import format_big_number

def card(title: str, subtitle: str | None = None):
    with st.container(border=True):
        st.subheader(title)
        if subtitle:
            st.caption(subtitle)
        return st.container()

def metric_row(items: list[tuple[str, int | float | str]]):
    cols = st.columns(len(items))
    for i, (label, value) in enumerate(items):
        with cols[i]:
            st.metric(label, value)

def bar_chart(df: pd.DataFrame, x: str, y: str, title: str):
    chart = (
        alt.Chart(df.reset_index(names=x))
        .mark_bar()
        .encode(x=alt.X(x, sort='-y'), y=y, tooltip=[x, y])
        .properties(height=320, title=title)
    )
    st.altair_chart(chart, use_container_width=True)

def donut_chart_from_dict(d: dict[str, int], title: str):
    total = sum(d.values()) or 1
    data = pd.DataFrame({"label": list(d.keys()), "value": list(d.values())})
    data["pct"] = data["value"] / total
    chart = (
        alt.Chart(data)
        .mark_arc(innerRadius=80)
        .encode(theta="value", color="label", tooltip=["label", "value", alt.Tooltip("pct", format=",.0%")])
        .properties(height=320, title=title)
    )
    st.altair_chart(chart, use_container_width=True)
