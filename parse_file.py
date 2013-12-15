from objects import *
from collections import deque
import itertools
from copy import deepcopy

def addBusesToNetwork(busNumber, busCount, stops, state, capacity):
    for i in range(0, int(busCount)):
        state.add_bus(Bus(busNumber + '.' + str(i), stops[i % len(stops)], [], capacity))
    return state
        
def addStopToNetwork(stopId, state):
    state.add_stop(Stop(stopId, deque([]), []))
    return state

def addBusesToStops(state):
    for stop in state.stops:
        for bus in state.buses:
            if bus.state == stop.id:
                stop.add_bus(bus, 0.0)
        stop.busQueue = sorted(stop.busQueue)
    return state

def findExperiment(data, i, model):
    ''' Finds experiment in the input line where 
        the first value for experiment is in position i '''
    experiment = None
    #Find the rate if no experiment presents
    rate = data[i]
    #If there is an experiment - find the first possible rate and add other to experiment list
    if rate == "experiment":
        experiment = []
        rate = data[i+1]
        for k in range(i+1, len(data)):
            experiment.append(model + [float(data[k])])
    return rate, experiment

def parseRoute(data, state):
    ''' Parses route given the data line for route'''
    experimentBuses = experimentCap = None
    routeNr = data[1]
    stops = []
    #Add all stops found in this route to the network
    i = 3
    while data[i] != "buses":
        stops.append(data[i])
        addStopToNetwork(data[i], state)
        i += 1
    #Find the number of buses if no experiment presents
    buses = data[i+1]
    j = i + 2 #Place where the 'capacity' should be kept if no experiment of number of buses found
    #If there is an experiment here - find the first number of buses and add other to experiment list
    if buses == "experiment":
        experimentBuses = []
        buses = data[i+2]
        while data[j] != "capacity":
            experimentBuses.append(["buses", routeNr, int(data[j])])
            j += 1
            
    capacity, experimentCap = findExperiment(data, j+1, ["capacity", routeNr]) 
    #Finally add routes and buses to the network
    state.add_route(Route(routeNr, stops))
    state = addBusesToNetwork(routeNr, buses, stops, state, int(capacity))
    return state, experimentBuses, experimentCap

def processLine(line, state):
    data = line.split(" ")
    object = data[0]
    experiment = experimentAddi = None
    if object == "route":
        state, experiment, experimentAddi = parseRoute(data, state)
    elif object == "road":
        addStopToNetwork(data[1], state)
        addStopToNetwork(data[2], state)
        rate, experiment = findExperiment(data, 3, [object, data[1], data[2]])
        state.add_road(Road(data[1], data[2], rate))
    elif object == "board":
        rate, experiment = findExperiment(data, 1, [object])
        state.changeBoards(rate)
    elif object == "disembarks":
        rate, experiment = findExperiment(data, 1, [object])
        state.changeDisembarks(rate)
    elif object == "departs":
        rate, experiment = findExperiment(data, 1, [object])
        state.changeBusDeparts(rate)
    elif object == "new":
        rate, experiment = findExperiment(data, 2, [object + " passengers"])
        state.changePaxArrives(rate)
    elif object == "stop":
        state.changeStopTime(data[2])
    elif object == "ignore":
        state.changeIgnore(True)
    elif object == "optimise":
        state.changeOptimise(True)
    elif not (object[0] == "#" or object == "\n"):
        raise Exception, 'incorrect input - %s' % line        
    return state, experiment, experimentAddi

def modifyState(state, change):
    if change[0] == 'buses':
        #Removing all buses from route change[1]
        remove = []
        for bus in state.buses:
            if bus.id.split('.')[0] == change[1]:
                capacity = bus.capacity #Saving the capacity
                remove.append(bus)
        for bus in remove:
            state.remove_bus(bus)
        #Finding all stops of route change[1]
        for route in state.routes:
            if route.number == change[1]:
                stops = route.stops
        #Adding new buses - there will be change[2] of them
        state = addBusesToNetwork(change[1], change[2], stops, state, capacity)
    if change[0] == 'capacity':
        for bus in state.buses:
            if bus.id.split('.')[0] == change[1]:
                bus.change_capacity(change[2])
    if change[0] == 'road':
        for road in state.roads:
            if road.starts == change[1] and road.ends == change[2]:
                road.change_rate(change[3])
                break
    if change[0] == 'board':
        state.changeBoards(change[1])
    if change[0] == 'disembarks':
        state.changeDisembarks(change[1])
    if change[0] == 'departs':
        state.changeBusDeparts(change[1])
    if change[0] == 'new passengers':
        state.changePaxArrives(change[1])
    return state

def addStateForExperiment(experiment, state):
    ''' Creates new state by modifying given state 
        with the new values in the experiment '''
    for change in experiment:
        state = modifyState(state, change)
    return state

def readFromFile(fileToRead):
    ''' Parses file, finds experiments and creates states for each of the experiment '''
    
    try:
        file = open(fileToRead, 'r')
    except IOError:
        print 'Error! No such file or directory: %s' % fileToRead
        return
    #Initialize variables
    #order routes, roads, buses, stops, passengers, boardRate, disembarkRate, busDepartRate, 
    #paxArrivalRate, stopTime, ignoreWarning, optimiseParameters
    state = State([], [], [], [], 0, 0, 0, 0, 0, False, False)
    experiments = []
    
    for line in file:
        experiment = None
        try:
            state, experiment, experimentAddi = processLine(line, state)
        except IndexError as l:
            print 'Error! Incorrect input'
            return 
        if experiment:
            experiments.append(experiment)
        if experimentAddi:
            experiments.append(experimentAddi)
            
    file.close() 
    states = [state]
    #Now need to get all possible variations of experiments
    variations = list(itertools.product(*experiments))
    states = [(state, variations[0])]
    for variation in variations[1:]: #First variation already added as a state
        states.append((addStateForExperiment(variation, deepcopy(state)), variation))

    return [(addBusesToStops(state), vari) for state, vari in states]