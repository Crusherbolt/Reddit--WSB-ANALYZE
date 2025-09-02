from pathlib import Path
import streamlit as st

@st.cache_data(show_spinner=False)
def load_ticker_set(nasdaq_file: str) -> set[str]:
    p = Path(nasdaq_file)
    if not p.exists():
        return {"AAPL", "TSLA", "NVDA", "GME", "AMC", "MSFT"}

    tickers: set[str] = set()
    for i, line in enumerate(p.read_text().splitlines()):
        if i == 0:
            continue
        try:
            symbol = line[2:line.find('|', 2)]
            if symbol.isupper():
                tickers.add(symbol)
        except Exception:
            continue
    return tickers
