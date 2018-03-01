"""
Google Hashcode 2018

MOVI team:

Huu Nghia NGUYEN
Vinh Hoa LA
Hoang Long MAI
Van Luong NGUYEN

"""
# Libraries to be imported
import sys
import signal
import time
from utils import *

# Global constants
OUTPUT_POSTFIX = "_movi.out"
OUTPUT_LOCATION = "output"

# Global variables
bestCore = 0
bestSolution = None

# Main functions

def signalHandler(sig, frame):
    """Print the best currently result
    
    Arguments:
        sig {Signal} -- Signal to be interupted
        frame {[type]} -- [description]
    """
    printBestSolution()

def printBestSolution():
    """Print the current best result
    """
    # print("Print the current best result: ")
    output_file = OUTPUT_LOCATION+"/" + str(bestCore) + "_" + str(int(time.time())) + OUTPUT_POSTFIX
    writeOutput(output_file, bestSolution)

def parseLineData(line, line_index):
    """Parse Line data based on the type of data line
    
    Arguments:
        line {[type]} -- [description]
        line_index {[type]} -- [description]
    """
    # TODO: To be completed!
    print (str(line_index) + " - " + line)
    # writeToFile('12' + OUTPUT_POSTFIX, line)

def readInput(file_path):
    """Read the input file
    
    Arguments:
        file_path {String} -- Path to the input file
    """
    # TODO: To be completed
    with open(file_path, 'r') as inputData:
        line_index = 0
        for line in inputData:
            line_index = line_index + 1
            parseLineData(line, line_index)

def writeOutput(file_path, solution):
    """Write the output of a solution to the file
    The file path should be in the format: score_timestamp.out
    
    Arguments:
        file_path {String} -- Output file
        solution {Object} -- A solution of the problem which need to be written in to the file
    """
    # TODO: To be completed
    writeToFile(file_path,"Solution")

def evaluate(solution):
    """Evaluate the score of the solution
    
    Arguments:
        solution {Object} -- The solution to be evaluated
    Return:
        The score of the solution
    """
    # TODO: to evaluate the solution

def solveProblem():
    """Solve the problem
    """
    # TODO: Solve the problem
    print("SolveProblem .... ")
    while True:
        print(".")

# Main functions

def start():
    # To be completed
    if (len(sys.argv) < 2):
        print ("[ERROR] Missing input")
        printHelp(sys.argv[0])
        return
    inputData = sys.argv[1]
    readInput(inputData)
    signal.signal(signal.SIGINT, signalHandler)
    solveProblem()

if __name__ == "__main__":
    start()
