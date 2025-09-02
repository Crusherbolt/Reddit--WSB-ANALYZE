import os
import praw
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Access the WallStreetBets subreddit
subreddit = reddit.subreddit('wallstreetbets')

title = subreddit.hot(limit =1)

for submission in title:
    print(submission.title)
    comments = submission.comments.list()
    for comment in comments[:2]:
        print(comment.body)
        print(comment.ups)

buy_upvote=0
sell_upvote=0
hold_upvote=0

hot_news = subreddit.hot(limit =1)
for submission in hot_news:
    print(submission.title)
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()
    for comment in comments:
        buy_list = re.findall(r'\bbuy\b',comment.body,flags=re.IGNORECASE)
        sell_list = re.findall(r'\bsell\b', comment.body, flags=re.IGNORECASE)
        hold_list = re.findall(r'\bhold\b', comment.body, flags=re.IGNORECASE)
        dont_buy_list = re.findall(r"\bdon't buy\b",comment.body, flags=re.IGNORECASE)
        dont_sell_list = re.findall(r"\bdon't sell\b",comment.body, flags=re.IGNORECASE)
        dont_hold_list = re.findall(r"\bdon't hold\b",comment.body, flags=re.IGNORECASE)
        # Decision logic based on sentiment lists
        if buy_list == []:
            pass  # No change to buy_upvote
        elif dont_buy_list == []:
            buy_upvote += comment.ups

        if sell_list == []:
            pass  # No change to sell_upvote
        elif dont_sell_list == []:
            sell_upvote += comment.ups

        if hold_list == []:
            pass  # No change to hold_upvote
        elif dont_hold_list == []:
            hold_upvote += comment.ups
            sell_upvote += comment.ups
print('buy_upvote =',buy_upvote)
print("sell_upvote =",sell_upvote)
print("hold_upvote =",hold_upvote)