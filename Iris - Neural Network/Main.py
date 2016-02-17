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
wizard = Wizard(dataset)
workingDatasets = wizard.organize_data()

nodeLayersArray = [1]  # LAST NEURON LAYER SHOULD BE DETERMINED BY NUMBER OF POSSIBLE TARGETS
Iris = Iris()
Iris.train(workingDatasets[0], nodeLayersArray)