import read_file as createNetwork
import update_state as update
import objects
import calculate_events
import math
import sys
import analysis
from random import random, uniform, shuffle

def weighted_choice(events, totalRate):
    #Shuffling events first
    shuffled = []
    indexes = range(len(events))
    shuffle(indexes)
    for i in indexes:
        shuffled.append(events[i])
    #Now randomly selecting from shuffled list
    #Found this algorithm in one of the answers in Stack Overflow 
    r = uniform(0, totalRate)
    upto = 0
    for rate, event in shuffled:
        if upto + rate > r:
            return event
        upto += rate
        
def resetAllGlobalParams():
    objects.resetGlobal()
    
def printExperiment(experiment):
    for change in experiment:
        line = change[0]
        for data in change[1:]:
            line += " %s" % data
        print line 
        
def costFunction(missed, experiment):
    totalChange = 0.0
    for change in experiment:
        totalChange += change[len(change)-1]
    return totalChange * missed
        
def simulate(state, listEvents):
    time = 0
    resetAllGlobalParams()
    while time <= float(state.stopTime):
        events = calculate_events.calculate(state)
        totalRate = sum([event[0] for event in events])
        delay = -totalRate/len(events) * math.log(random())
        chooseEvent = weighted_choice(events, totalRate)
        state = update.modify_state(state, chooseEvent, time, listEvents)
        #time = time + float(state.stopTime)
        time = time + delay
    
    analysis.print_stats(state)

#Getting input file name from the user command        
if __name__ == "__main__":
    fileToRead = sys.argv[1]

states = createNetwork.readFromFile(fileToRead)

if len(states) > 1:
    costs = []
    for state, vari in states:
        printExperiment(vari)
        simulate(state, False)
        costs.append((costFunction(state.missedTotal, vari), vari))
        
    #Find experiment that has minimum cost
    optimised =  min(costs, key=lambda item:item[0])[1]
    print "Optimised parameters:"
    printExperiment(optimised)
else:
    if not states[0][0].optimise:
        simulate(states[0][0], True)
    else:
        print "Error: Cannot optimise parameters when there are no experiment present"
