------Code structure------
	After the script is run with correct input file name, the file is parsed line by line by my_parser.py function. The script parses line by line and is tolerant in terms of argument order, but requires that area arguemts come in consecitive lines.
	It prints some warnings for invalid input for example if bin volume is bigger or almost as big as lorry volume
----------
	createObjects.py creates objects for all areas, and the bins and lorries in them
----------
	The events are stored in a Priority queue, where the time for each event is its priority. Only the first events of each type are scheduled, and then each event will create its successor.
----------
	For the moment only bag disposal events are fully implemented and running
--------- 
	Experimentation is in alpha mode - it is detected as valid unput, but the experimentation values are ignored for the moment
--------
	The values inside a road layout matrix are not extensively checked for correctness at the moment, provided they are integers.

--------Testing--------
	Testing has been done using various valid, invalid and valid, but unlikely input configurations. I have sumbmited some of the test files I have used