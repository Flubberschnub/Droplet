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

# Name file
fileNameTest = 'testFinalOfGalaxyCollision5000'
objectsTest = preferences.presetObjects

def speedUpTime(factor):
    constants.setTime(constants.TIME * factor)

def totalFramesCalculation(fps, seconds):
    totalFrames = fps*seconds
    return totalFrames

def storeTickData(objects, tickIndex, dataTable):
    objID = 0
    for obj in objects:
        data = [obj.position.x, obj.position.y, obj.color, obj.size]
        dataTable.loc[(tickIndex, objID), :] = data
        objID += 1

def saveAsCSV(data, fileName):
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    data_folder = os.path.join(parent_dir, 'testAnimations')

    os.makedirs(data_folder, exist_ok=True)

    csv_file_path = os.path.join(data_folder, fileName+'.csv')

    data.to_csv(csv_file_path)

def createAnimationData(objects, lengthInSeconds, timeSpeedFactor = 100, fps = 24, saveCSV = False, csvFileName = 'csvFile'):
    # Set up given constants
    totalFrames = totalFramesCalculation(fps, lengthInSeconds)
    speedUpTime(timeSpeedFactor)
    object_IDs = range(len(objects))
    tickIndices = range(totalFrames)

    # Data frame
    index = pd.MultiIndex.from_product([tickIndices, object_IDs], names=['Time Tick', 'Object ID'])
    animationData = pd.DataFrame(index=index, columns=['X Position', 'Y Position', 'Color', 'Size'])

    # Run Engine and Store Data
    for tickIndex in range(totalFrames):
        storeTickData(objects, tickIndex, animationData)
        tick.tick()

    if saveCSV == True:
        saveAsCSV(animationData, csvFileName)
        print("CSV saved as " + csvFileName + " in testAnimations folder")

    return animationData
