# WallStreetBets Analyzer Bot 📈

> Real-time sentiment analysis tool for r/wallstreetbets trading signals

## 🚀 Features

* Sentiment analysis of WSB comments
* Stock mention tracking
* Upvote-weighted scoring
* NLTK-based sentiment analysis
* Real-time data processing

## 📊 Demo Output
<img width="1627" height="718" alt="image" src="https://github.com/user-attachments/assets/6d7ec1fa-7f8d-47e5-964d-875465609626" />

### Sentiment Analysis
```bash
What Are Your Moves Tomorrow, September 03, 2025
buy_upvote = 175
sell_upvote = 97
hold_upvote = 20
```

### Top Stocks Analysis
```
Symbol  Compound
I       69.2061
GOOG     5.4756
GOOGL    6.7513
AI      -4.9287
SPY      3.9569
NVDA     1.0244
```

## 🛠️ Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/r-wallstreetbetsbot.git
cd r-wallstreetbetsbot
```

2. Create virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
   VISIT : [CREATE DEV APP](https://www.reddit.com/prefs/apps)
```bash
# Create .env file with:
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_USER_AGENT=your_agent
```

## 📖 Usage

```bash
# Sentiment Analysis
python senti.py

# Top Stocks Analysis 
python topstcks.py
```

## 💡 NLTK Sentiment Scoring

| Score Range | Interpretation |
|------------|----------------|
| > 0        | Positive      |
| = 0        | Neutral       |
| < 0        | Negative      |

## 📁 Project Structure

```
r-wallstreetbetsbot/
├── senti.py           # Sentiment analyzer
├── topstcks.py       # Stock tracker
├── nasdaqtraded.txt  # Stock database
├── requirements.txt   # Dependencies
├── .env              # Configuration
└── README.md         # Documentation
```

## 📦 Dependencies

* PRAW
* python-dotenv
* NLTK
* pandas

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

## ⚠️ Disclaimer

This tool is for educational purposes only. Make investment decisions at your own risk.
---
