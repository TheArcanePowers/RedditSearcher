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