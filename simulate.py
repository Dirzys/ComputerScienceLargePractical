from parse_file import readFromFile
from update_state import modify_state
from calculate_events import get_possible_events
from check_state import *
import math
from analysis import print_stats
from random import random, uniform

def weightedChoice(events, totalRate):
    ''' Randomly selecting from events list.
        Found this algorithm in one of the answers in Stack Overflow ''' 
    r = uniform(0, totalRate)
    upto = 0
    for rate, event in events:
        if upto + rate > r:
            return event
        upto += rate
    
def printExperiment(experiment):
    for change in experiment:
        line = change[0]
        for data in change[1:]:
            line += " %s" % data
        print line 
        
def costFunction(missed, experiment):
    ''' Calculated by multiplying the number of missed passengers
        with the sum of each value of experiments'''
    totalChange = 0.0
    for change in experiment:
        totalChange += change[len(change)-1]
    return totalChange * missed
        
def simulate(state, listEvents, keepEvents):
    ''' The main simulation algorithm. Print statistics at the end'''
    eventsDone = []
    time = 0
    while time <= float(state.stopTime):
        events = get_possible_events(state)
        totalRate = sum([event[0] for event in events])
        delay = -totalRate/len(events) * math.log(random())
        chooseEvent = weightedChoice(events, totalRate)
        state, eventDone = modify_state(state, chooseEvent, time, listEvents)
        if keepEvents:
            eventsDone.append(eventDone)
        time = time + delay
    
    print_stats(state)
    
def simulateAll(states):
    '''Simulate only once if no experiment present, otherwise simulate every possible state '''
    if len(states) > 1:
        costs = []
        for state, vari in states:
            printExperiment(vari)
            simulate(state, False, False)
            costs.append((costFunction(state.missedTotal, vari), vari))
        
        #Find experiment that has minimum cost
        if states[0][0].optimise:
            optimised =  min(costs, key=lambda item:item[0])[1]
            print "Optimised parameters:"
            printExperiment(optimised)
    else:
        if not states[0][0].optimise:
            simulate(states[0][0], True, False)
        else:
            print "Error: Cannot optimise parameters when there are no experiment present"

def printProblems(problems):
    for problem in problems:
        print problem
        
def findProblems(states):
    ''' Find errors and warnings (if not ignore warnings) in the input and print it if found some'''
    foundProblems = False
    for state, _ in states:
        warnings = errors = []
        if not state.ignore:
            warnings = findWarnings(state)
        errors = findErrors(state)
        if not warnings == errors == []:
            printProblems(errors + warnings)
            foundProblems = True
            break
    return foundProblems

def run(fileToRead):
    states = readFromFile(fileToRead)

    problems = True
    if states:
        problems = findProblems(states)

    if not problems:
        simulateAll(states)