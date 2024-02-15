import constants
import definitions
import math

class QuadNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.mass = 0
        self.width = width
        self.height = height
        self.children = [None,None,None,None]
        self.object = None
        self.objectCount = 0
        self.center_of_mass_x = x
        self.center_of_mass_y = y

    def getQuad(self, x, y):
        if x < self.x:
            if y < self.y:
                return 0
            else:
                return 2
        else:
            if y < self.y:
                return 1
            else:
                return 3

    def insert(self, object):
        if self.objectCount == 0:
            # If the node is empty, add the object to it
            self.object = object
            self.mass = object.mass
        elif self.objectCount == 1:
            # If the node has only one object, move existing object to a child node and add the new object to a child node
            if self.children[self.getQuad(self.object.position.x, self.object.position.y)] == None:
                # Negative if the quad is 0 or 2, positive if the quad is 1 or 3
                newX = self.x + (self.width/4) * ((self.getQuad(self.object.position.x, self.object.position.y) % 2) * 2 - 1)
                # Negative if the quad is 0 or 1, positive if the quad is 2 or 3
                newY = self.y + (self.height/4) * ((self.getQuad(self.object.position.x, self.object.position.y) // 2) * 2 - 1)
                newNode = QuadNode(newX, newY, self.width/2, self.height/2)
                newNode.insert(self.object)
                self.children[self.getQuad(self.object.position.x, self.object.position.y)] = newNode
            else:
                self.children[self.getQuad(self.object.position.x, self.object.position.y)].insert(self.object)
            
            # Add the new object to a child node
            if self.children[self.getQuad(object.position.x, object.position.y)] == None:
                # Negative if the quad is 0 or 2, positive if the quad is 1 or 3
                newX = self.x + (self.width/4) * ((self.getQuad(object.position.x, object.position.y) % 2) * 2 - 1)
                # Negative if the quad is 0 or 1, positive if the quad is 2 or 3
                newY = self.y + (self.height/4) * ((self.getQuad(object.position.x, object.position.y) // 2) * 2 - 1)
                newNode = QuadNode(newX, newY, self.width/2, self.height/2)
                newNode.insert(object)
                self.children[self.getQuad(object.position.x, object.position.y)] = newNode
            else:
                self.children[self.getQuad(object.position.x, object.position.y)].insert(object)
            self.object = None
        else:
            # If the node has more than one object, add the new object to a child node
            if self.children[self.getQuad(object.position.x, object.position.y)] == None:
                # Negative if the quad is 0 or 2, positive if the quad is 1 or 3
                newX = self.x + (self.width/4) * ((self.getQuad(object.position.x, object.position.y) % 2) * 2 - 1)
                # Negative if the quad is 0 or 1, positive if the quad is 2 or 3
                newY = self.y + (self.height/4) * ((self.getQuad(object.position.x, object.position.y) // 2) * 2 - 1)
                newNode = QuadNode(newX, newY, self.width/2, self.height/2)
                newNode.insert(object)
                self.children[self.getQuad(object.position.x, object.position.y)] = newNode
            else:
                self.children[self.getQuad(object.position.x, object.position.y)].insert(object)

        '''
        self.mass += object.mass
        # Calculate center of mass based on childen and objects
        self.center_of_mass_x = 0
        self.center_of_mass_y = 0
        for child in self.children:
            if child != None:
                self.center_of_mass_x += child.center_of_mass_x
                self.center_of_mass_y += child.center_of_mass_y
        if self.object != None:
            self.center_of_mass_x += self.object.position.x
            self.center_of_mass_y += self.object.position.y
        self.center_of_mass_x /= self.objectCount + 1
        self.center_of_mass_y /= self.objectCount + 1'''
        self.objectCount += 1

    def computeCenterOfMass(self):
        self.mass = 0
        self.center_of_mass_x = 0
        self.center_of_mass_y = 0
        for child in self.children:
            if child != None:
                child.computeCenterOfMass()
                self.mass += child.mass
                self.center_of_mass_x += child.center_of_mass_x * child.mass
                self.center_of_mass_y += child.center_of_mass_y * child.mass
        if self.object != None:
            self.mass += self.object.mass
            self.center_of_mass_x += self.object.position.x * self.object.mass
            self.center_of_mass_y += self.object.position.y * self.object.mass
        if self.mass != 0:
            self.center_of_mass_x /= self.mass
            self.center_of_mass_y /= self.mass

def getForce(object, quad):
    # Return a tuple containing the normalized direction and magnitude of the force
    result = ((0, 0), 0)
    if quad.object != None:
        # Simply calculate the gravity force if the quad has only one object
        r = (quad.object.position - object.position).getMagnitude()
        if r != 0:
            direction = ((quad.object.position.x - object.position.x)/r, (quad.object.position.y - object.position.y)/r)
            magnitude = constants.G*quad.object.mass*object.mass/((r**2) + (constants.EPSILON**2))
            result = (direction, magnitude)
    else:
        # If the quad has more than one object, perform recursive calculation based on theta
        r = ((quad.center_of_mass_x - object.position.x)**2 + (quad.center_of_mass_y - object.position.y)**2)**0.5
        if r != 0:
            if quad.width/r < constants.THETA:
                direction = ((quad.center_of_mass_x - object.position.x)/r, (quad.center_of_mass_y - object.position.y)/r)
                magnitude = constants.G*quad.mass*object.mass/((r**2) + (constants.EPSILON**2))
                result = (direction, magnitude)
            else:
                for child in quad.children:
                    if child != None:
                        force = getForce(object, child)
                        # add the vectors
                        currentVector = (result[0][0] * result[1], result[0][1] * result[1])
                        newVector = (force[0][0] * force[1], force[0][1] * force[1])
                        resultVector = (currentVector[0] + newVector[0], currentVector[1] + newVector[1])
                        resultMagnitude = (resultVector[0]**2 + resultVector[1]**2)**0.5
                        if resultMagnitude != 0:
                            result = ((resultVector[0]/resultMagnitude, resultVector[1]/resultMagnitude), resultMagnitude)
    return result
