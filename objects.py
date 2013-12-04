
class State:
    'Class for state'
    
    missedPaxOnStop = {}
    missedPaxOnRoute = {}
    missedTotal = 0
    
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
        
    def remove_bus(self, bus):
        self.buses.remove(bus)
            
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
    
    def missPax(self, stopId, routeId):
        if stopId in State.missedPaxOnStop:
            State.missedPaxOnStop[stopId] += 1
        else:
            State.missedPaxOnStop[stopId] = 1
        if routeId in State.missedPaxOnRoute:
            State.missedPaxOnRoute[routeId] += 1
        else:
            State.missedPaxOnRoute[routeId] = 1
        State.missedTotal += 1
            
class Route:
    'Class for all routes'
    
    #Keeping information about how long passengers wait at route
    timePaxWaitsOnRoute = {}
    paxWaited = {}
    
    def __init__(self, number, stops):
        self.number = number
        self.stops = stops
        self.numOfPaxIn = 0
        self.journeysMade = 0
        Route.timePaxWaitsOnRoute[self.number] = 0.0
        Route.paxWaited[self.number] = 0
        
class Road:
    'Class for all roads'
    
    def __init__(self, starts, ends, rate):
        self.starts = starts
        self.ends = ends
        self.rate = rate
        
    def change_rate(self, rate):
        self.rate = rate
        
class Passenger:
    'Class for all passengers'
    
    def __init__(self, destination, bus, time):
        self.destination = destination
        self.bus = bus
        self.time = time
    
    def changeTime(self, time):
        self.time = time
        return self
        
class Stop:
    'Class for all stops'
    
    #Keeping information about how long buses wait at queues
    timeOfWaiting = {}
    busesWaited = {}
    busArrivedOn = {}
    #Keeping information about how long passengers wait at stops
    timePaxWaitsOnStop = {}
    paxWaited = {}
    
    def __init__(self, id, busQueue, passengers):
        self.id = id
        self.busQueue = busQueue
        self.passengers = passengers
        Stop.timeOfWaiting[self.id] = 0.0
        Stop.busesWaited[self.id] = 0
        Stop.timePaxWaitsOnStop[self.id] = 0.0
        Stop.paxWaited[self.id] = 0
        
    def add_passengers(self, passenger):
        self.passengers.append(passenger)
        
    def remove_passenger(self, passenger, time):
        self.passengers.remove(passenger)
        #Since passenger boards the bus, it means he stopped waiting
        Stop.timePaxWaitsOnStop[self.id] += time - passenger.time
        Stop.paxWaited[self.id] += 1
        
    def pop_bus(self, bus, time):
        # If popping top bus, the new top bus no longer considered as waiting in the queue
        if self.top_bus() == bus:
            self.busQueue.remove(bus)
            busStopsWaiting = self.top_bus()
        # If popping not the top bus, this bus no longer considered as waiting in the queue    
        else:
            busStopsWaiting = bus    
            self.busQueue.remove(bus)
        
        #Bus that needs to stop waiting is removed from waiting list and added into stop statistics
        if busStopsWaiting != 'None':
            busId = busStopsWaiting.id
            Stop.timeOfWaiting[self.id] += time - Stop.busArrivedOn[busId]
            Stop.busesWaited[self.id] += 1 
            del Stop.busArrivedOn[busId]
        
    def top_bus(self):
        return self.busQueue[0] if not len(self.busQueue) == 0 else 'None'
    
    def add_bus(self, bus, time):
        #If bus have already been in the queue, just update that bus
        for existingBus in self.busQueue:
            if bus.id == existingBus.id:
                existingBus = bus
                return
        #Otherwise add the bus to the queue and save the time it arrived here
        self.busQueue.append(bus)
        Stop.busArrivedOn[bus.id] = time 
        
class Bus:
    'Class for all buses'
    
    def __init__(self, id, state, passengers, capacity):
        self.id = id
        self.state = state
        self.passengers = passengers
        self.capacity = capacity
        self.numOfPaxIn = 0
        self.journeysMade = 0
        
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        
    def change_capacity(self, capacity):
        self.capacity = capacity
        
    def remove_passenger(self, passenger, time):
        self.passengers.remove(passenger)
        #Since passenger disembarks the bus, it means he stopped waiting
        Route.timePaxWaitsOnRoute[self.id.split('.')[0]] += time - passenger.time
        Route.paxWaited[self.id.split('.')[0]] += 1
        
    def addJourney(self, route):
        self.numOfPaxIn += len(self.passengers)
        self.journeysMade += 1
        route.numOfPaxIn += len(self.passengers)
        route.journeysMade += 1
        