# Pre-Alpha
Initially, the program created seperate reports of most mentioned and highest scoring posts in the newest week on various subreddits.

Unfortunately this ended up outputting a multitude of files per subreddit:
And realistically, this barely addressed the actual aim of the program.

# Alpha
Thus entered **Verson 2**, which created a csv separated database per subreddit listing all the stocks mentioned and upvoted daily, and with their stock opening and closing prices. Additionally, running it appends the daily report to pre-existing csv files per subreddit.

This removes clutter completely, and allows one to run anaylsis on the data per subreddit - as each community and their impact will be entirely different. Also reads the text inside self posts and add those tickers to the count (both scores and mentions).

## Alpha-2

Because more data is always better than less, the program was made to colect High and Low data too. Additionally, the API was changed to yfinance - which makes the collection of all that data very easy.

For the sake of cleanliness of running areas, program creates an output folder which is where the csv files are created.

## The first run / Alpha-3
The first run taught me a few things. Most importantly, don't ever rely on human input to play nice.
Errors were being thrown left and right, and it turned out random words like "HOLD" passed both the re ticker checker, the actual ticker checker (as it was a valid ticker) but was actually unlisted! Thus, erroring out a function that was behind two safeguards.

Easy fix, just a try, except to return error values and allow the rest of the operation to continue. Along with this, the day's outputs were quickly looked over, and any clear false tickers were added to either the common or subreddit-specific blocklist. 

Thus introduces **version 2.1**. !!Soon, version 2.2 will include proper try except catces on all functions dealing with human input!!

# Now in Beta!

Discovering the functionality of Linting, I experimented with various linters such as flask8 and the ubiquitous pylint. Thus, this update ensured PEP8 compliance and overhauled the code, incorporating some error catching (such as subreddit verification and PRAW credential checking.)

In going over the code, I noticed there was quite a bit of room for improvement, and these have been mentioned in block comments. These will need to be addressed before leaving beta, as well as being packaged properly for a mock-pypi upload.

# Production/Stable