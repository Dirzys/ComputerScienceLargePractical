import objects

def processLine(line, state):
    data = line.split(" ")
    object = data[0]
    if object == "route":
        stops = []
        for i in range(3, len(data)-4):
            stops.append(data[i])    
        state[0].append(objects.Route(data[1], stops, data[len(data)-3], data[len(data)-1]))
    if object == "road":
        state[1].append(objects.Road(data[1], data[2], data[3]))
    if object == "board":
        state[2] = data[1]
    if object == "disembarks":
        state[3] = data[1]
    if object == "departs":
        state[4] = data[1]
    if object == "new":
        state[5] = data[2]
    if object == "stop":
        state[6] = data[2]
    if object == "ignore":
        state[7] = True
    if object == "optimise":
        state[8] = True
    return 

def readFromFile(fileToRead):
    file = open(fileToRead, 'r')
    #Initialize variables
    #order routes, roads, boardRate, disembarkRate, busDepartRate, 
    #paxArrivalRate, stopTime, ignoreWarning, optimiseParameters
    state = [[], [], 0, 0, 0, 0, 0, False, False]
    
    for line in file:
        processLine(line, state)
    
    file.close()
    return state