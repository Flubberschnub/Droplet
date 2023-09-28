import math
import constants
import random

# Global constants
global G
global TIME
global EPSILON
G = constants.G
TIME = constants.TIME
EPSILON = constants.EPSILON

## 2D Vector Class
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if issubclass(type(other), Vector):
            return type(self)(self.x * other.x, self.y * other.y)
        else:
            return type(self)(self.x * other, self.y * other)

    def getMagnitude(self):
        return (self.x**2 + self.y**2)**0.5

    def getDirection(self):
        return (self.x/self.getMagnitude(), self.y/self.getMagnitude())

## Position Class: 2D position vector
class Position(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)

## Velocity Class: 2D velocity vector
class Velocity(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)

## Acceleration Class: 2D acceleration vector
class Acceleration(Vector):
    def __init__(self, x, y):
        if type(x) == type(y):
            super().__init__(x, y)
        else:
            self.x = math.cos(math.atan2(x[1],x[0])) * y
            self.y = math.sin(math.atan2(x[1],x[0])) * y

## Object class: basic object with size, position, and velocity
class Object:
    def __init__(self, size, position, velocity, name="Object", color=(255, 255, 255)):
        self.size = size
        self.position = position
        self.velocity = velocity
        self.name = name
        self.color = color
    
    def update(self):
        self.position += self.velocity * TIME
    
    def accelerateToward(self, position, magnitude):
        angle = math.atan2(position.y - self.position.y, position.x - self.position.x)
        direction = (math.cos(angle), math.sin(angle))
        self.velocity.x += (Acceleration(direction, magnitude) * TIME).x
        self.velocity.y += (Acceleration(direction, magnitude) * TIME).y

## Object subclass: massive object with point gravity
class MassiveObject(Object):
    def __init__(self, size, position, velocity, mass, name="Massive Object", color=(255, 0, 0)):
        super().__init__(size, position, velocity, name, color)
        self.mass = mass

    def gravity(self, obj):
        r = (obj.position - self.position).getMagnitude()
        return G*self.mass*obj.mass/((r**2) + (EPSILON**2))
    
    def update(self):
        for obj in objects:
            if obj != self:
                obj.accelerateToward(self.position,(self.gravity(obj)/obj.mass))
        super().update()



# Initial objects (for testing)
# Randomized values
ACA = MassiveObject(6.96*(10**8), Position(random.uniform(-5*(10**12), 5*(10**12)), random.uniform(-5*(10**12), 5*(10**12))), Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 2*(10**30), "Alpha Centauri A")
ACB = MassiveObject(4.91*(10**8), Position(random.uniform(-5*(10**12), 5*(10**12)), random.uniform(-5*(10**12), 5*(10**12))), Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 1.6*(10**30), "Alpha Centauri B")
PC = MassiveObject(7.4*(10**7), Position(random.uniform(-5*(10**12), 5*(10**12)), random.uniform(-5*(10**12), 5*(10**12))), Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 2.39*(10**29), "Proxima Centauri")
TS = MassiveObject(7*(10**7), Position(random.uniform(-5*(10**12), 5*(10**12)), random.uniform(-5*(10**12), 5*(10**12))), Velocity(random.uniform(-5000, 5000), random.uniform(-5000, 5000)), 5.97*(10**24), "Trisolaris")

objects = [ACA, ACB, PC, TS]



def tick():

    # Global constants
    global G
    global TIME
    global EPSILON
    G = constants.G
    TIME = constants.TIME
    EPSILON = TIME * 500000

    for obj in objects:
        obj.update()
        print(obj.name + ":" + "(" + str(obj.position.x) + ", " + str(obj.position.y) + ")")