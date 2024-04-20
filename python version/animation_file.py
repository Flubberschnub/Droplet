import math
import constants
import random
import presets
import definitions
import barneshut
import tick
import numpy as np
from scipy.special import comb
from multiprocessing import Process, Pool
import preferences
import os

import pandas as pd

# Final animations will be stored on GitHub. Otherwise they will be stored on a local folder
final = False

# Name file
fileName = 'testFinalOfGalaxyCollision5000'
objects = preferences.presetObjects

# How many frames
totalFrames = 60*20
def totalFramesCalculation(fps, seconds):
    totalFrames = fps*seconds

# TIME speed
timeSpeed = 100
constants.setTime(constants.TIME * timeSpeed)

object_IDs = range(len(objects))
tickIndices = range(totalFrames)

# Data frame
index = pd.MultiIndex.from_product([tickIndices, object_IDs], names=['Time Tick', 'Object ID'])

animationData = pd.DataFrame(index=index, columns=['X Position', 'Y Position', 'Color', 'Size'])

def storeTickData(tickIndex):
    objID = 0
    for obj in objects:
        data = [obj.position.x, obj.position.y, obj.color, obj.size]
        animationData.loc[(tickIndex, objID), :] = data
        objID += 1

for tickIndex in range(totalFrames):
    storeTickData(tickIndex)
    tick.tick()

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

if final == True:
    data_folder = os.path.join(parent_dir, 'finalAnimations')
else:
    data_folder = os.path.join(parent_dir, 'animationFiles')

os.makedirs(data_folder, exist_ok=True)

csv_file_path = os.path.join(data_folder, fileName+'.csv')

animationData.to_csv(csv_file_path)
