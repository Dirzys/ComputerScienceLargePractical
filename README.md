I have written my simulation in Python. Python, because this is my favourite programming language that I am using 
daily.

To run the simulation use: 

	python main.py simpleInput.txt
	
- where the second term specifies input file that will be used for simulation.

This command will output all simulation to command line (together with statistics, optimised parameters,
warnings or errors)

I have written some test for my simulation.

To run these use:

	python unitTest.py
	
It contains all tests I have written. I have added all tests into one file just for simpler test process.

Test contains tests for testing:
- if simple file without experiments is parsed correctly
- if events are calculated correctly separately for boarding and disembarking the bus, arriving and leaving the stop
- if simulation outputs correct events and accurate statistics by using seed
- if file with experiments is parsed correctly and correct states are created
- if file catches errors and warnings (valid/invalid inputs) 

 