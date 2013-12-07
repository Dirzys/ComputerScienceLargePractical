
def requiredRoads(state):
    roads = []
    for route in state.routes:
        for i in range(0, len(route.stops)):
            road = [route.stops[i], route.stops[(i+1) % len(route.stops)]]
            if not road in roads:
                roads.append(road)
    return roads

def unnecessaryRoads(state):
    warnings = []
    required = requiredRoads(state)
    for road in state.roads:
        if [road.starts, road.ends] not in required:
            warnings.append('Warning! Road between stops %(one)s and %(two)s will not be used since no route operates through this road' % \
                            {'one': road.starts, 'two': road.ends})
    return warnings

def findWarnings(state):
    warnings = []
    warnings.extend(unnecessaryRoads(state))
    
    return warnings

def findErrors(state):
    errors = []
    return errors