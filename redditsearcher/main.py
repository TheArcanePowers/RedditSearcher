#Preamble
import praw
reddit = praw.Reddit("main-bot", user_agent="windows:github:alpha-1 (by u/thearcanepowers)")
reddit.read_only = True
#ticker extraction
import reticker
#ticker validation
import urllib.request as request
from contextlib import closing
import re
tickerTuple = ()
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
#reportWriter
import csv
###

#definitions
def tickerizeTitle(submission):
    extractor = reticker.TickerExtractor()
    return extractor.extract(submission.title)

def tickerCleanup(tickerDict):
    tickerDictClean = dict(tickerDict)
    for i in tickerDict:   
        if i not in tickerTuple:
            del tickerDictClean[i]

    del tickerDict
    tickerDict = tickerDictClean
    del tickerDictClean

    tickerDict = dict(sorted(tickerDict.items(), key=lambda item: item[1], reverse=True))
    return tickerDict

def analyzeMentions(subreddit):
#most mentioned tickers in past week
    print("Analyzing " + subreddit + " for mentions...")
    tickersMentionDict = {}
    for submission in reddit.subreddit(subreddit).new(limit=1000):
        tickers = tickerizeTitle(submission)
        for i in tickers:
                if i in tickersMentionDict:
                    oldNum = tickersMentionDict.get(i)
                    tickersMentionDict[i] = int(oldNum + 1)
                else:
                    tickersMentionDict[i] = int(1)

    return dict(tickerCleanup(tickersMentionDict))

def analyzeScores(subreddit):
#most upvoted tickers
    print("Analyzing " + subreddit + " for scores...")
    tickersScoreDict = {}
    for submission in reddit.subreddit(subreddit).new(limit=1000):
        tickers = tickerizeTitle(submission)
        upvotes = submission.score
        for i in tickers:
                if i in tickersScoreDict:
                    oldNum = tickersScoreDict.get(i)
                    tickersScoreDict[i] = int(oldNum + upvotes)
                else:
                    tickersScoreDict[i] = int(upvotes)
    return dict(tickerCleanup(tickersScoreDict))