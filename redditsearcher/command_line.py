#!/usr/bin/env python3
import fire
from main import analyze_subreddit


def main(subreddits: str):
    """
    redditsearcher - see what stonks are trending!
    :param subreddits: comma seperated list of subreddits to create reports for
    :return appends/created CSV files for newest subreddit posts, with each stock's \
        opening and closing dates, as well as high and low price, and volume.
    """
    print("ONLY RUN THIS AFTER 21:00 GMT")
    if isinstance(subreddits, tuple) is True:
        for count_value in enumerate(subreddits):
            analyze_subreddit(count_value[1])  # enumerate returns (count, value) tuple.
    else:
        analyze_subreddit(subreddits)


if __name__ == "__main__":
    print("""
    ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝
    ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║
    ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║
    ██║  ██║███████╗██████╔╝██████╔╝██║   ██║
    ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝

    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗███████╗██████╗
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗
    ███████╗█████╗  ███████║██████╔╝██║     ███████║█████╗  ██████╔╝
    ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  ██╔══██╗
    ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║███████╗██║  ██║
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
=====================================================================""")
    print()
    fire.Fire(main)
