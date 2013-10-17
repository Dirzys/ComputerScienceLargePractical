class State:
    'Class for state'
    
    def __init__(self, routes, roads, buses, stops, boards, disembarks, busDeparts, paxArrives, stopTime, ignore, optimise):
        self.routes = []
        self.roads = []
        self.buses = []
        self.stops = []
        self.boards = 0
        self.disembarks = 0
        self.busDeparts = 0
        self.paxArrives = 0
        self.stopTime = 0
        self.ignore = False
        self.optimise = False
        
    def add_routes(self, routes):
        self.routes.extend(routes)
            
    def add_roads(self, roads):
        self.roads.extend(roads)
            
    def add_buses(self, buses):
        self.buses.extend(buses)
            
    def add_stops(self, stops):
        self.stops.extend(stops)
            
    def changeBoards(self, rate):
        self.boards = rate
            
    def changeDisembarks(self, rate):
        self.disembarks = rate
            
    def changeBusDeparts(self, rate):
        self.busDeparts = rate
            
    def changePaxArrives(self, rate):
        self.paxArrives = rate
            
    def changeStopTime(self, time):
        self.stopTime = time
            
    def changeIgnore(self, value):
        self.ignore = value
            
    def changeOptimise(self, value):
        self.optimise = value

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
        
class Passenger:
    'Class for all passengers'
    
    def __init__(self, origin, destination, state):
        self.origin = origin
        self.destination = destination
        self.state = state
        
class Stop:
    'Class for all stops'
    
    def __init__(self, id, busQueue, passengers):
        self.id = id
        self.busQueue = busQueue
        self.passengers = []
        
    def add_passengers(self, passenger):
        self.passengers.append(passenger)

class Bus:
    'Class for all buses'
    
    def __init__(self, id, state):
        self.id = id
        self.state = state