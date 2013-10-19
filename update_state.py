from random import choice
import objects as new

def modify_state(state, event, time):
    
    def addNewPax():
        #Choosing random origin from all stops
        origin = choice(state.stops)
        originId = origin.id
        #Finding all possible destinations reachable by any route
        destinations = []
        for route in state.routes:
            if originId in route.stops:
                destinations.extend([dest for dest in route.stops if dest != originId])
        destinationId = choice(list(set(destinations)))
        buses = []
        #Finding all route numbers which can reach that destination
        for route in state.routes:
            if (destinationId in route.stops) and (originId in route.stops):
                buses.append(route.number)
        #Adding new passenger into the stop with id = originId
        for stop in state.stops:
            if stop.id == originId:
                stop.add_passengers(new.Passenger(destinationId, buses))
        #Output result
        print 'A new passenger enters at stop ' + originId + ' with destination ' + destinationId +' at time ' + str(time)
    
    def boardsBus(pax, busId, stop):
        for possibleStop in state.stops:
            if stop.id == possibleStop.id:
                possibleStop.remove_passenger(pax)
                break
        for bus in state.buses:
            if bus.id == busId:
                bus.add_passenger(pax)
                break
        #Output result
        print 'Passenger boards bus ' + busId + ' at stop ' + stop.id + ' with destination ' + pax.destination + ' at time ' + str(time)
    
    def disembarksBus(pax, bus, stop):
        for possibleBus in state.buses:
            if bus.id == possibleBus.id:
                possibleBus.remove_passenger(pax)
                break
        #Output result
        print 'Passenger disembarks bus ' + bus.id + ' at stop ' + stop.id + ' at time ' + str(time)
    
    def arrivesAtStop(bus):
        stopId = bus.state.ends
        for possibleBus in state.buses:
            if bus.id == possibleBus.id:
                possibleBus.state = stopId
                break
        for stop in state.stops:
            if stop.id == stopId:
                stop.add_bus(bus)
                break
        #Output result
        print 'Bus ' + bus.id +' arrives at stop ' + stopId + ' at time ' + str(time)
        
    def leavesStop(bus):
        stopId = bus.state
        #Find next stop
        for route in state.routes:
            if route.number == bus.id.split('.')[0]:
                nextStopIndex = (route.stops.index(stopId) + 1) % len(route.stops)
                nextStop = route.stops[nextStopIndex]
                break
        #Find road from this stop to the next one
        for road in state.roads:
            if road.starts == stopId and road.ends == nextStop:
                chooseRoad = road
                break
        #Change the state of the bus
        for possibleBus in state.buses:
            if bus.id == possibleBus.id:
                possibleBus.state = chooseRoad 
                break
        #Remove bus from stop queue 
        for stop in state.stops:
            if stopId == stop.id:
                stop.pop_bus(bus)
                
        #Output result
        print 'Bus ' + bus.id +' leaves stop ' + stopId + ' at time ' + str(time)
        
    type = event[0]
    if type == 'newpax':
        addNewPax()
    elif type == 'boards':
        boardsBus(event[1], event[2], event[3])
    elif type == 'disembarks':
        disembarksBus(event[1], event[2], event[3])
    elif type == 'comes':
        arrivesAtStop(event[1])
    elif type == 'departs':
        leavesStop(event[1])
    else:
        raise Exception, ': incorrect event type'
    return state