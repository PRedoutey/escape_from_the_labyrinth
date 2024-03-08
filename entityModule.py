#Player and block module
import pygame
import time

def frames(surface,width,height,divisions):
    frameList = []
    for i in range(divisions):
        frameList.append(surface.subsurface((8+i*width,7,16,21)))
    return frameList

class EntityObject(object):
    def __init__(self,renderSurface,tilemap,x,y,surface):
        self.ds = renderSurface
        self.tilemap = tilemap
        self.x = x
        self.y = y
        self.surface = surface
        self.dx = 0
        self.dy = 0
        self.width = surface.get_width()
        self.height = surface.get_height()
    def render(self):
        self.ds.blit(self.surface,(int(self.x-self.tilemap.windowLeft),int(self.y-self.tilemap.windowTop)))
    def update(self,friction=0.8):
        check = False
        self.x += self.dx
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dx > 0:
                    self.x -= .1
                else:
                    self.x += .1
            self.dx = 0
        self.dx *= friction
        self.y += self.dy
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dy > 0:
                    self.y -= .1
                else:
                    self.y += .1
            self.dy = 0
        self.dy *= friction
        return check

class PlayerObject(EntityObject):
    def __init__(self,renderSurface,tilemap,surfaceList,width,height):
        self.ds = renderSurface
        self.tilemap = tilemap
        self.x = float(tilemap.playerInfo[0])
        self.y = float(tilemap.playerInfo[1])
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height
        self.animTimer = time.time()
        self.walkImagesL = frames(surfaceList[0],32,32,4)
        self.walkImagesR = frames(surfaceList[1],32,32,4)
        self.walkImagesU = frames(surfaceList[2],32,32,4)
        self.walkImagesD = frames(surfaceList[3],32,32,4)
        self.walkImagesLU = frames(surfaceList[4],32,32,4)
        self.walkImagesLD = frames(surfaceList[5],32,32,4)
        self.walkImagesRU = frames(surfaceList[6],32,32,4)
        self.walkImagesRD = frames(surfaceList[7],32,32,4)
        self.idleImage = self.walkImagesD[0]
        self.walkAnimFrame = 0
        self.direction = "D"
        self.isMoving = False
        self.animUpdatePeriod=0.1
        self.blockList = []
        for block in tilemap.blockInfoList:
            self.blockList.append(BlockObject(renderSurface,tilemap,float(block[0]),float(block[1]),pygame.image.load("assets/block1.png")))
    def render(self):
        if self.isMoving == False:
            self.walkAnimFrame=0
        if self.direction == "L":
            currentFrame = self.walkImagesL[self.walkAnimFrame]
        elif self.direction == "R":
            currentFrame = self.walkImagesR[self.walkAnimFrame]
        elif self.direction == "U":
            currentFrame = self.walkImagesU[self.walkAnimFrame]
        elif self.direction == "D":
            currentFrame = self.walkImagesD[self.walkAnimFrame]
        elif self.direction == "LU":
            currentFrame = self.walkImagesLU[self.walkAnimFrame]
        elif self.direction == "LD":
            currentFrame = self.walkImagesLD[self.walkAnimFrame]
        elif self.direction == "RU":
            currentFrame = self.walkImagesRU[self.walkAnimFrame]
        elif self.direction == "RD":
            currentFrame = self.walkImagesRD[self.walkAnimFrame]
        else:
            currentFrame = self.idleImage
        self.ds.blit(currentFrame,(self.x,self.y))
    def renderBlocks(self):
        for block in self.blockList:
            block.render()
    def moveLeft(self):
        self.direction += "L"
        self.isMoving = True
        if self.dx > -2:
            self.dx -= .5
        for block in self.blockList:
            playerRect = pygame.Rect(self.x+self.dx,self.y,self.width,self.height)
            if playerRect.colliderect(block.x,block.y,block.width,block.height):
                self.dx = 0
                block.dx = -.5
                if self.updateBlocks():
                    self.dx = 0
    def moveRight(self):
        self.direction += "R"
        self.isMoving = True
        if self.dx < 2:
            self.dx += .5
        for block in self.blockList:
            playerRect = pygame.Rect(self.x+self.dx,self.y,self.width,self.height)
            if playerRect.colliderect(block.x,block.y,block.width,block.height):
                self.dx = 0
                block.dx = .5
                if self.updateBlocks():
                    self.dx = 0
    def moveUp(self):
        self.direction += "U"
        self.isMoving = True
        if self.dy > -2:
            self.dy -= .5
        for block in self.blockList:
            playerRect = pygame.Rect(self.x,self.y+self.dy,self.width,self.height)
            if playerRect.colliderect(block.x,block.y,block.width,block.height):
                self.dy = 0
                block.dy = -.5
                if self.updateBlocks():
                    self.dy = 0
    def moveDown(self):
        self.direction += "D"
        self.isMoving = True
        if self.dy < 2:
            self.dy += 1
        for block in self.blockList:
            playerRect = pygame.Rect(self.x,self.y+self.dy,self.width,self.height)
            if playerRect.colliderect(block.x,block.y,block.width,block.height):
                self.dy = 0
                block.dy = .5
                if self.updateBlocks():
                    self.dy = 0
    def update(self,friction=0.8):
        elapsedTime = time.time() - self.animTimer
        if self.isMoving and elapsedTime > self.animUpdatePeriod:
            self.walkAnimFrame += 1
            self.animTimer = time.time()
            if self.walkAnimFrame > 3:
                self.walkAnimFrame = 0
        check = False
        self.x += self.dx
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        for collideType in collideTypeList:
            if "portal" in collideType:
                row = collideType[0]
                col = collideType[1]
                for portal in self.tilemap.portalList:
                    if portal.row == row and portal.col == col:
                        if portal.active:
                            self.x,self.y = portal.checkCollision(self)
                        break
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dx > 0:
                    self.x -= .1
                else:
                    self.x += .1
            self.dx = 0
        self.dx *= friction
        self.y += self.dy
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        for collideType in collideTypeList:
            if "portal" in collideType:
                row = collideType[0]
                col = collideType[1]
                for portal in self.tilemap.portalList:
                    if portal.row == row and portal.col == col:
                        self.x,self.y = portal.checkCollision(self)
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dy > 0:
                    self.y -= .1
                else:
                    self.y += .1
            self.dy = 0
        self.dy *= friction
        return check
    def updateBlocks(self):
        check = False
        for block in self.blockList:
            if block.update(0):
                check = True
        return check

class BlockObject(EntityObject):
    def update(self,friction=0):
        check = False
        self.x += self.dx
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dx > 0:
                    self.x -= .1
                else:
                    self.x += .1
        self.dx *= friction
        self.y += self.dy
        collides,collideTypeList = self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)
        if collides != False:
            check = True
            while self.tilemap.checkTileCollision(self.x,self.y,self.width,self.height)[0] != False:
                if self.dy > 0:
                    self.y -= .1
                else:
                    self.y += .1
        self.dy *= friction
        return check
