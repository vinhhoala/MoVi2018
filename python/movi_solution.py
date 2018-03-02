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
import random

# Global constants
OUTPUT_POSTFIX = "_movi.out"
OUTPUT_LOCATION = "output"
MIN_DISTANCE = 0

# Global variables
bestCore = 0
bestSolution = None
list_rides = []
list_vehicles = []
# Main functions

class Vehicle:
    def __init__(self, id, x, y, steps):
        self.id = id
        self.x = x
        self.y = y
        self.remain_steps = 0
        self.rides = []
        self.last_finish = 0

    def takeRide(self, ride):
        self.rides.append(ride)
        self.last_finish = ride.l_finish
        self.x = ride.end_x
        self.y = ride.end_y
        self.remain_steps = ride.distance

class CityMap:
    def init(self, rows, cols, nb_rides, nb_vehicle, bonus, steps, file_path):
        self.rows = rows
        self.cols = cols
        self.nb_rides = nb_rides
        self.nb_vehicle = nb_vehicle
        self.bonus = bonus
        self.steps = steps
        self.data = [[0 for c in range(cols)] for r in range(rows)]
        self.file_path = file_path

class Ride:
    def __init__(self, r_id,  start_x, start_y, end_x, end_y, e_start, l_finish ):
        self.ride_id = r_id
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.e_start = e_start + getDistance(0,0,start_x, start_y)
        self.l_finish = l_finish
        self.distance = getDistance(start_x, start_y, end_x, end_y)
        self.timegap = l_finish - e_start
        self.status = 0 # 1 means that it has been taken

def getDistance(start_x, start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)

def printHelp(appName):
    """Print out the message if the user does not enter correct parameter

    Arguments:
        appName {String} -- String name
    """
    print("Usage:")
    print('\tpython ' + appName + ' <Input_data_file>')


def writeToFile(file_path, content):
    """Append a content to a file

    Arguments:
        file_path {String} -- Path of output file
        content {String} -- Content to be written
    """

    output = open(file_path, 'a')
    output.write(content)
    output.close()

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
                city_map.init(rows,cols,nb_rides,nb_vehicle,bonus,steps,file_path)
                for v in range(nb_vehicle):
                    new_vehicle = Vehicle(v, 0, 0, steps)
                    list_vehicles.append(new_vehicle)
            else:
                new_ride = parseRideData(line, line_index - 2)
                if(new_ride.distance + getDistance(0,0,new_ride.start_x, new_ride.start_y) < steps and new_ride.distance > MIN_DISTANCE):
                    list_rides.append(new_ride)

def writeOutput():
    """Write the output of a solution to the file
    The file path should be in the format: score_timestamp.out

    Arguments:
        file_path {String} -- Output file
        solution {Object} -- A solution of the problem which need to be written in to the file
    """
    output_time = str(int(time.time()))
    for veh in list_vehicles:
        output = str(len(veh.rides))
        for r in veh.rides:
            output = output + ' ' + str(r.ride_id)
        writeToFile(city_map.file_path + '_movi_' + output_time + '.out', output + "\n")


def evaluate(solution):
    """Evaluate the score of the solution

    Arguments:
        solution {Object} -- The solution to be evaluated
    Return:
        The score of the solution
    """
    # TODO: to evaluate the solution

def random_nb_ride(nb_remain_ride, nb_remain_vehicle):
    if(nb_remain_ride == 1):
        return 1
    else:
        return int(nb_remain_ride/nb_remain_vehicle)
        # return random.randint(0,int(nb_remain_ride/nb_remain_vehicle + 10))

def solveProblem():
    """Solve the problem
    """
    # TODO: Solve the problem

    # Preprocess data
    list_rides.sort(key=lambda x:x.e_start, reverse=True)
    while len(list_rides) > 0:
        for v in range(city_map.nb_vehicle):
            if len(list_rides) > 0:
                current_ride = list_rides.pop()
                list_vehicles[v].takeRide(current_ride)
            else:
                break
    writeOutput()

def findARide(v, list_rides, steps):
    # find all possible ride which the given vehicle can take and have score:
    # list_possible_rides = []
    remain_steps = city_map.steps - steps
    if len(list_rides) < 1:
        print("No ride to take")
        return None
    closest_ride = None
    min_distance = city_map.rows + city_map.cols
    earlest_ride = None
    min_time = remain_steps
    longest_ride = None
    longest_distance = 0
    max_score = 0
    max_ride = None
    r_index = 0
    shortest_ride = None
    shortest_distance = city_map.rows + city_map.cols

    for r in list_rides:
        distance = getDistance(v.x, v.y, r.start_x, r.start_y)
        # Find the best score ride
        # score = 0
        # if distance + steps < r.e_start:
        #     score = score + city_map.bonus
        # if distance + r.distance < remain_steps:
        #     score = score + r.distance
        # if max_score < score:
        #     max_score = score
        #     max_ride = r_index

        # if distance + r.distance < remain_steps:
        if min_distance > distance:
            min_distance = distance
            closest_ride = r_index
        if min_time > r.e_start:
            min_time = r.e_start
            earlest_ride = r_index
        if longest_distance < r.distance:
            longest_ride = r_index
            longest_distance = r.distance
        if shortest_distance > r.distance:
            shortest_distance = r.distance
            shortest_ride = r_index
        # list_possible_rides.append(r)
        r_index = r_index + 1
    # return earlest_ride # can choose longest_ride, earlest_ride or closest_ride
    # return max_ride # can choose longest_ride, earlest_ride or closest_ride
    # return closest_ride # can choose longest_ride, earlest_ride or closest_ride
    return shortest_ride # can choose longest_ride, earlest_ride or closest_ride
    # return longest_ride # can choose longest_ride, earlest_ride or closest_ride

def solveProblem2():
    # Preprocess data
    # list_rides.sort(key=lambda x:x.e_start, reverse=True)
    for step in range(city_map.steps):
        # Simulate the city: Update status of vehicle for each step
        for v in list_vehicles:
            if v.remain_steps > 0:
                # This vehicle still busy
                v.remain_steps = v.remain_steps - 1
            else:
                # This vehicle is free - find a ride
                ride_index = findARide(v, list_rides, step)
                if ride_index != None:
                    v.takeRide(list_rides[ride_index])
                    list_rides.remove(list_rides[ride_index])
                else:
                    writeOutput()
                    return
    writeOutput()

def getVehicule(ride, steps):
    first_veh = None
    closest_veh = None
    min_distance = city_map.rows + city_map.cols
    v_index = 0
    min_distance = city_map.rows + city_map.cols
    for v in list_vehicles:
        if v.remain_steps == 0:
            distance = getDistance(v.x, v.y, ride.start_x, ride.start_y)
            if (distance + ride.distance < city_map.steps - steps) and first_veh == None:
                first_veh = v_index
            if min_distance > distance:
                min_distance = distance
                closest_veh = v_index

    return first_veh


def solveProblem3():
    for steps in range(city_map.steps):
        # Simulate the city after each steps
        # Update remain steps of vehicules
        for v in list_vehicles:
            if v.remain_steps > 0:
                v.remain_steps = v.remain_steps - 1

        # Find a vehicule for current ride
        for r in list_rides:
            v = getVehicule(r, steps)
            if v!= None:
                list_vehicles[v].takeRide(r)
                list_rides.remove(r)
    writeOutput()

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
    # showInput()
    print(city_map.rows)
    print(city_map.cols)
    print(city_map.nb_rides)
    print(city_map.nb_vehicle)
    # for v in list_rides:
    #     print(json.dumps(v.__dict__))

    # for v in list_vehicles:
    #     print(json.dumps(v.__dict__))

    # signal.signal(signal.SIGINT, signalHandler)
    solveProblem3()

if __name__ == "__main__":
    start()
