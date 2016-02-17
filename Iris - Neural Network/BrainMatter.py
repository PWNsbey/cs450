import random


class IONode:
    isEndNode = False  # also, end nodes always are stuck right onto a neuron's output
    value = 0
    connections = []

    networkIndexRef = 0

    def update(self):
        if self.isEndNode:
            self.value = self.connection.outputValue

class NeuralConnection:
    inputObject = None   # the input or neuron providing a value
    outputObject = None  # the output or neuron receiving a value

    weight = (random.randint(-10, 10))/10  # todo: fix this
    weightedValue = 0

    networkIndexRef = 0

    def update(self):
        self.computeWeightedValue()

    def computeWeightedValue(self):
        if self.inputObject is IONode:
            self.weightedValue = self.inputObject.value * self.weight
        else:  # if not, it should be a Neuron. SHOULD.
            self.weightedValue = self.inputObject.outputValue * self.weight

class Neuron:
    incomingConnections = []  # all connections linking to this neuron
    outgoingConnections = []  # all outgoing connections leaving this neuron

    threshold = 0
    outputValue = 0

    networkIndexRef = 0

    def update(self):
        sum = 0
        for i in range(len(self.incomingConnections)):
            sum += self.incomingConnections[i].weightedValue

        if sum <= self.threshold:
            self.outputValue = 0
        else:
            self.outputValue = 1
