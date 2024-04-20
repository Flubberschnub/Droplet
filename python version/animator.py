
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
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
# Get Data

# File Name
fileName = 'testFinalOfGalaxyCollision5000'

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
csv_folder_path = os.path.join(parent_dir, 'finalAnimations')
csv_file_path = os.path.join(csv_folder_path, fileName+'.csv')


animationData = pd.read_csv(csv_file_path)
animationData.set_index(['Time Tick', 'Object ID'], inplace=True)

largestindex = animationData.index.max()

numberOfObjects = largestindex[1]+1
totalFrames = largestindex[0]+1

### Initalize plot

fig, ax = plot.subplots()

def init():
    ax.set_xlim(-10**13, 10**13)
    ax.set_ylim(-10**13, 10**13)
    return []

def xPositions(frame):
    xList = []
    for objID in range(numberOfObjects):
        x = animationData.loc[(frame, objID)].iloc[0]
        xList.append(x)
    return xList

def yPositions(frame):
    yList = []
    for objID in range(numberOfObjects):
        y = animationData.loc[(frame, objID)].iloc[1]
        yList.append(y)
    return yList

def update(frame):
    ax.clear()
    ax.set_xlim(-10**13, 10**13)
    ax.set_ylim(-10**13, 10**13)

    x = xPositions(frame)
    y = yPositions(frame)
    print(x,y)

    ax.scatter(x, y)
    return []

ani = FuncAnimation(fig, update, frames=range(totalFrames), interval = 1, init_func = init, blit = True)

plot.show()
