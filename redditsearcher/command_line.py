from main import analyzeMentions, analyzeScores
import fire
import csv

def writeReport(my_dict, filename):
    with open(filename + '.csv', 'w') as f:  
        w = csv.writer(f)
        w.writerows(my_dict.items())
    print("Report generated called " + filename + ".csv")

def main(subreddits: str, operation="B"):
    """
    redditsearcher - see what stocks are trending!
    :param subreddits: comma seperated list of subreddits to create reports for
    :param operation: (M)entions, (S)cores, or (B)oth
    :return creates reports
    """
    operation = operation.upper()[0]
    if type(subreddits) is tuple:
        for i in range(0, len(subreddits)):
            if operation == "M":
                writeReport(analyzeMentions(subreddits[i]), subreddits[i] + "_mentions")
            elif operation == "S":
                writeReport(analyzeScores(subreddits[i]), subreddits[i] + "_scores")
            elif operation == "B":
                writeReport(analyzeMentions(subreddits[i]), subreddits[i] + "_mentions")
                writeReport(analyzeScores(subreddits[i]), subreddits[i] + "_scores")
            else:
                print("Invalid Operation!")
    else:
        if operation == "M":
            writeReport(analyzeMentions(subreddits), subreddits + "_mentions")
        elif operation == "S":
            writeReport(analyzeScores(subreddits), subreddits + "_scores")
        elif operation == "B":
            writeReport(analyzeMentions(subreddits), subreddits + "_mentions")
            writeReport(analyzeScores(subreddits), subreddits + "_scores")

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