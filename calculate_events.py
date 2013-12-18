from objects import Road

def canBoardBus(state):
    ''' Find all passengers who can board some bus and add them to possible events list.
        Passenger can board bus only if all of the following holds true:
        --- Bus is at the same stop as passenger
        --- Bus is on top of the bus queue
        --- Bus is not on full capacity
        --- Passenger can reach his destination with this bus '''
    boardingRate = state.boards
    events = []
    for stop in state.stops:
        topBus = stop.top_bus()
        if topBus != 'None':
            if topBus.capacity > len(topBus.passengers):
                for pax in stop.passengers:
                    if topBus.id.split('.')[0] in pax.bus:
                        events.append((boardingRate, ['boards', pax, topBus.id, stop]))
    return events

def canDisembarkBus(state):
    ''' Find all passengers who can disembark some bus and add these events to possible events list.
        Passenger can disembark bus only if all of the following holds true:
        --- Bus is in the queue of some stop
        --- Passenger is in this bus
        --- Bus is on stop that is the same as passenger destination '''
    disembarkRate = state.disembarks
    events = []
    for stop in state.stops:
        for bus in stop.busQueue:
            for pax in bus.passengers:
                if pax.destination == stop.id:
                    events.append((disembarkRate, ['disembarks', pax, bus, stop]))
    
    return events

def canComeToStop(state):
    ''' Find all buses that can arrive in some stop.
        If bus is on some road then bus can come to stop that is at the end of this road '''
    events = []
    for bus in state.buses:
        if isinstance(bus.state, Road):
            events.append((float(bus.state.rate), ['comes', bus]))
    return events

def canLeaveStop(state):
    ''' Find all buses that can leave some stop.
        Bus can leave stop only if bus is in the bus queue of this stop and all of the following holds true:
        --- No passenger wants to disembark the bus at this stop
        --- No passenger wants to board the bus OR bus is on full capacity '''
    
    def noPaxToDisembark(bus, stop):
        for pax in bus.passengers:
            if pax.destination == stop.id:
                return False
        return True
    
    def noPaxToBoard(bus, stop):
        for pax in stop.passengers:
            if bus.id.split('.')[0] in pax.bus:
                return False
        return True
    
    busDepartsRate = state.busDeparts
    events = []
    for stop in state.stops:
        for bus in stop.busQueue:
            if noPaxToDisembark(bus, stop) and (noPaxToBoard(bus, stop) or (bus.capacity == len(bus.passengers))):
                events.append((busDepartsRate, ['departs', bus])) 
    return events

def get_possible_events(state):
    possibleEvents = []
    #New passenger can always arrive into the random stop with rate paxArrivalRate
    possibleEvents.append((state.paxArrives, ['newpax']))
    possibleEvents.extend(canBoardBus(state))
    possibleEvents.extend(canDisembarkBus(state))
    possibleEvents.extend(canComeToStop(state))
    possibleEvents.extend(canLeaveStop(state))
    return possibleEvents