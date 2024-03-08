#Tilemap module
import pygame
from deviceModule import *

class TileObject(object):
    def __init__(self,key,path,collides,collideType):
        self.key=key
        self.path=path
        self.surface=pygame.image.load(path)
        self.collides=collides
        self.collideType=collideType

class Tilemap(object):
    def __init__(self,renderSurface):
        self.tileframe=[None]*19
        for i in range(0,19):
            self.tileframe[i]=[None]*25
        self.ds = renderSurface
        self.level = 1
        self.mapWidth = 25
        self.mapHeight = 19
        self.tileWidth = 32
        self.tileHeight = 32
        self.windowLeft = 0
        self.windowTop = 0
        self.windowWidth = renderSurface.get_width()
        self.windowHeight = renderSurface.get_height()
        self.playerInfo = None
        self.blockInfoList = []
        self.tileList = []
        self.buttonList = []
        self.leverList = []
        self.gateList = []
        self.portalList = []
        
    def addTile(self,string,surface,collides,collideType):
        self.tileList.append(TileObject(string,surface,collides,collideType))

    def updateButtons(self,player):
        for button in self.buttonList:
            button.checkCollision(player)
            button.update()

    def updateLevers(self,player):
        for lever in self.leverList:
            lever.checkCollision(player)
            lever.update()
    
    def render(self):
        minRow=int(self.windowTop//self.tileHeight)
        if minRow<0:
            minRow=0    
        maxRow=int((self.windowTop+self.windowHeight)//self.tileHeight)+1
        if maxRow>self.mapHeight:
            maxRow=self.mapHeight
        minCol=int(self.windowLeft//self.tileWidth)
        if minCol<0:
            minCol=0    
        maxCol=int((self.windowLeft+self.windowWidth)//self.tileWidth)+1
        if maxCol>self.mapWidth:
            maxCol=self.mapWidth
        for row in range(minRow,maxRow):
            for col in range(minCol,maxCol):
                pair=self.tileframe[row][col]
                if pair!="  ":
                    for tile in self.tileList:
                        worldX=col*self.tileWidth
                        worldY=row*self.tileHeight
                        screenX=worldX-self.windowLeft
                        screenY=worldY-self.windowTop
                        if tile.key == pair: 
                            self.ds.blit(tile.surface,(screenX,screenY))
                            break

    def checkTileCollision(self,x,y,width,height):
        minRow=int(y//self.tileHeight)
        if minRow<0:
            minRow=0    
        maxRow=int((y+height)//self.tileHeight)+1
        if maxRow>self.mapHeight:
            maxRow=self.mapHeight
        minCol=int(x//self.tileWidth)
        if minCol<0:
            minCol=0    
        maxCol=int((x+width)//self.tileWidth)+1
        if maxCol>self.mapWidth:
            maxCol=self.mapWidth
        collides = False
        collideTypeList=[]
        sourceRectangle=pygame.Rect(x,y,width,height)
        for row in range(minRow,maxRow):
            for col in range(minCol,maxCol):
                tileKey=self.tileframe[row][col]
                for tile in self.tileList:
                    if tile.key == tileKey:
                        if sourceRectangle.colliderect((col*self.tileWidth,row*self.tileHeight,self.tileWidth,self.tileHeight)):
                            if tile.collides:
                                collides = True
                            if tile.collideType not in collideTypeList:
                                    collideTypeList.append([row,col,tile.collideType])
                        break
        return collides,collideTypeList

    def loadTilesFromFile(self,filename):
        self.level = 1
        self.playerInfo = None
        self.blockInfoList = []
        self.tileList = []
        self.buttonList = []
        self.leverList = []
        self.gateList = []
        self.portalList = []
        fp = open(filename,"r")
        fileLines = fp.readlines()
        fp.close()
        mapString = ""
        for line in fileLines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            (lhs,rhs) = line.split("=")
            if lhs == "level":
                self.level = int(rhs)
            elif lhs == "mapWidth":
                self.mapWidth = int(rhs)
            elif lhs == "mapHeight":
                self.mapHeight = int(rhs)
            elif lhs == "tileWidth":
                self.tileWidth = int(rhs)
            elif lhs == "tileHeight":
                self.tileHeight = int(rhs)
            elif lhs == "textureFile":
                tileInfo = rhs.split(",")
                if tileInfo[2] == "True":
                    tileInfo[2] = True
                else:
                    tileInfo[2] = False
                if tileInfo[3] == "None":
                    tileInfo[3] = None
                self.addTile(*tileInfo)
            elif lhs == "activator":
                activatorInfo = rhs.split(",")
                activatorInfo[0] = int(activatorInfo[0])
                activatorInfo[1] = int(activatorInfo[1])
                if activatorInfo[2] == "True":
                    activatorInfo[2] = True
                else:
                    activatorInfo[2] = False
                if activatorInfo[7] == "button":
                    self.buttonList.append(Button(self,*activatorInfo[:7]))
                elif activatorInfo[7] == "lever":
                    self.leverList.append(Lever(self,*activatorInfo[:7]))
            elif lhs == "device":
                deviceInfo = rhs.split(",")
                deviceInfo[0] = int(deviceInfo[0])
                deviceInfo[1] = int(deviceInfo[1])
                if deviceInfo[2] == "True":
                    deviceInfo[2] = True
                else:
                    deviceInfo[2] = False
                if deviceInfo[6] == "gate":
                    self.gateList.append(Gate(self,*deviceInfo[:6]))
                elif deviceInfo[6] == "portal":
                    self.portalList.append(Portal(self,*deviceInfo[:6]))
            elif lhs == "playerStart":
                self.playerInfo = rhs.split(",")
            elif lhs == "block":
                self.blockInfoList.append(rhs.split(","))
            elif lhs == "mapLine":
                rhs = rhs.replace('"','')
                mapString += rhs + '\n'
        mapString = mapString.strip()
        mapLines = mapString.split("\n")
        self.tileframe = [None] * self.mapHeight
        for i in range(0,self.mapHeight):
            self.tileframe[i] = [None] * self.mapWidth        
        for row in range(0,self.mapHeight):
            for col in range(0,self.mapWidth):
                line = mapLines[row]
                pair = line[col*2:col*2+2]
                self.tileframe[row][col] = pair

    def saveTilesToFile(self,filename,player):
        fp=open(filename,"w")
        fp.write("level="+str(self.level)+"\n")
        fp.write("mapWidth="+str(self.mapWidth)+"\n")
        fp.write("mapHeight="+str(self.mapHeight)+"\n")
        fp.write("tileWidth="+str(self.tileWidth)+"\n")
        fp.write("tileHeight="+str(self.tileHeight)+"\n")
        for tile in self.tileList:
            fp.write("textureFile="+tile.key+","+tile.path+","+str(tile.collides)+","+str(tile.collideType)+"\n")
        for button in self.buttonList:
            fp.write("activator="+str(button.row)+","+str(button.col)+","+str(button.active)+","+button.key1+","+button.key2+","+button.device+","+str(button.pair)+",button\n")
        for lever in self.leverList:
            fp.write("activator="+str(lever.row)+","+str(lever.col)+","+str(lever.active)+","+lever.key1+","+lever.key2+","+lever.device+","+str(lever.pair)+",lever\n")
        for gate in self.gateList:
            fp.write("device="+str(gate.row)+","+str(gate.col)+","+str(gate.active)+","+gate.key1+","+gate.key2+","+gate.direction+",gate\n")
        for portal in self.portalList:
            fp.write("device="+str(portal.row)+","+str(portal.col)+","+str(portal.active)+","+portal.key1+","+portal.key2+","+portal.direction+",portal\n")
        fp.write("playerStart="+str(player.x)+","+str(player.y)+"\n")
        for block in player.blockList:
            fp.write("block="+str(block.x)+","+str(block.y)+"\n")
        for row in range(0,self.mapHeight):
            linestring=""
            for col in range(0,self.mapWidth):
                linestring+=self.tileframe[row][col]
            fp.write("mapLine="+linestring+"\n")
        fp.close()
        
    def renderObject(self,surface,worldX,worldY):
        screenX=worldX-self.windowLeft
        screenY=worldY-self.windowTop
        self.ds.blit(surface,(screenX,screenY))
        
        
