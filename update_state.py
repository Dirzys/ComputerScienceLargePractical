from random import choice
import objects as new

def modify_state(state, event, time, listEvents):
    
    def updateBusInStop(bus):
        for stop in state.stops:
            if stop.id == bus.state:
                stop.add_bus(bus, time)
                break
    
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
                stop.add_passengers(new.Passenger(destinationId, buses, time))
        
        if listEvents:
            print 'A new passenger enters at stop ' + originId + ' with destination ' + destinationId +' at time ' + str(time)
    
    def boardsBus(pax, busId, stop):
        for possibleStop in state.stops:
            if stop.id == possibleStop.id:
                possibleStop.remove_passenger(pax, time)
                break
        for bus in state.buses:
            if bus.id == busId:
                bus.add_passenger(pax.changeTime(time))
                updateBusInStop(bus)
                break
        
        if listEvents:
            print 'Passenger boards bus ' + busId + ' at stop ' + stop.id + ' with destination ' + pax.destination + ' at time ' + str(time)
    
    def disembarksBus(pax, bus, stop):
        #Find route object for this bus
        for route in state.routes:
            if route.number == bus.id.split('.')[0]:
                chooseRoute = route
        for possibleBus in state.buses:
            if bus.id == possibleBus.id:
                possibleBus.remove_passenger(pax, time, chooseRoute)
                updateBusInStop(possibleBus)
                break
        
        if listEvents:
            print 'Passenger disembarks bus ' + bus.id + ' at stop ' + stop.id + ' at time ' + str(time)
    
    def arrivesAtStop(bus):
        stopId = bus.state.ends
        for possibleBus in state.buses:
            if bus.id == possibleBus.id:
                possibleBus.state = stopId
                updatedBus = possibleBus
                break
        updateBusInStop(updatedBus)
        
        if listEvents:
            print 'Bus ' + bus.id +' arrives at stop ' + stopId + ' at time ' + str(time)
        
    def leavesStop(bus):
        stopId = bus.state
        #Find next stop
        for route in state.routes:
            if route.number == bus.id.split('.')[0]:
                chooseRoute = route
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
                possibleBus.addJourney(chooseRoute) 
                break
        
        for stop in state.stops:
            if stopId == stop.id:
                #Remove bus from stop queue 
                stop.pop_bus(bus, time)
                #Find all passengers unable to board this bus due to full capacity
                for pax in stop.passengers:
                    if bus.id.split('.')[0] in pax.bus:
                        state.missPax(stopId, bus.id.split('.')[0])
                break
            
        if listEvents:
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