
class State:
    ''' Class for state object '''
    
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
        #Information about how many passengers have been 
        #missed due full capacity of the bus
        self.missedPaxOnStop = {}
        self.missedPaxOnRoute = {}
        self.missedTotal = 0
        
    def add_route(self, route):
        self.routes.append(route)
        self.missedPaxOnRoute[route.number] = 0 
            
    def add_road(self, road):
        self.roads.append(road)
            
    def add_bus(self, bus):
        self.buses.append(bus)
        
    def remove_bus(self, bus):
        self.buses = [busIn for busIn in self.buses if not bus.__dict__ == busIn.__dict__]
            
    def add_stop(self, stop):
        stop = stop if not stop.id in [existingStop.id for existingStop in self.stops] else []
        if stop != []:
            self.stops.append(stop)
            self.missedPaxOnStop[stop.id] = 0
            
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
        self.missedPaxOnStop[stopId] += 1
        self.missedPaxOnRoute[routeId] += 1
        self.missedTotal += 1
            
class Route:
    ''' Class for all routes '''
    
    def __init__(self, number, stops, buses, capacity):
        self.number = number
        self.stops = stops
        self.buses = buses
        self.capacity = capacity
        #Information about how many passengers use buses of this route
        self.numOfPaxIn = 0
        self.journeysMade = 0
        #Information about how long passengers wait at buses of this route
        self.timePaxWaitsOnRoute = 0.0
        self.paxWaited = 0
        
    def changeBusNr(self, buses):
        self.buses = buses
        
    def changeCapacity(self, capacity):
        self.capacity = int(capacity)
        
class Road:
    ''' Class for all roads '''
    
    def __init__(self, starts, ends, rate):
        self.starts = starts
        self.ends = ends
        self.rate = float(rate)
        
    def change_rate(self, rate):
        self.rate = float(rate)
        
    def __eq__(self, other) : 
        ''' Checking if two Road classes have the same information (are the same) '''
        return self.__dict__ == other.__dict__
        
class Passenger:
    ''' Class for all passengers '''
    
    def __init__(self, destination, bus, time):
        self.destination = destination
        self.bus = bus
        self.time = float(time)
    
    def changeTime(self, time):
        ''' Used then passenger boards the bus, i.e. 
            stops waiting for bus and starts waiting at the route '''
        self.time = float(time)
        return self
        
class Stop:
    ''' Class for all stops '''
    
    def __init__(self, id, busQueue, passengers):
        self.id = id
        self.busQueue = busQueue
        self.passengers = passengers
        #Information about how long buses wait at queues
        self.timeOfWaiting = 0.0
        self.busesWaited = 0
        self.busArrivedOn = {}
        #Information about how long passengers wait at stop
        self.timePaxWaitsOnStop = 0.0
        self.paxWaited = 0
        
    def add_passengers(self, passenger):
        self.passengers.append(passenger)
        
    def remove_passenger(self, passenger, time):
        self.passengers = [pax for pax in self.passengers if not passenger.__dict__ == pax.__dict__]
        #Since passenger boards the bus, it means he stopped waiting
        self.timePaxWaitsOnStop += time - passenger.time
        self.paxWaited += 1
        
    def pop_bus(self, bus, time):
        # If popping top bus, the new top bus no longer considered as waiting in the queue
        if self.top_bus().id == bus.id:
            self.busQueue.remove(bus)
            busStopsWaiting = self.top_bus()
        # If popping not the top bus, this bus no longer considered as waiting in the queue    
        else:
            busStopsWaiting = bus    
            self.busQueue.remove(bus)
        
        #Bus that needs to stop waiting is removed from waiting list and added into stop statistics
        if busStopsWaiting != 'None':
            busId = busStopsWaiting.id
            self.timeOfWaiting += time - self.busArrivedOn[busId]
            self.busesWaited += 1 
            del self.busArrivedOn[busId]
        
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
        #However, if the bus is alone at the stop, it does not need to wait
        if self.top_bus().id == bus.id:
            self.busesWaited += 1
        else:
            self.busArrivedOn[bus.id] = time 
        
class Bus:
    ''' Class for all buses '''
    
    def __init__(self, id, routeNr, state, passengers, capacity):
        self.id = id
        self.routeNr = routeNr
        self.state = state
        self.passengers = passengers
        self.capacity = capacity
        #Information about how many passengers use this bus
        self.numOfPaxIn = 0
        self.journeysMade = 0
        
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        
    def change_capacity(self, capacity):
        self.capacity = capacity
        
    def remove_passenger(self, passenger, time, route):
        self.passengers = [pax for pax in self.passengers if not passenger.__dict__ == pax.__dict__]
        #Since passenger disembarks the bus, it means he stopped waiting
        route.timePaxWaitsOnRoute += time - passenger.time
        route.paxWaited += 1
        
    def addJourney(self, route):
        ''' Whenever bus leaves the stop (starts driving the road) 
            it starts new journey and the statistics are captured for future analysis '''
        self.numOfPaxIn += len(self.passengers)
        self.journeysMade += 1
        route.numOfPaxIn += len(self.passengers)
        route.journeysMade += 1