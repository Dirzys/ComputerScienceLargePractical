
class State:
    'Class for state'
    
    def __init__(self, routes, roads, buses, stops, boards, disembarks, busDeparts, paxArrives, stopTime, ignore, optimise):
        self.routes = routes
        self.roads = roads
        self.buses = buses
        self.stops = stops
        self.boards = boards
        self.disembarks = disembarks
        self.busDeparts = busDeparts
        self.paxArrives = paxArrives
        self.stopTime = stopTime
        self.ignore = ignore
        self.optimise = optimise
        
    def add_route(self, route):
        self.routes.append(route)
            
    def add_road(self, road):
        self.roads.append(road)
            
    def add_bus(self, bus):
        self.buses.append(bus)
            
    def add_stop(self, stop):
        stop = stop if not stop.id in [existingStop.id for existingStop in self.stops] else []
        if stop != []:
            self.stops.append(stop)
            
    def changeBoards(self, rate):
        self.boards = float(rate)
            
    def changeDisembarks(self, rate):
        self.disembarks = float(rate)
            
    def changeBusDeparts(self, rate):
        self.busDeparts = float(rate)
            
    def changePaxArrives(self, rate):
        self.paxArrives = float(rate)
            
    def changeStopTime(self, time):
        self.stopTime = float(time)
            
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
        
    def top_bus(self):
        return self.busQueue[0]

class Bus:
    'Class for all buses'
    
    def __init__(self, id, state):
        self.id = id
        self.state = state