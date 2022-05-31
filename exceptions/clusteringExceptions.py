class BadNumberOfCluster(Exception):
    def __str__(self):
        return "Wrong Type for the number of Cluster. Should be 'int'"

class BothOptionsUsed(Exception):
    def __str__(self):
        return "You have to choose only one option between distance and threshold."
