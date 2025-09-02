import os
import pandas as pd
import praw
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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


with open('nasdaqtraded.txt') as f:
    lines =f.readlines()

companies =lines[1:]
# print(companies[1][2:])
# print(companies[1][2:companies[1].find('|',2)])

all_ticker = {}
top_tickers= {}

for line in companies:
    ticker = line[2:line.find('|',2)]
    all_ticker[ticker] = 1

regexPattern = r'\b([A-Z]+)\b'

sentimental_score= {}
final_1 ={}

nltk.download('vader_lexicon')

vader = SentimentIntensityAnalyzer()

for submission in subreddit.top('day'):
    # print(submission.title)
    strings = [submission.title]
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        strings.append(comment.body)
        # break
    for s in strings:
        for phrase in re.findall(regexPattern,s):
            if phrase in all_ticker:
                # Polarity (compound tells if a stings is + or -ve)
                score1 = vader.polarity_scores(s)
                #print(score1)
                if phrase not in sentimental_score:
                    sentimental_score[phrase] =score1
                else:
                    for key,_ in score1.items():
                        sentimental_score[phrase][key] += score1[key]
                if phrase not in top_tickers:
                    top_tickers[phrase] = 1
                else:
                    top_tickers[phrase] +=1
            ticker1 = list(sentimental_score)
            for ticker1 in ticker1:
                final_1[ticker1] = sentimental_score[ticker1]['compound']
    # break #to stop from system crash if too many comments.

# print(top_tickers)
series = pd.Series(top_tickers).sort_values(ascending =False)
top_picks = series[:10]
top_stocks = list(top_picks.index)
final_df =pd.DataFrame(pd.Series(final_1)).loc[top_stocks]
print(final_df)