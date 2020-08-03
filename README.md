#EasyStocks
A simple telegram bot for stocks written in Python

Main Features
1. Retrieval of stock data (Price, Price Changes, 5 most recent news) upon input of stock ticker
2. User can favourite stock ticke(s) that they frequently monitor to a shortlist that can be displayed with one-click

Commands
```
/start - starts the bot
/help - displays help
/shortlist - shortlists ticker(s) for one-click display
/selected - displays shortlisted stocks
```

Libraries used
1. Selenium for scraping of stock information from Yahoo Finance
2. Pyrebase for storing Users' favourites
3. Python-Telegram-Bot as a wrapper for Telegram Bot's API
