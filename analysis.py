
def print_stats(state):
    
    for stop in state.missedPaxOnStop:
        print "number of missed passengers stop %(stop)s %(miss)s" % \
                {'stop': stop, 'miss': state.missedPaxOnStop[stop]}
    for route in state.missedPaxOnRoute:
        print "number of missed passengers route %(route)s %(miss)s" % \
                {'route': route, 'miss': state.missedPaxOnRoute[route]}
    print "number of missed passengers %s" % state.missedTotal