import random

from sklearn import datasets
iris = datasets.load_iris()

# Show the data (the attributes of each instance)
print(iris.data)

# Show the target values (in numeric format) of each instance
print(iris.target)

# Show the actual target names that correspond to each number
print(iris.target_names)

# A class to hold all the attributes
class IrisObject:
	data = []
	target = 0

# The classifier itself.
class Classifier:
	totalObjects     = 0
	correctResults   = 0

	def train(self, trainingSet):
		totalObjects = len(trainingSet)

	def predict(self, testingSet):
		totalObjects = len(testingSet)
		returnList = [0]

		for i in range(len(testingSet)):
			returnList.append(0)
		returnList.pop(0) #get rid of that initial 0 we made in line 30

		return returnList;

# The master list
irisObjectsList = [len(iris.data)]

# Loading up the master list...
for x in range(len(iris.data)):
	y = IrisObject()
	y.data = iris.data[x]
	print(y.data)
	y.target  = iris.target[x]
	irisObjectsList.append(y)
# ... I get the feeling that I'm doing all this the hard way, but whatever.

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# randomizing...
random.shuffle(irisObjectsList)
#clearing the random 150...
irisObjectsList.remove(150)

# Print out the new list for verification...
for x in range(len(iris.data)):
	print(irisObjectsList[x].data)
for x in range(len(iris.data)):
	print(irisObjectsList[x].target)

# dividing up irisObjectsList for splitting into train/test sets
tenthOfListLen = len(irisObjectsList) / 10

# build the training set
trainingSet = irisObjectsList.copy()
for i in range(int(tenthOfListLen * 7), len(irisObjectsList)):
	trainingSet.pop()

# build the testing set
testingSet = irisObjectsList.copy()
for i in range(0, len(irisObjectsList) - int(tenthOfListLen * 3)):
	testingSet.pop()

# IT'S ALIIIIIIVE
classE = Classifier() # pronounced like WALL-E's name. Very important.

# "train"
classE.train(trainingSet)

# "test"
results = classE.predict(testingSet)
print(results)

# check results and print the success percentage
for i in range(len(results)):
	if results[i] == testingSet[i].target:
		classE.correctResults += 1

# print results
print("\n")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\n")
print(classE.correctResults / len(testingSet), "percent accuracy. Git gud scrub.")