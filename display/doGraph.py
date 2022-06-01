import argparse
import json
import math
import random

import numpy as np
from matplotlib import pyplot as plt

def x_coord(ac, bc, ab):
    """
    X coord calculation
    Args:
        ac:
        bc:
        ab:

    Returns:

    """
    return (math.pow(ac, 2) - math.pow(bc, 2) + math.pow(ab, 2)) / (2 * ab)


def y_coord(ac, c_x):
    """
    Y coord calculation
    Args:
        ac:
        c_x:

    Returns:

    """
    tmp = (math.pow(ac, 2) - math.pow(c_x, 2))
    if tmp > 0:
        return math.sqrt(tmp)
    if tmp == 0:
        return 0
    else:
        tmp = -1 * tmp
        return math.sqrt(tmp) * -1


def dist(ax, bx, ay, by):
    """
    Simple distance calculation
    Args:
        ax:
        bx:
        ay:
        by:

    Returns:

    """
    return math.sqrt(math.pow((bx - ax), 2) + math.pow((by - ay), 2))


def build_init_coordinates(coord_object):
    """
    Create 2 first base points, will be used as reference for every other point to calculate
    Args:
        coord_object:

    Returns:

    """
    # cluster1 {0,0}
    # cluster2 {?,0}
    x_points = [0]
    y_points = [0, 0]

    # init base segment
    x_points.append(float(coord_object[0]["distancesReferences"]["B"]) * 10)

    # take values
    bx = x_points[len(x_points) - 1]
    ax = x_points[len(x_points) - 2]
    by = y_points[len(y_points) - 1]
    ay = y_points[len(y_points) - 2]
    ab = dist(ax, bx, ay, by)

    return ab


def process_entry(entry, color, ab):
    """
    Process a cluster in json
    Args:
        entry:
        color:
        ab:

    Returns:

    """
    # Gather needed infos
    name, distances, points = entry["name"], entry["distancesReferences"], entry["listePoints"]

    # First point
    ac = float(distances.get("A")) * 10
    bc = float(distances.get("B")) * 10
    cx = x_coord(ac, bc, ab)
    cy = y_coord(ac, x_coord(ac, bc, ab))

    # show first point with legend
    plt.plot(cx, cy, color=color, label=name, marker='o')

    # Side points
    for entry_point in points.values():
        ac = float(entry_point.get("A")) * 10
        bc = float(entry_point.get("B")) * 10
        cx = x_coord(ac, bc, ab)
        cy = y_coord(ac, x_coord(ac, bc, ab))
        # show
        plt.plot(cx, cy, color=color, marker='o')


def open_dico(dico):
    """
    Open dico and process data
    Args:
        dico:

    Returns:

    """
    #data = json.load(file)

        # Init coordinates
    ab = build_init_coordinates(dico['clusters'])

    for entry in dico['clusters']:
            # Distant color for each cluster
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
            # Do math
        process_entry(entry, color, ab)
        
    return ab
   
    
# Given json in parameter
def open_points(ab, listePoints):
    try:
        data = listePoints
        for entry in data:
            ac = entry[0] * 10
            bc = entry[1] * 10
            cx = x_coord(ac, bc, ab)
            cy = y_coord(ac, x_coord(ac, bc, ab))

            # show
            plt.plot(cx, cy, color='black', marker="+")
    except:
        pass


def displaygraph(referencePointDico, analyzedPoints):
    # plt display config
    ab = open_dico(referencePointDico)
    open_points(ab, analyzedPoints)
    plt.axis([-5, 15, -5, 15])
    plt.axis("equal")
    plt.legend()
    plt.show()
