import read_file as createNetwork
import update_state as update
import objects
import calculate_events
import math
from random import random, uniform, shuffle

def weighted_choice(events, totalRate):
    #Shuffling events first
    shuffled = []
    indexes = range(len(events))
    shuffle(indexes)
    for i in indexes:
        shuffled.append(events[i])
    #Now randomly selecting from shuffled list
    r = uniform(0, totalRate)
    upto = 0
    for rate, event in shuffled:
        if upto + rate > r:
            return event
        upto += rate

state = createNetwork.readFromFile('input.dat')

time = 0
while time <= float(state.stopTime):
    events = calculate_events.calculate(state)
    totalRate = sum([event[0] for event in events])
    delay = -totalRate/len(events) * math.log(random())
    chooseEvent = weighted_choice(events, totalRate)
    state = update.modify_state(state, chooseEvent, time)
    #time = time + float(state.stopTime)
    time = time + delay
