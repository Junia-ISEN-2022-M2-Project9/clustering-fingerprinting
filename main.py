import argparse

from fingerprintClustering import createCluster

#----------------------------PARSING ARGUMENTS---------------------------------#
parser = argparse.ArgumentParser()

parser.add_argument("--files", "-f", nargs="+", help="Files of fingerprint")
parser.add_argument("--pcap", "-p", help="Pcap files")
parser.add_argument("--stats", "-s", help="Display stats", action="store_true")

parser.add_argument("--clusters", "-c",default=None, help="Number of clusters")
parser.add_argument("--threshold", "-t",default=None, help="Distance max between two fingerprints in a cluster")

parser.add_argument("--json", "-j", default="./output.json", help="Specify an output file to get clusters data at json format")


args = parser.parse_args()
numberOfCluster = args.clusters
distanceThreshold = args.threshold
dataFiles = args.files
outputFileName = args.json
enableStats = args.stats

if numberOfCluster != None:
    numberOfCluster = int(numberOfCluster)
    
if distanceThreshold != None:
    distanceThreshold = int(distanceThreshold)

#---------------------------------CLUSTERING-----------------------------------#
clustersData = createCluster(dataFiles, outputFileName, enableStats, distanceThreshold, numberOfCluster)

