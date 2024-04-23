
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import pandas as pd
import os


### preferences
'''
filename

fixed picture frame size?
dynamic picture frame

fps

interpolation

'''

def inputPathFromName(fileName, final):
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    if final == False:
        csv_folder_path = os.path.join(parent_dir, 'testAnimations')
    else:
        csv_folder_path = os.path.join(parent_dir, 'animations')

    csv_file_path = os.path.join(csv_folder_path, fileName+'.csv')
    return csv_file_path

def setFrame(fixed, figure):
    if fixed==True:
        figure.set_xlim(-10**13, 10**13)
        figure.set_ylim(-10**13, 10**13)
    else:
        #replace with varying frame
        figure.set_xlim(-10**13, 10**13)
        figure.set_ylim(-10**13, 10**13)

def listOfTraitAtTick(data, frame, numberOfObjects, traitIndex):
    traitList = []
    for objID in range(numberOfObjects):
        trait = data.loc[(frame, objID)].iloc[traitIndex]
        traitList.append(trait)
    return traitList

def dataFromCSV(inputFileName, final):
    csv_file_path = inputPathFromName(inputFileName, final)

    # Set up MultiIndex datatable
    data = pd.read_csv(csv_file_path)
    data.set_index(['Time Tick', 'Object ID'], inplace=True)

    return data

def animationCreator(data = None, inputFileName = 'testName', fromCSV = False, showPlot = False, fixedFrame = True, final = False):

    # Get Data
    if fromCSV == True:
        animationData = dataFromCSV(inputFileName, final)
    else:
        animationData = data

    largestindex = animationData.index.max()

    numberOfObjects = largestindex[1]+1
    totalFrames = largestindex[0]+1

    ### Initalize plot

    fig, ax = plot.subplots()

    def init():
        setFrame(fixedFrame, ax)
        return []

    def update(frame):
        ax.clear()

        setFrame(fixedFrame, ax)

        x = listOfTraitAtTick(animationData, frame, numberOfObjects, 0)
        y = listOfTraitAtTick(animationData, frame, numberOfObjects, 1)

        ax.scatter(x, y)
        return []

    ani = FuncAnimation(fig, update, frames=range(totalFrames), interval = 1, init_func = init, blit = True, repeat = False)

    if showPlot == True:
        plot.show()

    return ani
