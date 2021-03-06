
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
    ''' Find all roads that are specified, but will never be used in the simulation, 
        because there is no route that operates through this road and create a warning for each '''
    warnings = []
    required = requiredRoads(state)
    for road in state.roads:
        if [road.starts, road.ends] not in required:
            warnings.append('Warning! Road between stops %(one)s and %(two)s will not be used since no route operates through this road' % \
                            {'one': road.starts, 'two': road.ends})
    return warnings

def necessaryRoads(state):
    ''' Find all roads that are not specified in the input file, but are required 
        by some route and create an error for each '''
    errors = []
    required = requiredRoads(state)
    for road in required:
        if road not in [[roadInState.starts, roadInState.ends] for roadInState in state.roads]:
            errors.append('Error! Road between stops %(one)s and %(two)s is required, but not present in the input' % \
                            {'one': road[0], 'two': road[1]})
    return errors

def routesWithZeroCapacity(state):
    ''' Find all routes that has zero capacity and create a warning for each '''
    warnings = []
    for route in state.routes:
        if route.capacity == 0:
            warnings.append('Warning! Route %s has 0 capacity' % route.number)
    return warnings

def routesWithOneStop(state):
    ''' Find all routes that has only one stop and create an error for each '''
    errors = []
    for route in state.routes:
        if len(route.stops) == 1:
            errors.append('Error! Route %s has only one stop' % route.number)
    return errors

def routesWithSameNumber(state):
    ''' Find all routes that are specified more than once and create an error
        for each '''
    errors = []
    for i in range(0, len(state.routes)):
        for j in range(i+1, len(state.routes)):
            if state.routes[i].number == state.routes[j].number:
                errors.append('Error! Route %s is specified more than once' % state.routes[i].number)
    return errors

def roadsWithSameStartAndEnd(state):
    ''' Find all roads that are specified more than once and create an error for each '''
    errors = []
    for i in range(0, len(state.roads)):
        for j in range(i+1, len(state.roads)):
            if state.roads[i].starts == state.roads[j].starts and state.roads[i].ends == state.roads[j].ends:
                errors.append('Error! Road between stops %(one)s and %(two)s is specified more than once' % \
                            {'one': state.roads[i].starts, 'two': state.roads[i].ends})
    return errors

def deleteDuplicates(all):
    ''' Delete duplicate problems since some of them might occur more 
        than once (if for example three routes with same route number are specified) '''
    seen = set()
    seen_add = seen.add
    return [ x for x in all if x not in seen and not seen_add(x)]

def findWarnings(state, experiments):
    warnings = []
    warnings.extend(unnecessaryRoads(state))
    warnings.extend(routesWithZeroCapacity(state))
    return deleteDuplicates(warnings)

def findErrors(state, experiments):
    errors = []
    errors.extend(necessaryRoads(state))
    errors.extend(routesWithOneStop(state))
    errors.extend(routesWithSameNumber(state))
    errors.extend(roadsWithSameStartAndEnd(state))
    return deleteDuplicates(errors)