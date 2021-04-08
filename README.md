# RedditSearcher
A simple commandline app for generating csv files to see the most mentioned and highest scoring US tickers in reddit subreddits.

Currently in **Beta**

Program will create an entry for each ticker mentioned in the last day in each subreddit given, and generate a CSV entry with the number of mentions, total score of all posts, and adjusted stock prices at start and end of market.

# Installation
## Manual
```bash
  $ git clone https://github.com/thearcanepowers/redditsearcher
  $ cd redditsearcher
  $ python setup.py install
```

Do not forget to create a [praw.ini][https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html] file under the name of `[main-bot]`!

# Usage
```bash
$ redditsearcher --help
$ redditsearcher subreddit1,subreddit2,...
```
## subreddits
subreddits can be as many as wanted, written as a comma seperated list.

