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
import json
from utils import *

# Global constants
OUTPUT_POSTFIX = "_movi.out"
OUTPUT_LOCATION = "output"

# Global variables
bestCore = 0
bestSolution = None
list_rides = []

# Main functions

class Vehicle:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class CityMap:
    def init(self, rows, cols, nb_rides, nb_vehicle, bonus, steps):
        self.rows = rows
        self.cols = cols
        self.nb_rides = nb_rides
        self.nb_vehicle = nb_vehicle
        self.bonus = bonus
        self.steps = steps
        self.data = [[0 for c in range(cols)] for r in range(rows)]

class Ride:
    def __init__(self, r_id,  start_x, start_y, end_x, end_y, e_start, l_finish ):
        self.ride_id = r_id
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.e_start = e_start
        self.l_finish = l_finish

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

def parseRideData(line, line_index):
    """Parse Line data based on the type of data line
    
    Arguments:
        line {[type]} -- [description]
        line_index {[type]} -- [description]
    """
    array = line.split()
    new_ride = Ride(line_index, int(array[0]), int(array[1]), int(array[2]), int(array[3]), int(array[4]), int(array[5]))
    return new_ride

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
            if line_index == 1:
                # initialize
                array = line.split(' ')
                rows = int(array[0])
                cols = int(array[1])
                nb_vehicle = int(array[2])
                nb_rides = int(array[3])
                bonus = int(array[4])
                steps = int(array[5])
                city_map.init(rows,cols,nb_rides,nb_vehicle,bonus,steps)
            else:
                new_ride = parseRideData(line, line_index - 1)
                list_rides.append(new_ride)

def writeOutput(file_path, solution):
    """Write the output of a solution to the file
    The file path should be in the format: score_timestamp.out
    
    Arguments:
        file_path {String} -- Output file
        solution {Object} -- A solution of the problem which need to be written in to the file
    """
    # TODO: To be completed

def evaluate(solution):
    """Evaluate the score of the solution
    
    Arguments:
        solution {Object} -- The solution to be evaluated
    Return:
        The score of the solution
    """
    # TODO: to evaluate the solution

def random_nb_ride(nb_remain_ride):
    return random.randint(1,nb_remain_ride)

def solveProblem():
    """Solve the problem
    """
    # TODO: Solve the problem
    nb_remain_ride = city_map.nb_rides
    for v in range(city_map.nb_vehicle):
        nb_ride = random_nb_ride(nb_remain_ride)
        for r in range(nb_ride):
            
            output = str(nb_ride) + 


def showInput():
    print("Map:")
    print(json.dumps(city_map.__dict__))
    for ride in list_rides:
        print(json.dumps(ride.__dict__))

# Main functions

city_map = CityMap()

def start():
    # To be completed
    if (len(sys.argv) < 2):
        print ("[ERROR] Missing input")
        printHelp(sys.argv[0])
        return
    inputData = sys.argv[1]
    readInput(inputData)

    showInput()

    signal.signal(signal.SIGINT, signalHandler)
    solveProblem()

if __name__ == "__main__":
    start()
