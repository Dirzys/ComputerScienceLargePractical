import objects as new
from collections import deque

def addBusesToNetwork(busNumber, busCount, stops, state):
    for i in range(0, int(busCount)):
        state[2].append(new.Bus(busNumber + '.' + str(i), ('atStop', stops[i % len(stops)])))
        
def addStopToNetwork(stopId, state):
    for stop in state[3]:
        if stop.id == stopId:
            return
    state[3].append(new.Stop(stopId, deque([]), []))

def processLine(line, state):
    data = line.split(" ")
    object = data[0]
    if object == "route":
        stops = []
        for i in range(3, len(data)-4):
            stops.append(data[i])
            addStopToNetwork(data[i], state)
        buses = data[len(data)-3]    
        state[0].append(new.Route(data[1], stops, buses, data[len(data)-1]))
        addBusesToNetwork(data[1], buses, stops, state)
    if object == "road":
        addStopToNetwork(data[1], state)
        addStopToNetwork(data[2], state)
        state[1].append(new.Road(data[1], data[2], data[3]))
    if object == "board":
        state[5] = data[1]
    if object == "disembarks":
        state[6] = data[1]
    if object == "departs":
        state[7] = data[1]
    if object == "new":
        state[8] = data[2]
    if object == "stop":
        state[9] = data[2]
    if object == "ignore":
        state[10] = True
    if object == "optimise":
        state[11] = True
    return 

def readFromFile(fileToRead):
    file = open(fileToRead, 'r')
    #Initialize variables
    #order routes, roads, buses, stops, passengers, boardRate, disembarkRate, busDepartRate, 
    #paxArrivalRate, stopTime, ignoreWarning, optimiseParameters
    state = [[], [], [], [], [], 0, 0, 0, 0, 0, False, False]
    
    for line in file:
        processLine(line, state)
    
    file.close()
    return state