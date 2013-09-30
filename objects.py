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