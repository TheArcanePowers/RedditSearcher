#Preamble
import os
import sys
os.chdir(os.path.dirname(sys.argv[0])) #Change the scripts working directory to the script's own directory
import praw
reddit = praw.Reddit("main-bot", user_agent="windows:github:alpha-2 (by u/thearcanepowers)")
reddit.read_only = True
#ticker extraction
import reticker
#ticker validation
import urllib.request as request
from contextlib import closing
import re
global tickerTuple
tickerTuple = ()
#reportWriter
import csv
import calendar
from datetime import datetime
###

def tickerize(submissionattribute):
    extractor = reticker.TickerExtractor()
    return extractor.extract(submissionattribute)

def tickerCleanup(tickerDict, subreddit):
    blacklisted = []
    try:
        with open(f"redditsearcher/blacklists/{subreddit}", mode="r") as file:
            for line in file:
                blacklisted.append(line.split("|")[0])
    except IOError:
        pass
    
    with open("redditsearcher/blacklists/common", mode="r") as file:
        for line in file:
            blacklisted.append(line.split("|")[0])

    tickerDictClean = dict(tickerDict)
    for i in tickerDict:   
        if i not in tickerTuple or i in blacklisted:
            del tickerDictClean[i]
    
    del tickerDict
    tickerDict = tickerDictClean
    del tickerDictClean
    
    tickerDict = dict(sorted(tickerDict.items(), key=lambda item: item[1], reverse=True))
    return tickerDict

def loadTickerValidation():
    print("Downloading ticker validation...")
    global tickerTuple
    with closing(request.urlopen("ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt")) as r:
        for line in r:
            line = line.decode()
            newline = (re.search('[^|]*', line).group(),)
            tickerTuple += (newline)
    with closing(request.urlopen("ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt")) as r:
        for line in r:
            line = line.decode()
            newline = (re.search('[^|]*', line).group(),)
            tickerTuple += (newline)

def analyzeSub(subreddit):
    print("Analyzing " + subreddit)
    tickersMentionDict = {}
    tickersScoreDict = {}

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple()) - 86400

    for submission in reddit.subreddit(subreddit).new(limit=200):
        if submission.created_utc > unixtime:
            tickers = tickerize(submission.title)

            if submission.is_self == True:
                tickers = tickers + tickerize(submission.selftext)

            upvotes = submission.score
            for i in tickers:
                if i in tickersMentionDict:
                    oldNum = tickersMentionDict.get(i)
                    tickersMentionDict[i] = int(oldNum + 1)
                else:
                    tickersMentionDict[i] = int(1)
                if i in tickersScoreDict:
                    oldNum = tickersScoreDict.get(i)
                    tickersScoreDict[i] = int(oldNum + upvotes)
                else:
                    tickersScoreDict[i] = int(upvotes)
        else:
            continue
    return dict(tickerCleanup(tickersMentionDict, subreddit)), dict(tickerCleanup(tickersScoreDict, subreddit))

def stockPrices(ticker):
    import yfinance as yf
    data = yf.Ticker(ticker).history(period="1d")
    return round(data['Open'].array[0],2), round(data['Close'].array[0],2), round(data['High'].array[0],2), round(data['Low'].array[0],2), round(data['Volume'].array[0],2), 

def analyzeSubreddit(subreddit):
    if len(tickerTuple) == 0:
        loadTickerValidation()
    
    date = datetime.now().strftime("%d/%m/%y")
    mentions, scores = analyzeSub(subreddit)

    if os.path.exists(f"outputs/{subreddit}.csv"):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    print("getting stock prices")
    with open(f"outputs/{subreddit}.csv", mode=append_write, newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        if append_write == "w":
            writer.writerow(["date","ticker","scores","mentions","openprice_adj","closeprice_adj","dailyHigh","dailyLow","volume"])

        for stock in scores:
            openPrice, closePrice, dailyHigh, dailyLow, volumeTraded = stockPrices(stock)
            writer.writerow([date,stock,scores.get(stock),mentions.get(stock),openPrice,closePrice,dailyHigh,dailyLow,volumeTraded])
    
    print(subreddit + '.csv completed.')