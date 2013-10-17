import objects as new
from collections import deque

def canBoardBus(state):
    return []

def calculate(state):
    #Find all possible events with their rates
    possibleEvents = {}
    #New passenger can always arrive into the random stop with rate paxArrivalRate
    possibleEvents[state.paxArrives] = ['newpax']
    #Find all passengers who can board some bus and add them to possible events list
    boardingEvents = canBoardBus(state)
    return possibleEvents