import objects as new
from collections import deque

def calculate(state):
    #Find all possible events with their rates
    possibleEvents = {}
    #New passenger can always arrive into the random stop with rate paxArrivalRate
    possibleEvents[state.paxArrives] = ['newpax']
    return possibleEvents