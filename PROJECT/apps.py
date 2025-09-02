import streamlit as st

from src.config import AppConfig
from src.reddit_client import get_reddit_client
from src.sentiment_wsbtickers import run_pipeline_live, run_pipeline_demo
from src.voting_bsh import run_live, run_demo
from src.ui_components import card, metric_row, bar_chart, donut_chart_from_dict

st.set_page_config(page_title="WSB Sentiment & Votes", page_icon="🧠", layout="wide")

with st.sidebar:
    st.image("assets/logo.svg", width=96)
    st.title("WSB Analyzer")
    st.write("Two micro‑projects in one page.")

    mode = st.toggle("Live Reddit mode", value=False, help="Turn on to use your Reddit API credentials.")
    st.divider()
    time_filter = st.selectbox("Top posts time window (Project 1)", ["day", "week", "month"], index=0)
    top_limit = st.slider("# of top posts to scan", 5, 50, 15, step=5)
    st.caption("More posts = more coverage (slower).")

    st.divider()
    st.caption("Data sources")
    nasdaq_file = st.text_input("Nasdaq symbols file", "data/nasdaqtraded.txt")

st.title("WSB Sentiment & Vote Analyzer")

st.markdown(
    """
**Use‑cases showcased**

- **Project 1 — Ticker Sentiment:** NLP (VADER) over WSB titles & comments, ticker extraction, ranking, and visual reporting. 
- **Project 2 — Buy/Sell/Hold Votes:** Regex‑based intent parsing weighted by upvotes to gauge crowd positioning.
    """
)

cfg = AppConfig.from_env()
reddit = get_reddit_client() if mode else None

col1, col2 = st.columns(2, gap="large")

# ------------------- Project 1 -------------------
with col1:
    with card("Project 1: Ticker Sentiment", "Top WSB posts & comments → VADER sentiment by ticker"):
        if mode and reddit:
            df, counts = run_pipeline_live(reddit, cfg.subreddit, time_filter, top_limit, nasdaq_file)
        else:
            df, counts = run_pipeline_demo(nasdaq_file, "data/sample_submissions.json")

        st.write("### Sentiment by Ticker (compound score)")
        st.dataframe(df.head(10))

        if not df.empty:
            bar_chart(df.head(10), x="index", y="compound", title="Top 10 Tickers Sentiment")

# ------------------- Project 2 -------------------
with col2:
    with card("Project 2: Buy/Sell/Hold Votes", "Hot WSB thread → Upvote‑weighted action words"):
        if mode and reddit:
            title, votes = run_live(reddit, cfg.subreddit, cfg.hot_limit)
        else:
            title, votes = run_demo("data/sample_comments.json")

        st.write(f"### Hot Thread: {title}")
        metric_row([(k, v) for k, v in votes.items()])
        donut_chart_from_dict(votes, title="Vote Share")
