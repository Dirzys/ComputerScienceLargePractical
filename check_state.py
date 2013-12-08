
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

def routesWithOneStop(state):
    warnings = []
    for route in state.routes:
        if len(route.stops) == 1:
            warnings.append('Warning! Route %s has only one stop' % route.number)
    return warnings

def sameRoutesWithDifferentInfo(state):
    errors = []
    for i in range(0, len(state.routes)):
        for j in range(i+1, len(state.routes)):
            isEqual = state.routes[i].__eq__(state.routes[j])
            if state.routes[i].number == state.routes[j].number and not isEqual:
                errors.append('Error! Route %s is repeated with different information' % state.routes[i].number)
    return errors

def sameRoadsWithDifferentRate(state):
    errors = []
    for i in range(0, len(state.roads)):
        for j in range(i+1, len(state.roads)):
            isEqual = state.roads[i].__eq__(state.roads[j])
            if state.roads[i].starts == state.roads[j].starts and state.roads[i].ends == state.roads[j].ends and not isEqual:
                errors.append('Error! Road between stops %(one)s and %(two)s is repeated with different information' % \
                            {'one': state.roads[i].starts, 'two': state.roads[i].ends})
    return errors

def findWarnings(state):
    warnings = []
    warnings.extend(unnecessaryRoads(state))
    warnings.extend(routesWithOneStop(state))
    return warnings

def findErrors(state):
    errors = []
    errors.extend(necessaryRoads(state))
    errors.extend(sameRoutesWithDifferentInfo(state))
    errors.extend(sameRoadsWithDifferentRate(state))
    return errors