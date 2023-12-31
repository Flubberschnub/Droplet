import math
import constants
import random


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
        self.trail = Trail(self.position, self.size*2, (self.color[0], self.color[1], self.color[2]))
    
    def update(self):
        self.position += self.velocity * constants.TIME
        self.trail.position = self.position
        self.trail.update()
    
    def accelerateToward(self, position, magnitude):
        angle = math.atan2(position.y - self.position.y, position.x - self.position.x)
        direction = (math.cos(angle), math.sin(angle))
        self.velocity.x += (Acceleration(direction, magnitude) * constants.TIME).x
        self.velocity.y += (Acceleration(direction, magnitude) * constants.TIME).y

## Object subclass: massive object with point gravity
class MassiveObject(Object):
    def __init__(self, size, position, velocity, mass, name="Massive Object", color=(255, 0, 0)):
        super().__init__(size, position, velocity, name, color)
        self.mass = mass

    def gravity(self, obj):
        r = (obj.position - self.position).getMagnitude()
        return constants.G*self.mass*obj.mass/((r**2) + (constants.EPSILON**2))
    
    def update(self, objects):
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