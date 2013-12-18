from objects import Road

def canBoardBus(state):
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
    disembarkRate = state.disembarks
    events = []
    for stop in state.stops:
        for bus in stop.busQueue:
            for pax in bus.passengers:
                if pax.destination == stop.id:
                    events.append((disembarkRate, ['disembarks', pax, bus, stop]))
    
    return events

def canComeToStop(state):
    events = []
    for bus in state.buses:
        if isinstance(bus.state, Road):
            events.append((float(bus.state.rate), ['comes', bus]))
    return events

def canLeaveStop(state):
    
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
    #Find all passengers who can board some bus and add them to possible events list
    possibleEvents.extend(canBoardBus(state))
    #Find all passengers who can disembark some bus and add these events to possible events list
    possibleEvents.extend(canDisembarkBus(state))
    #Find all buses that can arrive in some stop
    possibleEvents.extend(canComeToStop(state))
    #Find all buses that can leave some stop
    possibleEvents.extend(canLeaveStop(state))
    return possibleEvents