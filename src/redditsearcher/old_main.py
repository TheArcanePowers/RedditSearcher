#!/usr/bin/env python3
# Preamble
import os
import sys
import urllib.request as request  # ticker validation section
from contextlib import closing
import re
import csv  # report writer section
import calendar
from datetime import datetime
import reticker  # ticker extraction
import yfinance as yf

valid_tickers = ()  # for ticker validation
os.chdir(os.path.dirname(sys.argv[0]))  # Change working dir to script's dir
# ATTEMPTING TO load praw
try:
    import praw
    import prawcore
    reddit = praw.Reddit("main-bot", user_agent="windows:github:Search-Beta (by u/thearcanepowers)")
except ImportError:
    sys.exit("FATAL ERROR: PRAW not installed. Have you ran setup.py?")
# except OAuthException:
#     print("No valid ([main-bot]) praw.ini file found, or supplied PRAW \
#         credentials do not match. Attempting backup manual authentification:")
#     try:
#         import praw
#         given_client_id = input("Client ID: "),
#         given_client_secret = input("Client Secret: "),

#         reddit = praw.Reddit(
#             client_id=given_client_id,
#             client_secret=given_client_secret,
#             user_agent="windows:github:Search-Beta (by u/thearcanepowers)")
#         reddit.read_only = True
#     except OAuthException:
#         sys.exit("FATAL ERROR: PRAW credentials do not match. Double-check your \
#             credentials, and ensure that that the username and password used \
#             are for the same user with which the application is associated")
#     except:
#         sys.exit("FATAL ERROR: PRAW error x2")
# Preamble Finished


def tickerize(submissionattribute):
    '''Simply uses the reticker library. Resonably could be removed.'''
    extractor = reticker.TickerExtractor()
    return extractor.extract(submissionattribute)


def ticker_cleanup(ticker_dict, subreddit):
    '''
    Takes in dirty ticker_dict, runs it through both its dedicated \
    blacklist and a common one, and then uses the downloaded valid ticker \
    list to remove all false positives.

        :param ticker_dict: input ticker dictionary to clean
        :param subreddit: subreddit to use for blacklist file

        :return outputs a validated ticker dictionary removing all false positives
    '''
    # Load blacklist
    blacklisted = []
    try:
        with open(f"blacklists/{subreddit}", mode="r") as file:
            for line in file:
                blacklisted.append(line.split("|")[0])
    except IOError:
        pass
    with open("blacklists/common", mode="r") as file:
        for line in file:
            blacklisted.append(line.split("|")[0])

    ticker_clean_dict = dict(ticker_dict)
    for i in ticker_dict:
        if i not in valid_tickers or i in blacklisted:
            del ticker_clean_dict[i]
    # Delete old dict and replace with new
    del ticker_dict
    ticker_dict = ticker_clean_dict
    del ticker_clean_dict
    # Sort dict (not really needed anymore though)
    # ticker_dict = dict(sorted(ticker_dict.items(),
    #                   key=lambda item: item[1], reverse=True))
    return ticker_dict


def load_ticker_validation():
    '''Downloads NASDAQ hosted tickers and forms tuple'''
    # Incredibly fustratingly, I've encountered a lot of issues with this delayed loading system.
    # Most likely, it's just because I decided to use my own half-baked solution, so I'm going to
    # research best practises for this. I've attempted having it return the tuple rather than change
    # the global variable, but then I get all caught up in order of execution!
    global valid_tickers
    print("Downloading ticker validation...")
    with closing(request.urlopen("ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt")) as r:
        for line in r:
            line = line.decode()
            newline = (re.search('[^|]*', line).group(),)
            valid_tickers += (newline)
    with closing(request.urlopen("ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt")) as r:
        for line in r:
            line = line.decode()
            newline = (re.search('[^|]*', line).group(),)
            valid_tickers += (newline)


def analyze_scores_mentions(subreddit):
    '''Uses PRAW to return two dictionaries with scores and mentions of each \
        ticker within precisely the past 24 hours'''
    # On reflection, returning two dictionaries is pretty stupid.
    # Something much better would be to return a nested JSON, with each ticker
    # placed underneath the date, and below each ticker mentioned then put the
    # number of mentions and scores. Just not sure if JSON would make it harder
    # to analyse!
    print("Analyzing " + subreddit)
    tickers_mentioned_dict = {}
    tickers_score_dict = {}

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple()) - 86400
    for submission in reddit.subreddit(subreddit).new(limit=200):
        if submission.created_utc > unixtime:
            tickers = tickerize(submission.title)
            if submission.is_self is True:
                tickers = tickers + tickerize(submission.selftext)
            upvotes = submission.score
            for i in tickers:
                if i in tickers_mentioned_dict:
                    old_number = tickers_mentioned_dict.get(i)
                    tickers_mentioned_dict[i] = int(old_number + 1)
                else:
                    tickers_mentioned_dict[i] = int(1)
                if i in tickers_score_dict:
                    old_number = tickers_score_dict.get(i)
                    tickers_score_dict[i] = int(old_number + upvotes)
                else:
                    tickers_score_dict[i] = int(upvotes)
        else:
            continue
    return dict(ticker_cleanup(tickers_mentioned_dict, subreddit)), \
        dict(ticker_cleanup(tickers_score_dict, subreddit))


def get_stockprices(ticker):
    '''Returns stock OHLC prices in the day's trading, as well as total volume.'''
    # If I were trying to minimize API calls, I'd do this very differently.
    # That being said, it would be a bigger headache, and yahooFinance has
    # an amazingly low latency that allows me to use sloppy coding here.
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return round(data['Open'].array[0], 2), round(data['Close'].array[0], 2), \
            round(data['High'].array[0], 2), round(data['Low'].array[0], 2), \
            round(data['Volume'].array[0], 2)
    except (ValueError, KeyError) as e:
        print(f"{ticker} failed with error {e}!")
        return "error", " error", "error", "error", "error"  # error out


def validate_reddit_name(sub):
    """Validates subreddits"""
    sr = reddit.subreddit(sub.strip())  # load subreddit
    try:
        if sr.description:  # Dummy test just to raise exception
            pass
        return True
    except prawcore.exceptions.Redirect:
        return False


def analyze_subreddit(subreddit):
    '''
    The main function. Loads tickers if not already, and calls all other \
        functions to output a csv file. Currently the locations are fixed, \
        but in the future I'll try to make the locations changable.
    Function checks for pre-existing csv output, and appends if already existing.
    '''
    # Preamble
    if len(valid_tickers) == 0:
        load_ticker_validation()
    if not validate_reddit_name(subreddit):  # stops function if subreddit invalid
        print(f"{subreddit} isn't valid! Skipping.")
        return
    if os.path.exists(f"outputs/{subreddit}.csv"):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    # End preamble
    date = datetime.now().strftime("%d/%m/%y")
    mentions, scores = analyze_scores_mentions(subreddit)
    with open(f"outputs/{subreddit}.csv", mode=append_write, newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        if append_write == "w":
            writer.writerow(["date", "ticker", "scores", "mentions",
                             "openprice_adj", "closeprice_adj", "daily_high",
                             "daily_low", "volume"])
        for stock in scores:
            open_price, close_price, daily_high, daily_low, volume_traded = get_stockprices(stock)
            writer.writerow([date, stock, scores.get(stock),
                             mentions.get(stock), open_price, close_price,
                             daily_high, daily_low, volume_traded])

    print(subreddit + '.csv completed.')
