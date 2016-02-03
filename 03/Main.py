from sklearn import datasets
from DataWizard import Wizard
from Iris import Iris as Iris

dataset = datasets.load_iris()

print("Dataset values:")

# Show the data (the attributes of each example)
print(dataset.data)

# Show the target values (in numeric format) of each example
print(dataset.target)

# Show the actual target names that correspond to each number
print(dataset.target_names)

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# organize and get the data back from the Wizard
discreteRefList = [4, 4, 4, 4]
wizard = Wizard(dataset, discreteRefList)
workingDatasets = wizard.organize_data()

iris = Iris(discreteRefList, wizard)
iris.train(workingDatasets[0])

iris.printTree()

iris.categorize(workingDatasets[1])
print( "\n\n\n", str(iris.accuracy) + "% correct")
