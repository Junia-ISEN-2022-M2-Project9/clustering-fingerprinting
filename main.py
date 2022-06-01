import argparse

from fingerprinting import createFingerprint, formatFpFile
from clustering import createCluster, analyseFile
from display.doGraph import displaygraph

#----------------------------PARSING ARGUMENTS---------------------------------#
parser = argparse.ArgumentParser(description = "Fingerprinting & Clustering")

parser.add_argument(
    "--files",
    "-f",
    nargs = "+",
    default = None,
    help = "Read a single or multiple pcap or fingerprint files",
)

parser.add_argument(
    "--format",
    default = "pcap",
    choices = ["pcap", "fingerprint"],
    help = "Choose the format between pcap (default) and fingerprint",
)

parser.add_argument(
    "-m",
    "--mode",
    type = int,
    default = 2,
    choices = [0, 1, 2, 3, 4],
    help = "Fingerprint report mode. "
    "\n0 - similar number of collisions and fingerprints as mode 2, but using fewer features, "
    "\n1 - representation of all designed features, but a little more collisions than modes 0, 2, and 4, "
    "\n2 - optimal (the default mode), "
    "\n3 - the lowest number of generated fingerprints, but the highest number of collisions, "
    "\n4 - the highest fingerprint entropy, but slightly more fingerprints than modes 0-2",
)

parser.add_argument(
    "--clusters",
    "-c",
    default = None,
    help = "Number of clusters",
)

parser.add_argument(
    "--threshold",
    "-t",
    default = None,
    help = "Distance max between two fingerprints in a cluster",
)

parser.add_argument(
    "--distance-algorithm",
    "-da",
    default = "sequence-matcher",
    choices = ["sequence-matcher", "levenshtein", "jaro", "damerau-levenshtein"],
    help = "Uses the sequence matcher distance by default, ",
)

parser.add_argument(
    "--stats",
    "-s",
    help = "Display stats",
    action = "store_true",
)

parser.add_argument(
    "--json",
    "-j",
    default = "./output.json",
    help = "Specify an output file to get clusters data at json format",
)

parser.add_argument(
    "--graph",
    "-g",
    nargs = "+",
    help = "Get a graphical representation of fingerprints. You can precise a pcap to analyze",
)

# Variable renaming
args = parser.parse_args()

inputFiles = args.files
format = args.format
numberOfCluster = args.clusters
distanceThreshold = args.threshold
distanceAlgorithm = args.distance_algorithm
reportingMode = args.mode
outputFileName = args.json
enableStats = args.stats
userFile = args.graph

numberOfCluster = int(numberOfCluster) if numberOfCluster != None else None
distanceThreshold = int(distanceThreshold) if distanceThreshold != None else None

#-------------------------------FINGERPRINTING---------------------------------#

dictOfFingerprints = createFingerprint(inputFiles, format, reportingMode)

#---------------------------------CLUSTERING-----------------------------------#

clustersData = createCluster(dictOfFingerprints, outputFileName, enableStats, distanceThreshold, numberOfCluster, distanceAlgorithm)

#----------------------------------GRAPHICS------------------------------------#

if userFile:
    listOfUserFingerprints = createFingerprint(userFile, format, reportingMode)
    userData = analyseFile(listOfUserFingerprints, clustersData, distanceAlgorithm)
    displaygraph(clustersData,userData)
    
