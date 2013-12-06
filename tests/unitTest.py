import unittest
import parse_file as createNetwork
import calculate_events
import objects as new
from collections import deque
from copy import deepcopy

class ReadFileTest(unittest.TestCase):

    def runTest(self):
        """ Test if file is read and network created successfully  """
        
        results = createNetwork.readFromFile('test_input.dat')[0][0]

        self.failUnless(len(results.routes)==1, 'One route must be added, found: ' + str(len(results.routes)))
        self.failUnless(len(results.roads)==3, 'Three roads must be added, found: ' + str(len(results.roads)))
        self.failUnless(len(results.buses)==4, 'Four buses must be added, found: ' + str(len(results.buses)))
        self.failUnless(len(results.stops)==3, 'Three stops must be added, found: ' + str(len(results.stops)))
        self.failUnless(results.boards==1.0, 'Boarding rate should be 1.0, found: ' + str(results.boards))
        self.failUnless(results.disembarks==3.0, 'Disembark rate should be 3.0, found: ' + str(results.disembarks))
        self.failUnless(results.busDeparts==3.0, 'Buses departing rate should be 3.0, found: ' + str(results.busDeparts))
        self.failUnless(results.paxArrives==8.0, 'New passengers arrival rate should be 8.0, found: ' + str(results.paxArrives))
        self.failUnless(results.stopTime==100.0, 'Stop time should be 100.0, found: ' + str(results.stopTime))
        self.failUnless(results.ignore==True, 'Ignore warnings should be true, found: ' + str(results.ignore))
        self.failUnless(results.optimise==True, 'Optimisation should be true, found: ' + str(results.optimise))
        
        self.failUnless(len(results.routes[0].stops)==3, '3 stops must be added to route 1, found: ' + str(len(results.routes[0].stops)))
        
class CalculateEventsTest(unittest.TestCase):

    def runTest(self):
        """ Test if calculate_events returns results in the required form """
        
        network = createNetwork.readFromFile('test_input.dat')[0][0]
        results = calculate_events.get_possible_events(network)
        
        for event in results:
            self.failUnless(isinstance(event, tuple), 'Possible events must be returned as tuples, but found: ' + str(type(event)) + ' for event ' + str(event))

class TestCanBoardBus(unittest.TestCase):

    def runTest(self):
        """ Test canBoardBus function if it returns correct results """
        
        paxs = [new.Passenger('2', ['1', '2'], 0.1), new.Passenger('3', ['2', '3'], 0.1)]
        bus1 = new.Bus('2.0', '', [], 10)
        bus2 = new.Bus('1.1', '', [], 10)
        stop = new.Stop('1', deque([bus1, bus2]), paxs)
        paxs2 = [new.Passenger('3', ['1', '2'], 0.1), new.Passenger('1', ['2', '3'], 0.1)]
        bus1b = new.Bus('1.2', '', [], 10)
        bus2b = new.Bus('2.3', '', [], 10)
        stop2 = new.Stop('2', deque([bus1b, bus2b]), paxs2)
        
        state = new.State([], [], [], [stop, stop2], 1.0, 0, 0, 0, 0, False, False)
        
        results = calculate_events.canBoardBus(state)
        
        for event in results:
            self.failUnless(event[1][3].top_bus().id.split('.')[0] in event[1][1].bus, 'Bus passenger is looking for is not at the top of the queue: ' + str(event[1][3].top_bus().id))

class TestCanDisembarkBus(unittest.TestCase):

    def runTest(self):
        """ Test canDisembarkBus function if it returns correct results """
        
        paxs = [new.Passenger('2', '2.0', 0.1), new.Passenger('3', '2.0', 0.1)]
        paxs2 = [new.Passenger('3', '1.1', 0.1), new.Passenger('2', '1.1', 0.1)]
        bus1 = new.Bus('2.0', '', paxs, 10)
        bus2 = new.Bus('1.1', '', paxs2, 10)
        stop = new.Stop('2', deque([bus1, bus2]), [])
        
        state = new.State([], [], [], [stop], 0, 1.0, 0, 0, 0, False, False)
        
        results = calculate_events.canDisembarkBus(state)
        
        for event in results:
            self.failUnless(event[1][1] in event[1][2].passengers, 'Passenger ' + str(event[1][1]) + ' is not in the bus ' + str(event[1][2].id) +', hence wrong event: ')
            self.failUnless(event[1][1].destination == event[1][3].id, 'Passenger ' + str(event[1][1]) + ' want to disembark at the stop ' + str(event[1][1].destination) + ', not stop ' + str(event[1][3].id))

class TestCanComeToStop(unittest.TestCase):

    def runTest(self):
        """ Test canComeToStop function, if it returns correct results """
        
        road1 = new.Road('1', '2', 1.0)
        stop = new.Stop('2', deque([]), 2.0)
        bus1 = new.Bus('2.0', road1, [], 10)
        bus2 = new.Bus('1.1', stop, [], 10)
        
        state = new.State([], [], [bus1, bus2], [], 0, 0, 0, 0, 0, False, False)
        
        results = calculate_events.canComeToStop(state)
        
        for event in results:
            self.failUnless(isinstance(event[1][1].state, new.Road), 'Returned bus ' + str(event[1][1]) + ' is not on any road')
           
class TestCanLeaveStop(unittest.TestCase):

    def runTest(self):
        """ Test canLeaveStop function, if it returns correct results """
        
        paxs = [new.Passenger('3', '2.0', 0.1), new.Passenger('3', '2.0', 0.1)]
        paxs2 = [new.Passenger('3', '1.1', 0.1), new.Passenger('2', '1.1', 0.1)]
        bus1 = new.Bus('2.0', '2', paxs, 2)
        bus2 = new.Bus('1.1', '2', paxs2, 10)
        stop = new.Stop('2', deque([bus1, bus2]), [new.Passenger('5', ['2'], 0.1)])
        
        state = new.State([], [], [bus1, bus2], [stop], 0, 0, 1.0, 0, 0, False, False)
        
        results = calculate_events.canLeaveStop(state)
        
        for event in results:
            self.failUnless(event[1][1].capacity == len(event[1][1].passengers), 'Bus ' + event[1][1].id + ' is not on capacity and should not leave the stop')
          
class TestCreateExperimentsState(unittest.TestCase):

    def runTest(self):
        """ Test if addStateForExperiment works correctly """
        
        # Since we are creating new states for experiments from the first one 
        # the test is going to create the first state from all the others by applying
        # first experiment changes and then check if it produces the same state
                
        results = createNetwork.readFromFile('testExperiments.dat')
        
        firstState, firstExperiment = results[0]
        for state, _ in results[1:]:
            state = createNetwork.addStateForExperiment(firstExperiment, state)
            
            #Buses
            buses = {}
            for route in state.routes:
                buses[route.number] = 0
            buses2 = deepcopy(buses)
            for bus in state.buses:
                buses[bus.id.split('.')[0]] += 1
            for bus in firstState.buses:
                buses2[bus.id.split('.')[0]] += 1
                
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
                               
           
def suite():
    suite = unittest.TestSuite()
    suite.addTest(ReadFileTest())
    suite.addTest(CalculateEventsTest())
    suite.addTest(TestCanBoardBus())
    suite.addTest(TestCanDisembarkBus())
    suite.addTest(TestCanComeToStop())
    suite.addTest(TestCanLeaveStop())
    suite.addTest(TestCreateExperimentsState())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testSuite = suite()
    runner.run(testSuite)