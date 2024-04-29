import matplotlib
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

def setFrame(fixed, figure, magnitude):
    if fixed==True:
        figure.set_xlim(-1.6*10**magnitude, 1.6*10**magnitude)
        figure.set_ylim(-.9*10**magnitude, .9*10**magnitude)
    else:
        #replace with varying frame
        figure.set_xlim(-1.6*10**magnitude, 1.6*10**magnitude)
        figure.set_ylim(-.9*10**magnitude, .9*10**magnitude)

def prettify(uglyFigure):
    uglyFigure.set_facecolor('black')



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


    fig, ax = plot.subplots(figsize=(16,9), dpi = 300)
    plot.style.use("dark_background")

    def init():
        setFrame(fixedFrame, ax, 13)
        prettify(ax)
        return []

    def update(frame):
        ax.clear()
        setFrame(fixedFrame, ax, 13)

        x = listOfTraitAtTick(animationData, frame, numberOfObjects, 0)
        y = listOfTraitAtTick(animationData, frame, numberOfObjects, 1)
        ax.scatter(x, y, color='white', s=1)

        #Progress Bar
        if frame%(1+(totalFrames//1000)) == 0:
            statement = f"{(frame / totalFrames) * 100:.2f}% of frames animated"
            print (statement, end="\r")

        return []

    ani = FuncAnimation(fig, update, frames=range(totalFrames), interval = 1, init_func = init, blit = True, repeat = False)

    print("Frame Animation All Done")


    if showPlot == True:
        plot.show()

    return ani
