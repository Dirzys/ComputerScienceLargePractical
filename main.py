import read_file as createNetwork
import objects
import calculate_events
import math
from random import random

initialState = createNetwork.readFromFile('input.dat')

time = 0
while time <= float(initialState.stopTime):
    events = calculate_events.calculate(initialState)
    print events
    totalRate = sum([event[0] for event in events])
    delay = -totalRate/len(events) * math.log(random())
    maxRate = max([event[0] for event in events])
    for event in events: 
        if event[0] == maxRate: 
            chooseEvent = event[1]
            break 
    #modify_state(chooseEvent)
    time = time + float(initialState.stopTime) + 1
    #time = time + delay

print initialState.stops