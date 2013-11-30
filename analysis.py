
def print_stats(state):
    
    for stop in state.missedPaxOnStop:
        print "number of missed passengers stop %(stop)s %(miss)s" % \
                {'stop': stop, 'miss': state.missedPaxOnStop[stop]}
    for route in state.missedPaxOnRoute:
        print "number of missed passengers route %(route)s %(miss)s" % \
                {'route': route, 'miss': state.missedPaxOnRoute[route]}
    print "number of missed passengers %s" % state.missedTotal
    
    for bus in state.buses:
        numJourn = bus.numOfPaxIn[bus.id]
        numPax = float(bus.journeysMade[bus.id])
        print "average passengers bus %(bus)s %(mean)0.3f" % \
                {'bus': bus.id, 'mean': (numPax/numJourn) if numJourn != 0 else 0}
     
    overall = {'numJourn' : 0,
               'numPax'   : 0
               }       
        
    for route in state.routes:
        numJourn = route.numOfPaxIn[route.number]
        numPax = float(route.journeysMade[route.number])
        print "average passengers route %(route)s %(mean)0.3f" % \
                {'route': route.number, 'mean': (numPax/numJourn) if numJourn != 0 else 0}
        overall['numJourn'] += numJourn
        overall['numPax'] += numPax
        
    print "average passengers %0.3f" % (overall['numPax']/overall['numJourn']) if overall['numJourn'] != 0 else 0  
                