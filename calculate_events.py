import objects as new
from collections import deque

def canBoardBus(state):
    boardingRate = state.boards
    events = []
    for stop in state.stops:
        for pax in stop.passengers:
            if stop.top_bus().id.split('.')[0] in pax.bus:
                events.append((boardingRate, ['boards', pax, stop]))
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

def calculate(state):
    #Find all possible events with their rates
    possibleEvents = []
    #New passenger can always arrive into the random stop with rate paxArrivalRate
    possibleEvents.append((state.paxArrives, ['newpax']))
    #Find all passengers who can board some bus and add them to possible events list
    possibleEvents.extend(canBoardBus(state))
    #Find all passengers who can disembark some bus and add these events to possible events list
    possibleEvents.extend(canDisembarkBus(state))
    return possibleEvents