#!/usr/bin/python
from region import Region
from config import *
from inputbit import InputVector
import 
from nxt.sensor import*    

brick = nxt.locator.find_one_brick()

def testCount():
  rows = 5
	cols = 5
	coverage = 20
	numbits = 10 # I may need more bits for my readngs.
	numRounds = 500
	trainingRounds = numRounds/4
	originalInputVector = InputVector(numbits)
	inputVector = InputVector(0)
	predictions = dict()
 
     # Repeat several times to increase activity:
     # Seems to just extend the number of elements in inputVector by numbits (10) 3 times. 
     # Why not extend it by 3*numbits?
     # I think becuase rather than make it 3 times as long, it actually repeats the vector three times,
     # probably so as to, as said above, increase activity in those cells and aid learning. 
     # Good old repartition. In which case, I'm not sure I want to use this in my tests...
	for i in range(3): 
		inputVector.extendVector(originalInputVector)
     
     # Get a non-local variable and feed it to a local one for local manipulation.
	desiredLocalActivity = DESIRED_LOCAL_ACTIVITY
     
     # This sets up a new region, called newRegion,
     # a variable called ouputVector, which calls a method to find just that,
     # and a variable for the number of correct prodicitons, initialised as 0. 
	newRegion = Region(rows,cols,inputVector,coverage,desiredLocalActivity)
	outputVector = newRegion.getOutputVector()
	correctBitPredictions = 0
 
 
      # This is where the action starts. This loop forms the main body of the test.
      # For every time round, an input is given, the CLA updates spacial and temporal 
      # poolers with this new input and an output is found. 
	for round in range(numRounds): 
           # The old version gave two inputs alternatly. The aim was to get the CLA to 
           # predict one of two numbers. 
		#print("Round: " + str(round))
		# if (round % 2 == 0):
		# 	val = 682
		# else:
		# 	val = 341
		val = Ultrasonic(brick, PORT_1).get_sample() # Instead I'm now feeding in readings from the sonar. 
		setInput(originalInputVector,val) # These next few lines convert the inputs and outputs from integers to bitstrings,
		inputString = inputVector.toString() # so that the CLA can handle them. 
		outputString = outputVector.toString()
		#print(originalInputVector.toString())
           
		#for bit in originalInputVector.getVector():
		# 	print(bit.bit)
		# print('')
		# print(inputString)


		if outputString in predictions: # predictions was set up at the start, you might have missed it. 
			currentPredictionString = predictions[outputString]
		else:
			currentPredictionString = "[New input]"
			predictions[outputString] = inputString # I'm sure this line should be here. It's not indented in the origonal. 
   
		print("Round: %d" % round) # Prints the number of the round
		printStats(inputString, currentPredictionString)
  
		if (round > trainingRounds): 
			correctBitPredictions += stringOverlap(currentPredictionString, predictions[outputString])
				 

		newRegion.doRound() # The CLA bit!
		printColumnStats(newRegion) 
  
      
      # With the experiment now over, stat summaries are now printed. 
	for key in predictions:
		print("key: " + key + " predictions: " + predictions[key])
	print("Accuracy: " + str(float(correctBitPredictions)/float(30*(numRounds-trainingRounds))))


def stringOverlap(str1,str2):
	count = 0
	length = min(len(str1),len(str2)) # Returns the length of the smallest string
	for i in range(length):           # For the length of the smallest string, compare the bits
		if (str1[i] == str2[i]):    # If bits are equal, increment 'count'. 
			count += 1
	return count                     # Returns the number of bits in two strings which are the same. 


def printStats(inputVector,outputVector): # Does what it says in the name. 
	#print('Input-: ',end='')
      print('Input-:')
      print(inputVector)
      #print('Output: ',end='')
      print('Output-: ')
      print(outputVector)


def setInput(inputVector,bitArray): # Not sure about this. What does it do in main program?
	for i in range(inputVector.getLength()):
		bitValue = (bitArray & (1 << i) > 0)
		inputVector.getBit(i).setActive(bitValue)


def printColumnStats(r): # Called once on, or about, line 65
	alarmColumnCount = 0
	stableColumnCount = 0
	errorColumnsFound = 0
	for c in newRegion.columns:
		if (not c.isActive()):
				continue
		allCellsActive = True
		cellActiveFound = False
		for cell in c.cells:
			if (not cell.isActive(CURRENT_TIME_STEP)):
				allCellsActive = False
			else:
				cellActiveFound = True
		if allCellsActive:
			alarmColumnCount += 1
		elif cellActiveFound:
			stableColumnCount += 1
		else:
			errorColumnsFound += 1
	print("Alarm Columns: " + str(alarmColumnCount) + " Stable Columns: " + str(stableColumnCount))

# debug main run
print("Running!")
testCount() 
# This is the only bit that really executes. Everythig else is just a method. The test count method calls all the others.
