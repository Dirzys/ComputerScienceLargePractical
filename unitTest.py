import unittest
from copy import deepcopy
from collections import deque
from random import seed
from calculate_events import *
from objects import Bus, Passenger, Stop, State
from parse_file import readFromFile, addStateForExperiment, createStatesFromExperiments
from simulate import simulate, findProblems
from simulationTestEvents import testEvents, testStats

class ReadFileTest(unittest.TestCase):

    def runTest(self):
        """ Test if file is read and network created successfully  """
        
        results, _ = readFromFile('inputs/testSimpleInput.dat')

        self.failUnless(len(results.routes)==1, 'One route must be added, found: %s' % len(results.routes))
        self.failUnless(len(results.roads)==3, 'Three roads must be added, found: %s' % len(results.roads))
        self.failUnless(len(results.buses)==4, 'Four buses must be added, found: %s' % len(results.buses))
        self.failUnless(len(results.stops)==3, 'Three stops must be added, found: %s' % len(results.stops))
        self.failUnless(results.boards==1.0, 'Boarding rate should be 1.0, found: %s' % results.boards)
        self.failUnless(results.disembarks==3.0, 'Disembark rate should be 3.0, found: %s' % results.disembarks)
        self.failUnless(results.busDeparts==3.0, 'Buses departing rate should be 3.0, found: %s' % results.busDeparts)
        self.failUnless(results.paxArrives==8.0, 'New passengers arrival rate should be 8.0, found: %s' % results.paxArrives)
        self.failUnless(results.stopTime==100.0, 'Stop time should be 100.0, found: %s' % results.stopTime)
        self.failUnless(results.ignore==True, 'Ignore warnings should be true, found: %s' % results.ignore)
        self.failUnless(results.optimise==True, 'Optimisation should be true, found: %s' % results.optimise)
        
        self.failUnless(len(results.routes[0].stops)==3, '3 stops must be added to route 1, found: %s' % len(results.routes[0].stops))
        
class CalculateEventsTest(unittest.TestCase):

    def runTest(self):
        """ Test if calculate_events returns results in the required form """
        
        network, _ = readFromFile('inputs/testSimpleInput.dat')
        results = get_possible_events(network)
        
        for event in results:
            self.failUnless(isinstance(event, tuple), 'Possible events must be returned as tuples, but found: %(type)s for event %(event)s' % \
                                                        {'type': type(event), 'event': event})

class TestCanBoardBus(unittest.TestCase):

    def runTest(self):
        """ Test canBoardBus function if it returns correct results """
        
        paxs = [Passenger('2', ['1', '2'], 0.1), Passenger('3', ['2', '3'], 0.1)]
        bus1 = Bus('2.0', '2', '', [], 10)
        bus2 = Bus('1.1', '1', '', [], 10)
        stop = Stop('1', deque([bus1, bus2]), paxs)
        paxs2 = [Passenger('3', ['1', '2'], 0.1), Passenger('1', ['2', '3'], 0.1)]
        bus1b = Bus('1.2', '1', '', [], 10)
        bus2b = Bus('2.3', '2', '', [], 10)
        stop2 = Stop('2', deque([bus1b, bus2b]), paxs2)
        
        state = State([], [], [], [stop, stop2], 1.0, 0, 0, 0, 0, False, False)
        
        results = canBoardBus(state)
    
        for event in results:
            self.failUnless(event[1][3].top_bus().routeNr in event[1][1].bus, 'Bus the passenger is looking for is not at the top of the queue: %s' % event[1][3].top_bus().id)

class TestCanDisembarkBus(unittest.TestCase):

    def runTest(self):
        """ Test canDisembarkBus function if it returns correct results """
        
        paxs = [Passenger('2', '2.0', 0.1), Passenger('3', '2.0', 0.1)]
        paxs2 = [Passenger('3', '1.1', 0.1), Passenger('2', '1.1', 0.1)]
        bus1 = Bus('2.0', '2', '', paxs, 10)
        bus2 = Bus('1.1', '1', '', paxs2, 10)
        stop = Stop('2', deque([bus1, bus2]), [])
        
        state = State([], [], [], [stop], 0, 1.0, 0, 0, 0, False, False)
        
        results = canDisembarkBus(state)
        
        for event in results:
            self.failUnless(event[1][1] in event[1][2].passengers, 'Passenger %(pax)s is not in the bus %(bus)s, hence he cannot disembark this bus' % \
                                                                        {'pax': event[1][1].__dict__, 'bus': event[1][2].id})
            self.failUnless(event[1][1].destination == event[1][3].id, 'Passenger %(pax)s wants to disembark at the stop %(stop)s, not stop %(stop2)s' % \
                                                                        {'pax': event[1][1].__dict__, 'stop': event[1][1].destination, 'stop2': event[1][3].id})

class TestCanComeToStop(unittest.TestCase):

    def runTest(self):
        """ Test canComeToStop function, if it returns correct results """
        
        road1 = Road('1', '2', 1.0)
        stop = Stop('2', deque([]), 2.0)
        bus1 = Bus('2.0', '2', road1, [], 10)
        bus2 = Bus('1.1', '1', stop, [], 10)
        
        state = State([], [], [bus1, bus2], [], 0, 0, 0, 0, 0, False, False)
        
        results = canComeToStop(state)
        
        for event in results:
            self.failUnless(isinstance(event[1][1].state, Road), 'Returned bus %s is not on any road' % event[1][1].__dict__)
           
class TestCanLeaveStop(unittest.TestCase):

    def runTest(self):
        """ Test canLeaveStop function, if it returns correct results """
        
        paxs = [Passenger('3', '2.0', 0.1), Passenger('3', '2.0', 0.1)]
        paxs2 = [Passenger('3', '1.1', 0.1), Passenger('2', '1.1', 0.1)]
        bus1 = Bus('2.0', '2', '2', paxs, 2)
        bus2 = Bus('1.1', '1', '2', paxs2, 10)
        stop = Stop('2', deque([bus1, bus2]), [Passenger('5', ['2'], 0.1)])
        
        state = State([], [], [bus1, bus2], [stop], 0, 0, 1.0, 0, 0, False, False)
        
        results = canLeaveStop(state)
        
        for event in results:
            self.failUnless(event[1][1].capacity == len(event[1][1].passengers), 'Bus %s is not on capacity and should not leave the stop' % event[1][1].id)
       
class TestSimulationOutput(unittest.TestCase):

    def runTest(self):
        """ Test if simulation algorithm works correctly """
               
        results, _ = readFromFile('inputs/testSimulation.dat')
        
        seed(1)
        events, stats = simulate(results, False, True)
        
        for i, event in enumerate(events):
            self.failUnless(event == testEvents[i], 'Simulation do not match: %s' % event)
        
        for i, stat in enumerate(stats):
            self.failUnless(stat == testStats[i], 'Statistics do not match: %s' % stat)
          
class TestCreateExperimentsState(unittest.TestCase):

    def runTest(self):
        """ Test if addStateForExperiment works correctly """
        
        # Since we are creating new states for experiments from the first one 
        # the test is going to create the first state from all the others by applying
        # first experiment changes and then check if it produces the same state
                
        state, experiments = readFromFile('inputs/testExperiments.dat')
        results = createStatesFromExperiments(state, experiments)
        
        firstState, firstExperiment = results[0]
        for state, _ in results[1:]:
            state = addStateForExperiment(firstExperiment, state)
            
            #Buses
            buses = {}
            for route in state.routes:
                buses[route.number] = 0
            buses2 = deepcopy(buses)
            for bus in state.buses:
                buses[bus.routeNr] += 1
            for bus in firstState.buses:
                buses2[bus.routeNr] += 1
                
            self.failUnless(buses == buses2, 'The number of buses in states are not the same: %(one)s and  %(two)s' % {'one':buses, 'two':buses2})
                
            
            #Capacity
            for bus in state.buses:
                for bus2 in firstState.buses:
                    if bus.id == bus2.id:
                        self.failUnless(bus.capacity == bus2.capacity, 'Bus capacities are not the same for buses: %(one)s and  %(two)s' % {'one':bus.__dict__, 'two':bus2.__dict__})
                
                  
            #Roads
            for road in state.roads:
                for road2 in firstState.roads:
                    if road.starts == road2.starts and road.ends == road2.ends:
                        self.failUnless(road.__eq__(road2), 'Roads from %(starts)s to %(ends)s are not the same' % {'starts':road.starts, 'ends':road.ends})
              
            #Boards rate
            self.failUnless(firstState.boards == state.boards, 'Board rates are not the same for states: %(one)s and  %(two)s' % {'one':state.__dict__, 'two':state.__dict__})
                
            #Disembarks rate
            self.failUnless(firstState.disembarks == state.disembarks, 'Disembarks rates are not the same for states: %(one)s and  %(two)s' % {'one':state.__dict__, 'two':state.__dict__})
            
            #Depart rate
            self.failUnless(firstState.busDeparts == state.busDeparts, 'Bus depart rates are not the same for states: %(one)s and  %(two)s' % {'one':state.__dict__, 'two':state.__dict__})
                     
            #New passengers rate
            self.failUnless(firstState.paxArrives == state.paxArrives, 'New passenger rates are not the same for states: %(one)s and  %(two)s' % {'one':state.__dict__, 'two':state.__dict__})

class TestWarningsAndErrors(unittest.TestCase):

    def runTest(self):
        """ Test if program finds warnings and errors correctly """
        
        testProblems = ['Error! Road between stops 2 and 2 is required, but not present in the input', 'Error! Road between stops 5 and 2 is required, but not present in the input', 'Error! Road between stops 3 and 6 is required, but not present in the input', 'Error! Road between stops 6 and 1 is required, but not present in the input', 'Error! Route 2 has only one stop', 'Error! Route 1 is specified more than once', 'Error! Route 3 is specified more than once', 'Error! Road between stops 1 and 2 is specified more than once', 'Warning! Road between stops 3 and 4 will not be used since no route operates through this road', 'Warning! Road between stops 4 and 2 will not be used since no route operates through this road', 'Warning! Road between stops 5 and 9 will not be used since no route operates through this road', 'Warning! Route 4 has 0 capacity']
         
        results, experiments = readFromFile('inputs/testProblems.dat')
        _, problems = findProblems(results, experiments)
        
        for i, problem in enumerate(problems):
            self.failUnless(problem == testProblems[i], 'Problems do not match: %s' % problem)
       
def suite():
    suite = unittest.TestSuite()
    suite.addTest(ReadFileTest())
    suite.addTest(CalculateEventsTest())
    suite.addTest(TestCanBoardBus())
    suite.addTest(TestCanDisembarkBus())
    suite.addTest(TestCanComeToStop())
    suite.addTest(TestCanLeaveStop())
    suite.addTest(TestSimulationOutput())
    suite.addTest(TestCreateExperimentsState())
    suite.addTest(TestWarningsAndErrors())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testSuite = suite()
    runner.run(testSuite)