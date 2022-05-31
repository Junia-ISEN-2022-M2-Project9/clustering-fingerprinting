#!/bin/python
import os
import sys
import json
import re

from exceptions.clusteringExceptions import (BadNumberOfCluster, BothOptionsUsed)

from difflib import SequenceMatcher
import jellyfish

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

from scipy.cluster.hierarchy import ClusterWarning
from warnings import simplefilter

simplefilter("ignore", ClusterWarning)

# Fp = Fingerprint

# -----------------------FONCTIONS------------------------#


# Fonction de calcul de distance

def distance(distanceAlgorithm, f1, f2):
    if distanceAlgorithm == "sequence-matcher":
        return (1 - SequenceMatcher(None, *sorted((f1, f2))).ratio())  # isjunk=None (no element ignored), .ratio give float between [0,1]
    if distanceAlgorithm == "levenshtein":
        return jellyfish.levenshtein_distance(f1,f2)
    if distanceAlgorithm == "jaro":
        return jellyfish.jaro_distance(f1,f2)
    if distanceAlgorithm == "damerau-levenshtein":
        return jellyfish.damerau_levenshtein_distance(f1,f2)


# Dendogram display function
def plot_dendrogram(model, **kwargs):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
                counts[i] = current_count

                linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)

                # Plot the corresponding dendrogram
                dendrogram(linkage_matrix, **kwargs)


# Write the useful information into a JSON file
def getClustersData(numberOfCluster, listOfClusters, listOfDistances, outputFileName):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    data = {
        'clusters' : []
    }

    n=0
    for cluster in listOfClusters:
        distanceMin = [999999999999999,9999999999999999999999, 9999999999]
        for fingerprint in cluster:
            somme = sum([listOfDistances[fingerprint[1]][j] for j in list(zip(*cluster))[1]])
            if(somme < distanceMin[2]):
                distanceMin=[*fingerprint, somme]
        maximum = max([listOfDistances[fingerprint[1]][j] for j in list(zip(*cluster))[1]])

        data['clusters'].append({ #Ajout dans le fichier Json
            'name' : "cluster"+str(n),
            'idFingerprintRef' : distanceMin[1],
            'fingerprintRef' : distanceMin[0],
            'distanceRef' : maximum,
            'distancesReferences' : {},
            'listePoints' : {}
        })
        n+=1

    for i in range(numberOfCluster):
        a = 0
        for z in range(3): # Prends les trois premiers points du cluster pour donner la forme generale.
            distances = {}
            count = 0
            for m in range(numberOfCluster): # ajoute distance autres cluster rapport aux points selectiones
                try:
                    distances[alphabet[count]] = (listOfDistances[listOfClusters[i][z][1]][data['clusters'][m]['idFingerprintRef']])
                    count += 1
                except IndexError:
                    a = 1
            if a != 1:
                data['clusters'][i]['listePoints']['point'+str(z)]=(distances)

        dic = {}
        for p in range(numberOfCluster): # Ajoute distance autres points de reference compare au cluster
            dic[alphabet[p]] = listOfDistances[data['clusters'][i]['idFingerprintRef']][data['clusters'][p]['idFingerprintRef']]
        data['clusters'][i]['distancesReferences'] = dic

    if (outputFileName):
        with open(outputFileName, 'w') as outfile:
            json.dump(data, outfile)
    return data

def showStats(model, listOfFingerprints, listWithAllTaggedFingerprints):
    for k in range(model.n_clusters_):
        # Will be reset for each cluster needed
        stats = {}                                  # dictionary containing stats for a cluster
        results = []                                # contains wanted fingerprints followed by its txt source
        print("\ncluster number " + str(k))
        for p in range(len(listOfFingerprints)):
            if model.labels_[p] == k:
                results.append(listOfFingerprints[p] + ' ' + listWithAllTaggedFingerprints[p][1])
        # show some stats
        # fetch name at each end of fingerprint and count in a dictionary
        for finger in results:
            # split with space presence
            textFileName = re.split("\s", finger)
            # dict exists
            if textFileName[1] in stats:
                stats[textFileName[1]] += 1
            # dict does not exist
            else:
                stats[textFileName[1]] = 1
        # do maths with stats dictionary
        clusterSize = 0
        for key in stats:
            clusterSize += stats[key]
        for key in stats:
            stats[key] = str(round(stats[key]/clusterSize*100, 2)) + "%"
        print(stats)
        print('Number of fingerprints in this cluster: ',clusterSize)
        #for res in results:
            #print(res)



# -----------------------------------MAIN--------------------------------------#

def createCluster(dictOfFingerprints, outputFileName, enableStats, distanceThreshold, numberOfCluster, distanceAlgorithm):

    # Error Handling
    if numberOfCluster != None and distanceThreshold != None:
        raise BothOptionsUsed

    if numberOfCluster != None and not isinstance(numberOfCluster, int):
        raise BadNumberOfCluster

    listOfFingerprints = []                 # Liste contenant toutes les fingerprints
    listWithAllTaggedFingerprints = []      # Liste contenant toutes les fingerprints et leur fichier associé
    listOfDistances = []                    # Chaque liste contient l'ensemble des distances par rapport a une empreinte.
    listOfClusters = []                     # Liste de tous les clusters contenant chacun les empreintes correspondantes

    # Formatage des empreintes
    for (nameOfFile, fpList) in dictOfFingerprints.items():
        listOfFingerprints.extend(fpList)
        listWithAllTaggedFingerprints.extend([[fp, nameOfFile] for fp in fpList])

    # Création de la matrice de distances
    for fp1 in listOfFingerprints:
        listOfDistanceForOneFingerprint = []
        for fp2 in listOfFingerprints:
            listOfDistanceForOneFingerprint.append(distance(distanceAlgorithm, fp1, fp2))
        listOfDistances.append(listOfDistanceForOneFingerprint)

    # Création du modèle
    model = AgglomerativeClustering(distance_threshold = distanceThreshold, n_clusters = numberOfCluster)  # n_cluster= number of cluster to find, if not none distance must be none.
    model = model.fit(listOfDistances)
    numberOfCluster = model.n_clusters_

    # Création de la liste contenant les différents clusters
    for indexCluster in range(numberOfCluster): #REMPLACER NUMBEROFCLUSTER PAR LA DISTANCE DANS L OBJET
        cluster = [[listOfFingerprints[indexFingerprint], indexFingerprint] for indexFingerprint in range(len(listOfFingerprints)) if model.labels_[indexFingerprint] == indexCluster]
        listOfClusters.append(cluster)

    data = getClustersData(numberOfCluster, listOfClusters, listOfDistances, outputFileName)

    # Show statistics about cluster data
    if enableStats:
        showStats(model, listOfFingerprints, listWithAllTaggedFingerprints)

    return data

def analyseFile(listOfUserFingerprints, clusterData, distanceAlgorithm):
    # Fichier clusterData = fingerprints en input à analyser
    # Fichier reference = fingerprints référentes des clusters

    result = [[distance(distanceAlgorithm, fp, clusterData["clusters"][idxFpRef]["fingerprintRef"]) for idxFpRef in range(len(clusterData["clusters"]))] for fp in listOfUserFingerprints]
    print(result)
