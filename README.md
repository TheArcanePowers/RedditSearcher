# RedditSearcher
A simple commandline app for generating csv files to see the most mentioned and highest scoring US tickers in reddit subreddits.

Currently in **Alpha!**

# Installation
## Manual
```bash
  $ git clone https://github.com/thearcanepowers/redditsearcher
  $ cd redditsearcher
  $ python setup.py install
```

Do not forget to create a [praw.ini][https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html] file under the name of `main-bot`!

# Usage
```bash
$ redditsearcher --help
$ redditsearcher subreddits operation
```
## subreddits
comma seperated list of subreddits

## operation
Can be either:

**S**cores
**M**entions
**B**oth