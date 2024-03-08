#Activator and device module
import pygame

class ActivatorObject(object):
    def __init__(self,tilemap,row,col,active,key1,key2,device,pair):
        self.tilemap = tilemap
        self.row = row
        self.col = col
        self.x = self.tilemap.tileWidth * col
        self.y = self.tilemap.tileHeight * row
        self.active = active
        self.key1 = key1
        self.key2 = key2
        self.device = device
        self.pair = pair
    def checkCollision(self,player):
        self.active = False
        activatorRect = pygame.Rect(self.x,self.y,self.tilemap.tileWidth,self.tilemap.tileHeight)
        if activatorRect.colliderect(player.x,player.y,player.width,player.height):
            self.active = True
        else:
            for block in player.blockList:
                if activatorRect.colliderect(block.x,block.y,block.width,block.height):
                    self.active = True
                    break

class Button(ActivatorObject):
    def update(self):
        if self.active:
            self.tilemap.tileframe[self.row][self.col] = self.key2
            if self.device == "door":
                for row in range(self.tilemap.mapHeight):
                    for col in range(self.tilemap.mapWidth):
                        if self.tilemap.tileframe[row][col] == "D1":
                            self.tilemap.tileframe[row][col] = "D2"
            elif self.device == "gate":
                for gate in self.tilemap.gateList:
                    if gate.pair == self.pair:
                        self.tilemap.tileframe[gate.row][gate.col] = gate.key2
            elif self.device == "portal":
                for portal in self.tilemap.portalList:
                    if portal.pair == self.pair:
                        portal.active = True
                        self.tilemap.tileframe[portal.row][portal.col] = portal.key2
        else:
            self.tilemap.tileframe[self.row][self.col] = self.key1
            if self.device == "door":
                for row in range(self.tilemap.mapHeight):
                    for col in range(self.tilemap.mapWidth):
                        if self.tilemap.tileframe[row][col] == "D2":
                            self.tilemap.tileframe[row][col] = "D1"
            elif self.device == "gate":
                for gate in self.tilemap.gateList:
                    if gate.pair == self.pair:
                        self.tilemap.tileframe[gate.row][gate.col] = gate.key1
            elif self.device == "portal":
                for portal in self.tilemap.portalList:
                    if portal.pair == self.pair:
                        portal.active = False
                        self.tilemap.tileframe[portal.row][portal.col] = portal.key1

class Lever(ActivatorObject):
    def checkCollision(self,player):
        activatorRect = pygame.Rect(self.x,self.y,self.tilemap.tileWidth,self.tilemap.tileHeight)
        if activatorRect.colliderect(player.x,player.y,player.width,player.height):
            if self.active:
                self.active = False
            else:
                self.active = True
    def update(self):
        if self.active:
            self.tilemap.tileframe[self.row][self.col] = self.key2
            if self.device == "gate":
                for gate in self.tilemap.gateList:
                    if gate.pair == self.pair:
                        self.tilemap.tileframe[gate.row][gate.col] = gate.key2
            elif self.device == "portal":
                for portal in self.tilemap.portalList:
                    if portal.pair == self.pair:
                        portal.active = True
                        self.tilemap.tileframe[portal.row][portal.col] = portal.key2
        else:
            self.tilemap.tileframe[self.row][self.col] = self.key1
            if self.device == "gate":
                for gate in self.tilemap.gateList:
                    if gate.pair == self.pair:
                        self.tilemap.tileframe[gate.row][gate.col] = gate.key1
            elif self.device == "portal":
                for portal in self.tilemap.portalList:
                    if portal.pair == self.pair:
                        portal.active = False
                        self.tilemap.tileframe[portal.row][portal.col] = portal.key1

class DeviceObject(object):
    def __init__(self,tilemap,row,col,active,key1,key2,direction=None):
        self.tilemap = tilemap
        self.row = row
        self.col = col
        self.x = self.tilemap.tileWidth * col
        self.y = self.tilemap.tileHeight * row
        self.active = active
        self.key1 = key1
        self.key2 = key2
        self.direction = direction
    def checkCollision(self,player):
        deviceRect = pygame.Rect(self.x,self.y,self.tilemap.tileWidth,self.tilemap.tileHeight)
        if deviceRect.colliderect(player.x,player.y,player.width,player.height):
            return True
        return False

class Gate(DeviceObject):
    def __init__(self,tilemap,row,col,active,key1,key2,direction=None):
        super().__init__(tilemap,row,col,active,key1,key2,direction)
        self.pair = key1[0]

class Portal(DeviceObject):
    def __init__(self,tilemap,row,col,active,key1,key2,direction=None):
        super().__init__(tilemap,row,col,active,key1,key2,direction)
        self.pair = key1[0]
    def checkCollision(self,player):
        x = player.x
        y = player.y
        if self.direction == "left":
            x += 1
        elif self.direction == "right":
            x -= 1
        elif self.direction == "up":
            y += 1
        elif self.direction == "down":
            y -= 1
        deviceRect = pygame.Rect(self.x,self.y,self.tilemap.tileWidth,self.tilemap.tileHeight)
        if deviceRect.colliderect(x,y,player.width,player.height):
            for portal in self.tilemap.portalList:
                if portal.pair == self.pair and portal.key1 != self.key1:
                    newX = portal.x
                    newY = portal.y
                    if portal.direction == "left":
                        newX -= player.width + 1
                    elif portal.direction == "right":
                        newX += self.tilemap.tileWidth + player.width + 1
                    elif portal.direction == "up":
                        newY -= player.height + 1
                    elif portal.direction == "down":
                        newY += self.tilemap.tileHeight + player.height + 1
                    return newX,newY
        return player.x,player.y
