#!/bin/python
import os
import sys
import json

from difflib import SequenceMatcher
import jellyfish

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering



# -----------------------FONCTIONS------------------------#


# Fonction de calcul de distance avec sequenceMatcher

def distance(f1, f2):
    return (1 - SequenceMatcher(None, *sorted((f1, f2))).ratio())  # isjunk=None (no element ignored), .ratio give float between [0,1]


# Fonction de calcul de distance avec jellyfish
# Uncomment to use levenstein distance
"""
def distance(f1,f2):
    return(jellyfish.levenshtein_distance(f1,f2))
"""
# Uncomment to use jaro distance
"""
def distance(f1,f2):
    return(jellyfish.jaro_distance(f1,f2))
"""
# Uncomment to use damerau levenstein distance
"""
def distance(f1,f2):
    return(jellyfish.damerau_levenshtein_distance(f1,f2))
"""


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
def getClustersData(numberOfCluster, listOfClusters, listOfDistances, dataFile, outputFileName):

    data = {
        'clusters' : []
    }

    for cluster in listOfClusters:
        distanceMin = [999999999999999,9999999999999999999999, 9999999999]
        for fingerprint in cluster:
            somme = sum([listOfDistances[fingerprint[1]][j] for j in list(zip(*cluster))[1]])
            if(somme < distanceMin[2]):
                distanceMin=[*fingerprint, somme]
        maximum = max([listOfDistances[fingerprint[1]][j] for j in list(zip(*cluster))[1]])

        data['clusters'].append({ #Ajout dans le fichier Json
            'name' : dataFile,
            'idFingerprintRef' : distanceMin[1],
            'fingerprintRef' : distanceMin[0],
            'distanceRef' : maximum,
            'distancesReferences' : []
        })

    for i in range(numberOfCluster):
        for p in range(numberOfCluster):
            data['clusters'][i]['distancesReferences'].append(listOfDistances[data['clusters'][i]['idFingerprintRef']][data['clusters'][p]['idFingerprintRef']])


    with open(outputFileName, 'w') as outfile:
        json.dump(data, outfile)


# --------------------------MAIN--------------------------#

def main(dataFiles):

    numberOfCluster = 2
    listWithAllTaggedFingerprints = []      # Liste contenant toutes les fingerprints et leur fichier associé
    listOfFingerprints = []                 # Liste contenant toutes les fingerprints
    listOfDistances = []                    # Chaque liste contient l'ensemble des distances par rapport a une empreinte.
    listOfClusters = []                     # Liste de tous les clusters contenant chacun les empreintes correspondantes

    # Formatage des empreintes
    for dataFile in dataFiles:
        with open(dataFile, "r") as file:
            listOfFingerprintsInFile = [line.replace('\n', '') for line in file]
            listOfFingerprintsInFile = sorted(set(listOfFingerprintsInFile), key = listOfFingerprintsInFile.index)  # Retire les doublons ET prévserve l'ordre
            listOfFingerprintsInFile2 = []
            for y in range(len(listOfFingerprintsInFile)):
                listOfFingerprintsInFile2.append([listOfFingerprintsInFile[y], dataFile])
        listOfFingerprints.extend(listOfFingerprintsInFile)
        listWithAllTaggedFingerprints.extend(listOfFingerprintsInFile2)
        listOfFingerprints = [stringLine for stringLine in listOfFingerprints if stringLine != ""] #Supprime les lignes vides

        # Création de la matrice de distances
        for fingerprint in listOfFingerprints:
            listOfDistanceForOneFingerprint = []
            for fingerprint2 in listOfFingerprints:
                listOfDistanceForOneFingerprint.append(distance(fingerprint, fingerprint2))
            listOfDistances.append(listOfDistanceForOneFingerprint)

        # Création du modèle
        model = AgglomerativeClustering(distance_threshold = None, n_clusters = numberOfCluster)  # n_cluster= number of cluster to find, if not none distance must be none.
        model = model.fit(listOfDistances)

        # Affichage
        """
        plt.title("Dendogramme de Regroupement Hierarchique")
        plot_dendrogram(model, truncate_mode="level", p=10) # plot the top ten levels of the dendrogram
        plt.xlabel("Nombre de points dans un noeud (ou index de point s'il n'y a pas de parenthèse)")
        plt.ylabel("Distance entre les clusters")
        plt.show()
        print(model.n_clusters_)
        print(model.labels_)
        """

        # Création de la liste contenant les différents clusters
        for indexCluster in range(numberOfCluster):
            cluster = [[listOfFingerprints[indexFingerprint], indexFingerprint] for indexFingerprint in range(len(listOfFingerprints)) if model.labels_[indexFingerprint] == indexCluster]
            listOfClusters.append(cluster)

        getClustersData(numberOfCluster, listOfClusters, listOfDistances, dataFile, 'fingerprintRef.json')

if __name__ == '__main__':
    dataFiles = sys.argv[1:]
    main(dataFiles)
    os.system("cat fingerprintRef.json | jq")


























"""
import re

    for n in range(numberOfCluster):
        # Will be reset for each cluster needed
        stats = {}  # dictionary containing stats for a cluster
        results = []  # contains wanted fingerprints followed by its txt source
        print("\ncluster number " + str(n))
        for p in range(len(listOfFingerprints)):
            if model.labels_[p] == k:
                results.append(listOfFingerprints[p] + ' ' + listWithAllTaggedFingerprints[p][1])
        # show some stats
        # fetch name at each end of fingerprint and count in a dictionary
        for finger in results:
            # split with space presence
            text_file_name = re.split("\s", finger)
            # dict exists
            if text_file_name[1] in stats:
                stats[text_file_name[1]] += 1
            # dict does not exist
            else:
                stats[text_file_name[1]] = 1
        # do maths with stats dictionary
        cluster_size = 0
        for key in stats:
            cluster_size += stats[key]
        for key in stats:
            stats[key] = str(round(stats[key]/cluster_size*100, 2)) + "%"
        #print(stats)
        for res in results:
            pass
            #print(res)
"""
