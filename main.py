
class Route:
    'Class for all routes'
    routeCount = 0
    
    def __init__(self, number, stops, buses, capacity):
        self.number = number
        self.stops = stops
        self.buses = buses
        self.capacity = capacity
        Route.routeCount += 1
        
class Road:
    'Class for all roads'
    roadCount = 0
    
    def __init__(self, starts, ends, rate):
        self.starts = starts
        self.ends = ends
        self.rate = rate
        Road.roadCount += 1
        
#Initialize variables
routes = []
roads = []
boardRate = 0
disembarkRate = 0
busDepartRate = 0
paxArrivalRate = 0
stopTime = 0
ignoreWarnings = False
optimiseParameters = False
 
def processLine(line):
    data = line.split(" ")
    object = data[0]
    if object == "route":
        stops = []
        for i in range(3, len(data)-4):
            stops.append(data[i])    
        routes.append(Route(data[1], stops, data[len(data)-3], data[len(data)-1]))
    if object == "road":
        roads.append(Road(data[1], data[2], data[3]))
    if object == "board":
        boardRate = data[1]
    if object == "disembarks":
        disembarkRate = data[1]
    if object == "departs":
        busDepartRate = data[1]
    if object == "new":
        paxArrivalRate = data[2]
    if object == "stop":
        stopTime = data[2]
    if object == "ignore":
        ignoreWarnings = True
    if object == "optimise":
        optimiseParameters = True
    return 

file = open('input.dat', 'r')

for line in file:
    processLine(line)
    
file.close()