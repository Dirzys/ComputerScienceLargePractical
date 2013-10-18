import unittest
import read_file as createNetwork
import calculate_events

class ReadFileTest(unittest.TestCase):

    def runTest(self):
        """ Test if file is read and network created successfully  """
        
        results = createNetwork.readFromFile('test_input.dat')

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
        
        network = createNetwork.readFromFile('test_input.dat')
        results = calculate_events.calculate(network)
        
        for event in results:
            self.failUnless(isinstance(event, tuple), 'Possible events must be returned as tuples, but found: ' + str(type(event)) + ' for event ' + str(event))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ReadFileTest())
    suite.addTest(CalculateEventsTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testSuite = suite()
    runner.run(testSuite)