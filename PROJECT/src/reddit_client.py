import os
from typing import Optional
import praw
from dotenv import load_dotenv
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_reddit_client() -> Optional[praw.Reddit]:
    load_dotenv()
    required = [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME",
        "REDDIT_PASSWORD",
        "REDDIT_USER_AGENT",
    ]
    if not all(os.getenv(k) for k in required):
        return None
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
