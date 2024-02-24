import math
import constants
import random
import presets
import definitions
import barneshut
import numpy as np
from scipy.special import comb
from multiprocessing import Process, Pool
import os

def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)

    result = 0
    for n in range(0, N + 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result

# Initial objects (for testing)
objects = presets.objects_Random

global massDensity
massDensity = 0

global quadtree

def updateObject(obj, quadtree):
    for i in range(int(constants.TIME / constants.TIMESTEP)):
        obj.update(quadtree)
    return obj

def tick():
    #This function is called every frame
    
    # Create quadtree
    global quadtree
    # create quadtree root node based on the distance of the furthest objects
    leftmost = min(objects, key=lambda obj: obj.position.x).position.x
    rightmost = max(objects, key=lambda obj: obj.position.x).position.x
    topmost = min(objects, key=lambda obj: obj.position.y).position.y
    bottommost = max(objects, key=lambda obj: obj.position.y).position.y
    quadtree = barneshut.QuadNode(0, 0, max(abs(rightmost), abs(leftmost), abs(topmost), abs(bottommost))*2, max(abs(rightmost), abs(leftmost), abs(topmost), abs(bottommost))*2)
    for obj in objects:
        quadtree.insert(obj)
    quadtree.computeCenterOfMass()

    charLength = 0

    for obj in objects:
        global massDensity

        for i in range(int(constants.TIME / constants.TIMESTEP)):
            obj.update(quadtree)



            #obj.naiveupdate(objects)
        # Calculate average distance between particles and also mass density
        '''charLength = 0
        for obj2 in objects:
            if obj != obj2:
                charLength += (obj.position - obj2.position).getMagnitude()
                massDensity += (obj.mass + obj2.mass) / ((obj.position - obj2.position).getMagnitude()**2)
        charLength /= math.comb(len(objects), 2)
        massDensity /= math.comb(len(objects), 2)'''
        #print(obj.name + ":" + "(" + str(obj.position.x) + ", " + str(obj.position.y) + ")")

    ## lesser epsilon is more accurate
    ## greater epsilon is more stable
    constants.EPSILON = 5000000000000#(math.sqrt(constants.TIME+1)) * (massDensity**0.9)
    constants.TIMESTEP = constants.TIME / 1