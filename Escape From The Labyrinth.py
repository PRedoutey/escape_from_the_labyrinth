#Main file - Escape from the Labyrinth
#Patrick Redoutey
#ETGG1802
#Lab 5
import pygame
import random
import tilemapModule
from entityModule import *

pygame.init()

ds = pygame.display.set_mode((800,608))
dsRect = pygame.Rect(0,0,800,608)

font = pygame.font.SysFont('Comic Sans', 32, True)

#create images for main menu
title = pygame.image.load("assets/titleScreen.jpg")
newGame1 = pygame.image.load("assets/newGame.png")
newGame2 = pygame.image.load("assets/newGameGlow.png")
newGameRect = pygame.Rect(230,358,340,87)
newGame = False
continue1 = pygame.image.load("assets/continue.png")
continue2 = pygame.image.load("assets/continueGlow.png")
continueRect = pygame.Rect(268,462,269,88)
continueGame = False

#main menu loop
fps_clock=pygame.time.Clock()
startup = True
while startup:
    fps_clock.tick(60)
    pygame.event.pump()
    keys=pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    #make "New Game" and "Continue" glow when hovered over
    if newGameRect.collidepoint(mx,my):
        newGameImage = newGame2
    else:
        newGameImage = newGame1
    if continueRect.collidepoint(mx,my):
        continueImage = continue2
    else:
        continueImage = continue1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startup = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                startup = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #select "New Game" or "Continue"
            if newGameImage == newGame2:
                startup = False
                newGame = True
            elif continueImage == continue2:
                startup = False
                continueGame = True
    ds.fill((0,0,0))
    ds.blit(title,(0,0))
    ds.blit(newGameImage,(230,358))
    ds.blit(continueImage,(268,462))
    pygame.display.update()

tilemap1 = tilemapModule.Tilemap(ds)

#load save file or level 1
if newGame:
    tilemap1.loadTilesFromFile(f"level1.txt")
    currentLevel = 1 
elif continueGame:
    tilemap1.loadTilesFromFile(f"saveFile.txt")
    currentLevel = tilemap1.level

#create text for tutorials or to indicate file saves
saveText = font.render("File saved.", False, (255,255,255))
saveTextTimer = 0
level1Text = font.render("Use WSAD to move.", False, (255,255,255))
level2Text = font.render("Use SPACE to interact with levers.", False, (255,255,255))
level3Text = font.render("Use R to restart level if stuck.", False, (255,255,255))
level4Text = font.render("Use Ctrl + S to save your progress.", False, (255,255,255))
level4Text2 = font.render("Your progress also saves automatically when you exit.", False, (255,255,255))

#load player sprite
playerSurfaces = []
playerSurfaces.append(pygame.image.load("assets/sprite/spriteLeft.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteRight.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteUp.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteDown.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteLeftUp.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteLeftDown.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteRightUp.png"))
playerSurfaces.append(pygame.image.load("assets/sprite/spriteRightDown.png"))

#game loop
gaming = True
while gaming:
    player = PlayerObject(ds,tilemap1,playerSurfaces,16,21)
    restart = False
    #level loop
    mainloop = True
    while mainloop:
        fps_clock.tick(120)
        pygame.event.pump()
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                gaming = False
            elif event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_LCTRL:
                    if keys[pygame.K_s]:
                        tilemap1.saveTilesToFile("saveFile.txt",player)
                        saveTextTimer = 120
                elif event.key == pygame.K_ESCAPE:
                    mainloop = False
                    gaming = False
                #restart level
                elif event.key == pygame.K_r:
                    mainloop = False
                    restart = True
                #flip lever
                elif event.key == pygame.K_SPACE:
                    tilemap1.updateLevers(player)
        #player/block movement
        player.direction = ""
        player.isMoving = False
        if keys[pygame.K_a]:
            player.moveLeft()
        elif keys[pygame.K_d]:
            player.moveRight()
        if keys[pygame.K_w]:
            player.moveUp()
        elif keys[pygame.K_s]:
            player.moveDown()
        player.update()
        player.updateBlocks()
        tilemap1.updateButtons(player)
        #end level if player not on screen
        if not dsRect.colliderect(player.x,player.y,player.width,player.height):
            mainloop = False
        #rendering
        ds.fill((0,0,0))
        tilemap1.render()
        player.render()
        player.renderBlocks()
        #render tutorial text depending on level
        if currentLevel == 1:
            ds.blit(level1Text,(128,128))
        elif currentLevel == 2:
            ds.blit(level2Text,(64,64))
        elif currentLevel == 3:
            ds.blit(level3Text,(64,64))
        elif currentLevel == 4:
            ds.blit(level4Text,(10,10))
            ds.blit(level4Text2,(10,52))
        #render save file text if saved recently
        if saveTextTimer > 0:
            ds.blit(saveText,(10,566))
            saveTextTimer -= 1
        pygame.display.update()

    #restart loop with current level
    if restart:
        tilemap1.loadTilesFromFile(f"level{currentLevel}.txt")
        continue
    #continue to next level
    if gaming:
        currentLevel += 1
        #break loop if past last level
        if currentLevel > 5:
            break
        tilemap1.loadTilesFromFile(f"level{currentLevel}.txt")

#save file if game is not beaten
if currentLevel <= 5:
    tilemap1.saveTilesToFile("saveFile.txt",player)
#display win screen
else:
    winScreen = pygame.image.load("assets/victoryScreen.jpg")
    ds.fill((0,0,0))
    ds.blit(winScreen,(0,0))
    pygame.display.update()
    #end program loop
    end = True
    while end:
        fps_clock.tick(30)
        pygame.event.pump()
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = False
    
pygame.display.quit()
