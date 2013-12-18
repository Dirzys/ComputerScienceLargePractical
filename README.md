---GENERAL INFO---
I have written my simulation in Python. Python, because this is my favourite programming language that I am using 
daily.

---HOW TO RUN SIMULATION---
To run the simulation use: 

	python main.py simpleInput.txt
	
- where the second term specifies input file that will be used for simulation.

This command will output all simulation to command line (together with statistics, optimised parameters,
warnings or errors)

---HOW TO RUN TESTS---
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

---ADDITIONAL VALIDATION---
Warning shown:
- if route with zero capacity found

Since simulation can still be run, considering routes with empty capacity as a valid input, however, since it is 
quite strange to have such a "route" showing a warning to user.

Error shown:
- if route with only one stop found

Firstly, I was thinking that this should be a warning, however, after thinking about it more carefully I have decided
to consider routes with only one stop as invalid since in case no other routes operates through this stop, if new
passenger comes to this stop, he will not be able to go everywhere (destination stop cannot be the same as origin
stop and no other options are available, because no other routes operates through this stop)

- if route with same number found more than once
- if more than one road with identical starting and ending stops found

I was thinking about showing warning if two identical routes/roads have been found. However, I have decided to
consider this as an error since the original simulation would have two identical routes/roads that might be mixed 
up by the simulation (unless, of course, we are removing these identical instances from our state)

 