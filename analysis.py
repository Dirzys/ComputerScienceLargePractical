
def print_stats(state):
    
    for stop in state.missedPaxOnStop:
        print "number of missed passengers stop %(stop)s %(miss)s" % \
                {'stop': stop, 'miss': state.missedPaxOnStop[stop]}
    for route in state.missedPaxOnRoute:
        print "number of missed passengers route %(route)s %(miss)s" % \
                {'route': route, 'miss': state.missedPaxOnRoute[route]}
    print "number of missed passengers %s" % state.missedTotal
    
    for bus in state.buses:
        numPax = bus.numOfPaxIn[bus.id]
        numJourn = float(bus.journeysMade[bus.id])
        print "average passengers bus %(bus)s %(mean)0.3f" % \
                {'bus': bus.id, 'mean': (numPax/numJourn) if numJourn != 0 else 0}
     
    overall = {'numJourn' : 0,
               'numPax'   : 0
               }       
        
    for route in state.routes:
        numPax = route.numOfPaxIn[route.number]
        numJourn = float(route.journeysMade[route.number])
        print "average passengers route %(route)s %(mean)0.3f" % \
                {'route': route.number, 'mean': (numPax/numJourn) if numJourn != 0 else 0}
        overall['numJourn'] += numJourn
        overall['numPax'] += numPax
        
    print "average passengers %0.3f" % (overall['numPax']/overall['numJourn']) if overall['numJourn'] != 0 else 0  
               
    #Average Bus Queuing Time
    overall = {'timeOfWaiting' : 0.0,
               'busesWaited'   : 0
               }  
    
    for stop in state.stops: 
        timeOfWaiting = stop.timeOfWaiting[stop.id]
        busesWaited = stop.busesWaited[stop.id]
        
        #Also considering buses that were waiting at the queue, but have not left the stop 
        #or arrived into top of the queue by the end of simulation
        busesArrived = stop.busArrivedOn
        for busInQueue in stop.busQueue:
            if busInQueue.id in busesArrived:
                timeOfWaiting += state.stopTime - busesArrived[busInQueue.id]
                busesWaited += 1
                
        print "average queuing at stop %(stop)s %(time)0.3f" % \
                {'stop': stop.id, 'time': (timeOfWaiting/busesWaited) if busesWaited != 0 else 0}
        overall['timeOfWaiting'] += timeOfWaiting
        overall['busesWaited'] += busesWaited
        
    print "average queuing at all stops %0.3f" % (overall['timeOfWaiting']/overall['busesWaited']) if overall['busesWaited'] != 0 else 0