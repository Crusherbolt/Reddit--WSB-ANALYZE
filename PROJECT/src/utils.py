import json
from pathlib import Path
import streamlit as st

@st.cache_data(show_spinner=False)
def load_json(path: str):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text())

@st.cache_data(show_spinner=False)
def read_text(path: str) -> str:
    p = Path(path)
    return p.read_text() if p.exists() else ""

def format_big_number(n: int) -> str:
    for unit in ["", "K", "M", "B"]:
        if abs(n) < 1000:
            return f"{n}{unit}"
        n = n / 1000
    return f"{n:.1f}T"
