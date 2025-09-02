import re
from typing import Dict, List, Tuple
import pandas as pd
import streamlit as st

from .utils import load_json

B = re.compile(r"\bbuy\b", re.I)
S = re.compile(r"\bsell\b", re.I)
H = re.compile(r"\bhold\b", re.I)
DB = re.compile(r"\bdon't buy\b", re.I)
DS = re.compile(r"\bdon't sell\b", re.I)
DH = re.compile(r"\bdon't hold\b", re.I)

def tally_votes(comments: List[dict]) -> Dict[str, int]:
    buy = sell = hold = 0
    for c in comments:
        text = c.get("body", "")
        ups = int(c.get("ups", 0))
        if B.search(text) and not DB.search(text):
            buy += ups
        if S.search(text) and not DS.search(text):
            sell += ups
        if H.search(text) and not DH.search(text):
            hold += ups
    return {"BUY": buy, "SELL": sell, "HOLD": hold}

def run_live(reddit, subreddit: str, hot_limit: int = 1) -> Tuple[str, Dict[str, int]]:
    title = ""
    votes = {"BUY": 0, "SELL": 0, "HOLD": 0}
    for submission in reddit.subreddit(subreddit).hot(limit=hot_limit):
        title = submission.title or ""
        submission.comments.replace_more(limit=0)
        comments = [
            {"body": getattr(c, 'body', ''), "ups": int(getattr(c, 'ups', 0))}
            for c in submission.comments.list()
        ]
        votes = tally_votes(comments)
        break
    return title, votes

def run_demo(sample_path: str) -> Tuple[str, Dict[str, int]]:
    comments = load_json(sample_path)
    title = "WSB Hot Thread (Demo)"
    return title, tally_votes(comments)
