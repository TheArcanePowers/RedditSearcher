Initially, the program created seperate reports of most mentioned and highest scoring posts in the newest week on various subreddits.

Unfortunately this ended up outputting a multitude of files per subreddit:
And realistically, this barely addressed the actual aim of the program.

Thus entered **Verson 2**, which created a csv separated database per subreddit listing all the stocks mentioned and upvoted daily, and with their stock opening and closing prices. Additionally, running it appends the daily report to pre-existing csv files per subreddit.

This removes clutter completely, and allows one to run anaylsis on the data per subreddit - as each community and their impact will be entirely different. Also reads the text inside self posts and add those tickers to the count (both scores and mentions).

#V2.1

Because more data is always better than less, the program was made to colect High and Low data too. Additionally, the API was changed to yfinance - which makes the collection of all that data very easy.

For the sake of cleanliness of running areas, program creates an output folder which is where the csv files are created.