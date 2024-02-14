
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
        self.center_of_mass_y /= self.objectCount + 1
        self.objectCount += 1