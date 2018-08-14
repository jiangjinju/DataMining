import random
import os


sourcefile = "cleanedTrain.txt"
testFile_start = "test_part"
trainFileStart = "train_part"

for count in range(1,11):
	testFile = testFile_start + str(count) + ".txt"
	trainFile = trainFileStart + str(count) + ".txt"
	
	if os.path.isfile(testFile):
		os.remove(testFile)		
	if os.path.isfile(trainFile):
		os.remove(trainFile)		


	linesForTest = random.sample(range(1, 19578), 500)

	file = open(sourcefile, 'r')
	i = 0
	for line in file:
		if (i in linesForTest):
			fileToWrite = testFile
		else:
			fileToWrite = trainFile
		with open(fileToWrite,'a') as mf:
			mf.write(line)
			mf.close
		i += 1
	file.close