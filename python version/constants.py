global TIME
global SCALE
global G
global EPSILON

TIME = 1000000
SCALE = 0.0000000001
G = 6.67408e-11
EPSILON = TIME * 500000

def setTime(time):
    global TIME
    TIME = time

def setScale(scale):
    global SCALE
    SCALE = scale

def setG(g):
    global G
    G = g