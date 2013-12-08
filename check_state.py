
def requiredRoads(state):
    ''' Find all roads that are required for simulation to run '''
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

def necessaryRoads(state):
    errors = []
    required = requiredRoads(state)
    for road in required:
        if road not in [[roadInState.starts, roadInState.ends] for roadInState in state.roads]:
            errors.append('Error! Road between stops %(one)s and %(two)s is required, but not present in the input' % \
                            {'one': road[0], 'two': road[1]})
    return errors

def findWarnings(state):
    warnings = []
    warnings.extend(unnecessaryRoads(state))
    
    return warnings

def findErrors(state):
    errors = []
    errors.extend(necessaryRoads(state))
    return errors