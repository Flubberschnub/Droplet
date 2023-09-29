import math
import constants
import random
import presets
import definitions
import numpy as np
from scipy.special import comb

def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)

    result = 0
    for n in range(0, N + 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result

# Initial objects (for testing)
objects = presets.objects_Flennestra

global massDensity
massDensity = 0

def tick():

    charLength = 0

    for obj in objects:
        global massDensity

        obj.update(objects)
        # Calculate average distance between particles and also mass density
        charLength = 0
        for obj2 in objects:
            if obj != obj2:
                charLength += (obj.position - obj2.position).getMagnitude()
                massDensity += (obj.mass + obj2.mass) / ((obj.position - obj2.position).getMagnitude()**2)
        charLength /= math.comb(len(objects), 2)
        massDensity /= math.comb(len(objects), 2)
        #print(obj.name + ":" + "(" + str(obj.position.x) + ", " + str(obj.position.y) + ")")

    ## lesser epsilon is more accurate
    ## greater epsilon is more stable
    constants.EPSILON = (math.sqrt(constants.TIME+1)) * (massDensity**0.9)