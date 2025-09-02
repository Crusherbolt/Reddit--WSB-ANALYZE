import re
from typing import Dict, List, Tuple
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st

from .tickers import load_ticker_set
from .utils import load_json

REGEX_TICKER = r"\b([A-Z]{1,5})\b"

@st.cache_resource(show_spinner=False)
def get_vader() -> SentimentIntensityAnalyzer:
    nltk.download('vader_lexicon', quiet=True)
    return SentimentIntensityAnalyzer()

def aggregate_sentiment(texts: List[str], ticker_set: set[str]) -> Tuple[pd.DataFrame, Dict[str, int]]:
    vader = get_vader()
    sentimental_score: Dict[str, Dict[str, float]] = {}
    counts: Dict[str, int] = {}

    for s in texts:
        for phrase in re.findall(REGEX_TICKER, s):
            if phrase in ticker_set:
                score = vader.polarity_scores(s)
                if phrase not in sentimental_score:
                    sentimental_score[phrase] = score.copy()
                else:
                    for k, v in score.items():
                        sentimental_score[phrase][k] += v
                counts[phrase] = counts.get(phrase, 0) + 1

    final = {t: sentimental_score[t]["compound"] for t in sentimental_score}
    df = pd.DataFrame.from_dict(final, orient="index", columns=["compound"]).sort_values("compound", ascending=False)
    return df, counts

def run_pipeline_live(reddit, subreddit: str, time_filter: str, top_limit: int, ticker_file: str) -> Tuple[pd.DataFrame, Dict[str, int]]:
    ticker_set = load_ticker_set(ticker_file)
    posts = reddit.subreddit(subreddit).top(time_filter, limit=top_limit)
    texts: List[str] = []
    for submission in posts:
        texts.append(submission.title or "")
        submission.comments.replace_more(limit=0)
        for c in submission.comments.list():
            texts.append(getattr(c, 'body', ""))
    return aggregate_sentiment(texts, ticker_set)

def run_pipeline_demo(ticker_file: str, sample_path: str) -> Tuple[pd.DataFrame, Dict[str, int]]:
    ticker_set = load_ticker_set(ticker_file)
    samples = load_json(sample_path)
    texts: List[str] = []
    for item in samples:
        texts.append(item.get("title", ""))
        texts.extend(item.get("comments", []))
    return aggregate_sentiment(texts, ticker_set)
