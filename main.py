#!/bin/python3

from hfinger.analysis import hfinger_analyze

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import OrdinalEncoder

# création du hash / import du dataset
pcap_path = "/home/loucas/Bureau/exp/ml/test.pcap"
reporting_mode = 4
fingerprints = [i.get('fingerprint') for i in hfinger_analyze(pcap_path,reporting_mode)]


# formatage du dataset
df = []

for i in fingerprints:
    fp = i.split("|")
    fp = list(map(lambda x : x if x != '' else 0, fp))
    df.append(fp)

df = pd.DataFrame(data=df)


# conversion des data strings en integers
ord_enc = OrdinalEncoder()
df[[6, 8, 9]] = ord_enc.fit_transform(df[[6, 8, 9]])

"""
Objectif de la classification :
Connaitre le nombres de clusters, classes, groupes ou segments (K)
N observations --> K groupes
On fait varier le nombre K tout en surveillant l'inertie intra-classe (W)
W correspond au degré d'homogéïnité des groupes que nous avons formé
"""

# Etape 1 : Identifier le nombre de cluster
tab = []

for i in range(10):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(df)
    tab.append(kmeans.inertia_)

plt.plot(range(10), tab)
plt.xlabel("Nombre de clusters")
plt.ylabel("Inertie W")
plt.show()
