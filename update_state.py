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
                stop.add_passengers(new.Passenger(destinationId, 'waits', buses))
        #Output result
        print 'A new passenger enters at stop ' + originId + ' with destination ' + destinationId +' at time ' + str(time)
    
    type = event[0]
    if type == 'newpax':
        addNewPax()
    elif type == 'boards':
        pass
    elif type == 'disembarks':
        pass
    elif type == 'comes':
        pass
    elif type == 'departs':
        pass
    else:
        raise Exception, ': incorrect event type'
    return state