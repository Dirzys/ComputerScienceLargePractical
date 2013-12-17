
def print_stats(state, keepStats):
    
    stats = []
    def printKeepStats(stat):
        if keepStats:
            stats.append(stat)
        else:
            print stat
    
    #Number of missed passengers
    for stop in state.missedPaxOnStop:
        printKeepStats("number of missed passengers stop %(stop)s %(miss)s" % \
                      {'stop': stop, 'miss': state.missedPaxOnStop[stop]})
    for route in state.missedPaxOnRoute:
        printKeepStats("number of missed passengers route %(route)s %(miss)s" % \
                       {'route': route, 'miss': state.missedPaxOnRoute[route]})
    printKeepStats("number of missed passengers %s" % state.missedTotal)
    
    #Average Passengers Per Bus Per Road
    for bus in state.buses:
        numPax = bus.numOfPaxIn
        numJourn = float(bus.journeysMade)
        printKeepStats("average passengers bus %(bus)s %(mean)0.4f" % \
                       {'bus': bus.id, 'mean': (numPax/numJourn) if numJourn != 0 else 0})
     
    overall = {'numJourn' : 0,
               'numPax'   : 0
               }       
        
    for route in state.routes:
        numPax = route.numOfPaxIn
        numJourn = float(route.journeysMade)
        printKeepStats("average passengers route %(route)s %(mean)0.4f" % \
                       {'route': route.number, 'mean': (numPax/numJourn) if numJourn != 0 else 0})
        overall['numJourn'] += numJourn
        overall['numPax'] += numPax
        
    printKeepStats("average passengers %0.4f" % (overall['numPax']/overall['numJourn']) if overall['numJourn'] != 0 else 0)  
               
    #Average Bus Queuing Time
    overall = {'timeOfWaiting' : 0.0,
               'busesWaited'   : 0
               }  
    
    for stop in state.stops: 
        timeOfWaiting = stop.timeOfWaiting
        busesWaited = float(stop.busesWaited)
        
        #Also considering buses that were waiting at the queue, but have not left the stop 
        #or arrived into top of the queue by the end of simulation
        busesArrived = stop.busArrivedOn
        for busInQueue in stop.busQueue:
            if busInQueue.id in busesArrived:
                timeOfWaiting += state.stopTime - busesArrived[busInQueue.id]
                busesWaited += 1
                
        printKeepStats("average queuing at stop %(stop)s %(time)0.4f" % \
                       {'stop': stop.id, 'time': (timeOfWaiting/busesWaited) if busesWaited != 0 else 0})
        overall['timeOfWaiting'] += timeOfWaiting
        overall['busesWaited'] += busesWaited
        
    printKeepStats("average queuing at all stops %0.4f" % (overall['timeOfWaiting']/overall['busesWaited']) if overall['busesWaited'] != 0 else 0)
    
    #Average Waiting Passengers
     
    overall = {'timePaxWaits' : 0.0,
               'paxWaited'   : 0
               }       
        
    for stop in state.stops:
        timePaxWaitsOnStop = stop.timePaxWaitsOnStop
        paxWaited = float(stop.paxWaited)
        #Also considering passengers that were waiting at the stop until the end of simulation
        for pax in stop.passengers:
            timePaxWaitsOnStop += pax.time
            paxWaited += 1.0
        printKeepStats("average waiting passengers at stop %(stop)s %(mean)0.4f" % \
                       {'stop': stop.id, 'mean': (timePaxWaitsOnStop/paxWaited) if paxWaited != 0 else 0})
        overall['timePaxWaits'] += timePaxWaitsOnStop
        overall['paxWaited'] += paxWaited
        
    for route in state.routes:
        timePaxWaitsOnRoute = route.timePaxWaitsOnRoute
        paxWaited = float(route.paxWaited)
        #Also considering passengers that were waiting on the route until the end of simulation
        for bus in state.buses:
            if bus.id.split('.')[0] == route.number:
                for pax in bus.passengers:
                    timePaxWaitsOnRoute += pax.time
                    paxWaited += 1.0
        printKeepStats("average waiting passengers on route %(route)s %(mean)0.4f" % \
                       {'route': route.number, 'mean': (timePaxWaitsOnRoute/paxWaited) if paxWaited != 0 else 0})
        overall['timePaxWaits'] += timePaxWaitsOnRoute
        overall['paxWaited'] += paxWaited
        
    printKeepStats("average waiting passengers %0.4f" % (overall['timePaxWaits']/overall['paxWaited']) if overall['paxWaited'] != 0 else 0)
           
    return stats