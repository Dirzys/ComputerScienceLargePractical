import read_file as createNetwork
import update_state as update
import objects
import calculate_events
import math
from random import random

state = createNetwork.readFromFile('input.dat')

time = 0
while time <= float(state.stopTime):
    events = calculate_events.calculate(state)
    print events
    totalRate = sum([event[0] for event in events])
    delay = -totalRate/len(events) * math.log(random())
    maxRate = max([event[0] for event in events])
    for event in events: 
        if event[0] == maxRate: 
            chooseEvent = event[1]
            break 
    state = update.modify_state(state, chooseEvent, time)
    time = time + float(state.stopTime) + 1
    #time = time + delay
