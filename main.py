import read_file as createNetwork
import objects
import calculate_events
import math
from random import random
import operator

initialState = createNetwork.readFromFile('input.dat')

time = 0
while time <= float(initialState[9]):
    rates = calculate_events.calculate(initialState)
    events = {'a': 0.1}
    totalRate = sum([events[event] for event in events])
    delay = -totalRate/len(events) * math.log(random())
    chooseEvent = max(events.iteritems(), key = operator.itemgetter(1))[0]
    #modify_state(chooseEvent)
    time = time + float(initialState[9]) + 1
    #time = time + delay

print initialState