from sklearn import datasets
from organizer import Organizer
from Iris import Iris

irisDataset = datasets.load_iris()

print("Dataset values:")

# Show the data (the attributes of each instance)
print(irisDataset.data)

# Show the target values (in numeric format) of each instance
print(irisDataset.target)

# Show the actual target names that correspond to each number
print(irisDataset.target_names)

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#organize and get the data back from the Organizer
workingDatasets = Organizer(irisDataset).organize_data()

# printing the shuffled sets
for i in range(len(workingDatasets[0])):
    print("Training set: ", workingDatasets[0][i].target)
print("-------------------------")
for i in range(len(workingDatasets[1])):
    print("Testing set: ", workingDatasets[1][i].target)
print("--------------------------------------------------------------")

# IT'S ALIIIIIIVE
Iris = Iris()

# Train that thang
Iris.train(workingDatasets[0])

# Run the predictions. Test mercilessly.
results = Iris.predict(workingDatasets[1], 4)

print(Iris.percent_correct(), "percent accuracy. Git gud scrub.")