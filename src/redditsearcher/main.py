import datetime  # get day today
import yfinance as yf


def tickerize(submission):
    '''Uses the reticker library to extract tickers from title and self text.'''
    extractor = reticker.TickerExtractor()
    tickers = extractor.extract(submission.title)
    if submission.is_self is True:
        tickers = tickers + extractor.extract(submission.selftext)
    return tickers


def main(subreddit, num_of_days: int):
    unix_starttime = calendar.timegm(datetime.utcnow().utctimetuple())
    unix_stoptime = unix_starttime - (num_of_days*86400)

    # Scrapes subreddit until reaches end date.
    # For each post, adds tickers to list and for each ticker adds score and mentions
    for submission in reddit.subreddit(subreddit).new(limit=None):
        if submission.created_utc < unixtime_stoptime:
            break  # exits for loop once done all posts in the time range

        day_number = unix_starttime - datetime.date(submission.created_utc)  # returns utc difference in seconds
        day_number = round(day_number/86400, 0)

        day[day_number].date = datetime.date.today() - datetime.timedelta(days=day_number)
        
        post_tickers = tickerize(submission)
        day[day_number].tickerlist.add(post_tickers)
        for ticker in post_tickers:
            day[day_number].mentions.add(ticker)
            day[day_number].scores.add(ticker, submission.score)

    # 
    for day_number in range(0, num_of_days):
        daterange = datetime.date.today() - datetime.timedelta(days=day_number)
        datatable = yf.download(
                                # ticker list
                                tickers=day[day_number].tickerlist, 
                                # get history just for that day
                                start=daterange, 
                                end=daterange, 
                                # group by ticker (to access via data['SPY'])
                                group_by="ticker"),
                                # adjust all OHLC automatically
                                auto_adjust = True
                                )
# for day_number in len(daterange):
#   daterange = today - day_number
#   datatable = yfinance.download(day[day_number].tickerlist, daterange)
#   day[day_number].stockdata.add(column)
#   write_json_day(day_number)


# write_json_day(day)
#   json_date = day[day_number].date
#   for ticker in day[day_number].tickerlist:
#       "ticker":{
#           mentions: day[day_number].mentions(ticker),
#           score: day[day_number].scores(ticker),
#           stockdata: {
#              open: day[day_number].stockdata.open,
#              close: day[day_number].stockdata.close,
#              high: day[day_number].stockdata.high,
#              low: day[day_number].stockdata.low,
#              volume: day[day_number].stockdata.volume
#        }
#   },


# class day
# 
# self.tickerlist = tickerlist
# 


# json to csv