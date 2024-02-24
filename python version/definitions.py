import math
import constants
import random
import barneshut
import numpy as np
import scipy.integrate as spi


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
        
    def normalized(self):
        # Convert to unit vector
        result = type(self)(self.x, self.y)
        magnitude = self.getMagnitude()
        if magnitude != 0:
            result.x /= magnitude
            result.y /= magnitude
        return result

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
        self.trail = Trail(self.position, self.size*2, (self.color[0], self.color[1], self.color[2]))
    
    def update(self):
        #leapfrog integration

        self.position += self.velocity * constants.TIMESTEP

        self.trail.position = self.position
        self.trail.update()
    
    # Accelerate toward a position with a given magnitude
    def accelerateToward(self, position, magnitude):
        angle = math.atan2(position.y - self.position.y, position.x - self.position.x)
        direction = (math.cos(angle), math.sin(angle))
        self.velocity.x += (Acceleration(direction, magnitude) * constants.TIMESTEP).x
        self.velocity.y += (Acceleration(direction, magnitude) * constants.TIMESTEP).y
    
    # Accelerate given a direction and magnitude
    def accelerate(self, direction, magnitude):
        self.velocity.x += (direction[0] * magnitude * constants.TIME)
        self.velocity.y += (direction[1] * magnitude * constants.TIME)

## Object subclass: massive object with point gravity
class MassiveObject(Object):
    def __init__(self, size, position, velocity, mass, name="Massive Object", color=(255, 0, 0)):
        super().__init__(size, position, velocity, name, color)
        self.mass = mass
        self.acceleration = Acceleration(0, 0)

    def gravity(self, obj):
        r = (obj.position - self.position).getMagnitude()
        return constants.G*self.mass*obj.mass/((r**2) + (constants.EPSILON**2))
    
    def update(self, quadtree):
        '''for obj in objects:
            if obj != self:
                obj.accelerateToward(self.position,(self.gravity(obj)/obj.mass))'''
        force = barneshut.getForce(self, quadtree)
        accelerationFromForce = Acceleration((force[0][0]*force[1])/self.mass, (force[0][1]*force[1])/self.mass)
        #self.accelerate(force[0], force[1]/self.mass)
        
        # leapfrog integration
        self.velocity += (self.acceleration * (constants.TIMESTEP/2)) #kick
        super().update() # drift
        self.acceleration = accelerationFromForce #calc a_t+1
        self.velocity += (self.acceleration * (constants.TIMESTEP/2)) #kick

    def naiveupdate(self, objects):
        for obj in objects:
            if obj != self:
                obj.accelerateToward(self.position,(self.gravity(obj)/obj.mass))
        super().update()



## Trail Class: trail of an object
class Trail:
    def __init__(self, pos, size, color=(255, 255, 255)):
        self.position = pos
        self.color = color
        self.size = size
        self.length = self.size * 0.0000005
        self.trail = []
    
    def update(self):
        self.trail.append(self.position)
        if len(self.trail) > self.length:
            self.trail.pop(0)