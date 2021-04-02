from main import analyzeSubreddit
import fire
import csv

def main(subreddits: str):
    """
    redditsearcher - see what stonks are trending!
    :param subreddits: comma seperated list of subreddits to create reports for
    :return appends/created CSV files for newest subreddit posts, with their opening and closing dates.
    """
    print("ONLY RUN THIS AFTER 21:00 GMT")
    
    if type(subreddits) is tuple:
        for i in range(0, len(subreddits)):
            analyzeSubreddit(subreddits[i])
    else:
        analyzeSubreddit(subreddits)

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