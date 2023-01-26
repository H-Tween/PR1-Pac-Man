from board import board
import pygame
import random

pygame.init()

WIDTH = 840
HEIGHT = 890

# Getting the height of every square from the board 
# Removing 50px from the bottom allowing score and powerUps to be displayed, 30 is height of board
height = ((HEIGHT - 50) // 30) 

# Getting the width of every square from the board, 28 is width of board 
width = ((WIDTH // 28)) 

# Setting size of screen
screen = pygame.display.set_mode([WIDTH, HEIGHT]) 

# Setting Font
font = pygame.font.SysFont("freesansbold.tff", 20)
largeFont = pygame.font.SysFont("freesansbold.tff", 40)
extraLargeFont = pygame.font.SysFont("freesansbold.tff", 85)

# Tracking time
timer = pygame.time.Clock()

# FPS for amount of executions per second ############
fps = 60

# Setting the game ending condition 
gameEnd = False

# Counter used to change pacman images to appear to animate as well as flicking of the powerUps
counter = 0
pacmanImages = []

endGameCounter = 0

# Setting initial postion of player
playerX = 10 # 10 13 453
playerY = 395 # 395 (scaling changed) 646

# Player lives
lives = 2

# Setting Initial position of ghosts
# Bottom Left
ghostX1 = 32
ghostY1 = 812
ghostDirection1 = 0
ghostAlive1 = True
ghostEaten1 = False

# Bottom Right
ghostX2 = 782
ghostY2 = 812
ghostDirection2 = 2
ghostAlive2 = True
ghostEaten2 = False

# Top Left
ghostX3 = 32
ghostY3 = 31
ghostDirection3 = 3
ghostAlive3 = True
ghostEaten3 = False

# Top Right
ghostX4 = 782
ghostY4 = 31
ghostDirection4 = 1
ghostAlive4 = True
ghostEaten4 = False

# Starting direction of player
direction = 0 

# Starting direction of player
directionChoice = 0 # pressing a key before pacman can move makes pacman turn in that direction when next available
padding = 0

flickering = True # allows the powerUps to appear to "flicker" so they are seperate from pellets
speed = 3 # speed that pacman moves (can be changed with a possible option menu)
ghostSpeed = 3

# R, L, U, D
possibleDirections = [False, False, False, False]
possibleGhostDirections1 = [False, False, False, False]
possibleGhostDirections2 = [False, False, False, False]
possibleGhostDirections3 = [False, False, False, False]
possibleGhostDirections4 = [False, False, False, False]

score = 0
powerUps = 0
powerUpCounter = 0
powerUpActive = False

moving = False # stops everything from moving in the beginning of the game
startUpCounter = 0


# displays each pacman image in order
for i in range(1, 4): 
    pacmanImages.append(pygame.transform.scale(pygame.image.load(f"images//pacman/P{i}.png"), (24, 24)))

ghost1 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
ghost2 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
ghost3 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
ghost4 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))

def drawBoard(board):
    for i in range(len(board)): # each row
        for j in range(len(board[i])): # each column in row

            circle = (j * width + (0.5 * width), i * height + (0.5 * height))
            x = width * j
            y = height * i

            # Draw pellets
            if board[i][j] == 1:
                pygame.draw.circle(screen, "white", circle, 4) 
            
            # Draw powerUps
            if board[i][j] == 2 and flickering == True:
                pygame.draw.circle(screen, "white", circle, 8)

            # Draw rectangle
            if board[i][j] == 3:
                pygame.draw.rect(screen, "red", (x, y, width + 2, height + 2)) # Outline of walls/squares
                pygame.draw.rect(screen, "blue", (x, y, width, height)) # Walls/squares
            
            # Draw line
            if board[i][j] == 4: 
                lineStart = (x, y + (0.5 * height)) # Start X and Y
                lineEnd = (x + width, y + (0.5 * height)) # End X and Y coordinates
                pygame.draw.line(screen, "white", lineStart, lineEnd, 3)

def drawScoreboardAndPowerUps(powerUps, padding, powerUpCounter):
    # Display score
    scoreText = font.render(f'Score: {score}', True, "white")
    screen.blit(scoreText, (5, 317)) 

    # Display PowerUps
    powerUpsText = font.render('PowerUps: ', True, "white")
    screen.blit(powerUpsText, (695, 317)) 

    # For every powerUp gained, the powerUp is drawn next to the display text, showing how many powerUps are available
    for i in range(powerUps):
        pygame.draw.circle(screen, "white", (775 + padding, 323), 8) # 506
        padding += 18

    # Testing
    # testText = font.render(f'PowerUps: {powerUps} and {powerUpCounter}', True, "white")
    # screen.blit(testText, (300, 500))

    # Display powerUp timer
    newPowerUpCounter = float(powerUpCounter / 60)
    roundedPowerUpCounter = format(newPowerUpCounter, '.1f')
    powerUpCounterText = font.render(f'PowerUpCounter: {roundedPowerUpCounter}', True, "white")
    screen.blit(powerUpCounterText, (695, 483)) 


def drawLives(lives):
    # Lives
    livesText = font.render('Lives: ', True, 'white')
    screen.blit(livesText, (5, 483))

    # Display Lives
    pacManLives = pygame.transform.scale(pygame.image.load(f"images//pacman/P1.png"), (24, 24))
    if lives == 2:
        screen.blit(pacManLives, (48, 477))
        screen.blit(pacManLives, (48 + 28, 477))
        screen.blit(pacManLives, (48 + 56, 477))
    elif lives == 1:
        screen.blit(pacManLives, (48, 477))
        screen.blit(pacManLives, (48 + 28, 477))
    elif lives == 0:
        screen.blit(pacManLives, (48, 477))
        
    # For loop caused the game to decrease in fps

    # for i in range(lives + 1): 
    #     pacManLives = pygame.transform.scale(pygame.image.load(f"images//pacman/P1.png"), (24, 24))
    #     screen.blit(pacManLives, (48 + padding, 477))
    #     padding += 28

def drawTrademark():
    # Displaying creators of game
    createdByText = font.render('Created By: ', True, "white")
    nameOneText = font.render('Harrison Tween & ', True, "white")
    nameTwoText = font.render('Aaron Temiwoluwa', True, "white")

    screen.blit(createdByText, (345, 385)) # + 15, + 15
    screen.blit(nameOneText, (360, 400))
    screen.blit(nameTwoText, (375, 415))

def drawStartGame(powerUpCounter):
    if powerUpCounter < 60: 
        startTimer = 3
    elif powerUpCounter < 120:
        startTimer = 2
    else:
        startTimer = 1
        
    startGameText = largeFont.render(f'Starting in: {startTimer}', True, 'white')
    screen.blit(startGameText, (330, 518))

def drawEndGame():
    if endGameFlickering == True:
        gameEndText = extraLargeFont.render('GAME OVER', True, 'white')
        screen.blit(gameEndText, (235, 200))
    exitGameFont = largeFont.render('Please Exit', True, 'white')
    screen.blit(exitGameFont, (345, 518))
    

def drawPacman(playerX, playerY):
    # Right, left, up, down
    imageCounter = counter // 8

    # Change direction pacman faces

    # If facing right
    if direction == 0:
        screen.blit(pacmanImages[imageCounter], (playerX, playerY)) 

    # If facing left
    elif direction == 1:
        screen.blit(pygame.transform.flip(pacmanImages[imageCounter], True, False), (playerX, playerY))

    # If facing up
    elif direction == 2:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], 90), (playerX, playerY))

    # If facing down
    elif direction == 3:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], -90), (playerX, playerY))

def drawGhost(ghostX, ghostY, ghostDirection, ghost):
    
    ghostCenterX = ghostX + 13
    ghostCenterY = ghostY + 13

    # ghostRec = pygame.draw.rect(screen, "red", (ghostCenterX - 13, ghostCenterY - 13, 25, 25))
    ghostHitbox = pygame.rect.Rect((ghostCenterX - 13, ghostCenterY - 13), (25, 25))
    # If facing right
    if ghostDirection == 0 or ghostDirection == 2:
        screen.blit(ghost, (ghostX, ghostY)) 

    # If facing left
    elif ghostDirection == 1 or ghostDirection == 3:
        screen.blit(pygame.transform.flip(ghost, True, False), (ghostX, ghostY))

    return ghostHitbox

def positionCheck(playerCenterX, playerCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleDirections = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [12, 18] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (playerCenterX // 28) < 29:

        # Checking collision for up and down

        if direction == 2 or direction == 3: # if going up or down
            if gridCenter[0] <= playerCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(playerCenterY + factor) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[3] = True # opposite direction

                if board[(playerCenterY - factor) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[2] = True # opposite direction
            
            if gridCenter[0] <= playerCenterY % height <= gridCenter[1]:
                if board[playerCenterY // height][(playerCenterX - width) // width] < 3: # if square next to is free 
                    possibleDirections[1] = True # opposite direction
               
                if board[playerCenterY // height][(playerCenterX + width) // width] < 3: # if square next to is free 
                    possibleDirections[0] = True # opposite direction

        # Checking collision for left and right

        if direction == 0 or direction == 1: # if going right or left
            if gridCenter[0] <= playerCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(playerCenterY + height) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[3] = True # opposite direction

                if board[(playerCenterY - height) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[2] = True # opposite direction
            
            if gridCenter[0] <= playerCenterY % height <= gridCenter[1]:
                if board[playerCenterY // height][(playerCenterX - factor) // width] < 3: # if square next to is free 
                    possibleDirections[1] = True # opposite direction
               
                if board[playerCenterY // height][(playerCenterX + factor) // width] < 3: # if square next to is free 
                    possibleDirections[0] = True # opposite direction
    
    else:
        possibleDirections[0] = True
        possibleDirections[1] = True

    return possibleDirections

def positionCheckGhost1(ghostCenterX, ghostCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleGhostDirections1 = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [13, 17] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (ghostCenterX // 28) < 29:

        # Checking collision for up and down

        number = ghostCenterX % width

        if ghostDirection1 == 2 or ghostDirection1 == 3: # if going up or down
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections1[3] = True # opposite direction

                if board[(ghostCenterY - factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections1[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - width) // width] < 3: # if square next to is free 
                    possibleGhostDirections1[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + width) // width] < 3: # if square next to is free 
                    possibleGhostDirections1[0] = True # opposite direction
            
            # If ghost is in the box, moving up is true. When reaching the top wall, moving left and right is true
            if ghostCenterX % width == 13 and ghostCenterX == 403 and ghostCenterY <= 413 and ghostCenterY > 322 and powerUpCounter == 0:
                if ghostCenterY <= 413:
                    possibleGhostDirections1 = [False, False, True, False]
                    if ghostCenterY <= 323:
                        possibleGhostDirections1 = [True, True, False, False]
                        return possibleGhostDirections1

        # Checking collision for left and right
        num = ghostCenterX % height
        if ghostDirection1 == 0 or ghostDirection1 == 1: # if going right or left
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections1[3] = True # opposite direction

                if board[(ghostCenterY - height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections1[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections1[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections1[0] = True # opposite direction
    
    else:
        possibleGhostDirections1[0] = True
        possibleGhostDirections1[1] = True

    return possibleGhostDirections1

def positionCheckGhost2(ghostCenterX, ghostCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleGhostDirections2 = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [13, 17] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (ghostCenterX // 28) < 29:

        # Checking collision for up and down

        number = ghostCenterX % width

        if ghostDirection2 == 2 or ghostDirection2 == 3: # if going up or down
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections2[3] = True # opposite direction

                if board[(ghostCenterY - factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections2[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - width) // width] < 3: # if square next to is free 
                    possibleGhostDirections2[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + width) // width] < 3: # if square next to is free 
                    possibleGhostDirections2[0] = True # opposite direction
            
            # If ghost is in the box, moving up is true. When reaching the top wall, moving left and right is true
            if ghostCenterX % width == 13 and ghostCenterX == 403 and ghostCenterY <= 413 and ghostCenterY > 322 and powerUpCounter == 0:
                if ghostCenterY <= 413:
                    possibleGhostDirections2 = [False, False, True, False]
                    if ghostCenterY <= 323:
                        possibleGhostDirections2 = [True, True, False, False]
                        return possibleGhostDirections2

        # Checking collision for left and right
        num = ghostCenterX % height
        if ghostDirection2 == 0 or ghostDirection2 == 1: # if going right or left
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections2[3] = True # opposite direction

                if board[(ghostCenterY - height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections2[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections2[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections2[0] = True # opposite direction
    
    else:
        possibleGhostDirections2[0] = True
        possibleGhostDirections2[1] = True

    return possibleGhostDirections2

def positionCheckGhost3(ghostCenterX, ghostCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleGhostDirections3 = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [13, 17] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (ghostCenterX // 28) < 29:

        # Checking collision for up and down

        number = ghostCenterX % width

        if ghostDirection3 == 2 or ghostDirection3 == 3: # if going up or down
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections3[3] = True # opposite direction

                if board[(ghostCenterY - factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections3[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - width) // width] < 3: # if square next to is free 
                    possibleGhostDirections3[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + width) // width] < 3: # if square next to is free 
                    possibleGhostDirections3[0] = True # opposite direction
            
            # If ghost is in the box, moving up is true. When reaching the top wall, moving left and right is true
            if ghostCenterX % width == 13 and ghostCenterX == 403 and ghostCenterY <= 413 and ghostCenterY > 322 and powerUpCounter == 0:
                if ghostCenterY <= 413:
                    possibleGhostDirections3 = [False, False, True, False]
                    if ghostCenterY <= 323:
                        possibleGhostDirections3 = [True, True, False, False]
                        return possibleGhostDirections3

        # Checking collision for left and right
        num = ghostCenterX % height
        if ghostDirection3 == 0 or ghostDirection3 == 1: # if going right or left
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections3[3] = True # opposite direction

                if board[(ghostCenterY - height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections3[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections3[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections3[0] = True # opposite direction
    
    else:
        possibleGhostDirections3[0] = True
        possibleGhostDirections3[1] = True

    return possibleGhostDirections3

def positionCheckGhost4(ghostCenterX, ghostCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleGhostDirections4 = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [13, 17] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (ghostCenterX // 28) < 29:

        # Checking collision for up and down

        number = ghostCenterX % width

        if ghostDirection4 == 2 or ghostDirection4 == 3: # if going up or down
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections4[3] = True # opposite direction

                if board[(ghostCenterY - factor) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections4[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - width) // width] < 3: # if square next to is free 
                    possibleGhostDirections4[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + width) // width] < 3: # if square next to is free 
                    possibleGhostDirections4[0] = True # opposite direction
            
            # If ghost is in the box, moving up is true. When reaching the top wall, moving left and right is true
            if ghostCenterX % width == 13 and ghostCenterX == 403 and ghostCenterY <= 413 and ghostCenterY > 322 and powerUpCounter == 0:
                if ghostCenterY <= 413:
                    possibleGhostDirections4 = [False, False, True, False]
                    if ghostCenterY <= 323:
                        possibleGhostDirections4 = [True, True, False, False]
                        return possibleGhostDirections4

        # Checking collision for left and right
        num = ghostCenterX % height
        if ghostDirection4 == 0 or ghostDirection4 == 1: # if going right or left
            if gridCenter[0] <= ghostCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(ghostCenterY + height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections4[3] = True # opposite direction

                if board[(ghostCenterY - height) // height][ghostCenterX // width] < 3: # if square below/above is free 
                    possibleGhostDirections4[2] = True # opposite direction
            
            if gridCenter[0] <= ghostCenterY % height <= gridCenter[1]:
                if board[ghostCenterY // height][(ghostCenterX - factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections4[1] = True # opposite direction
               
                if board[ghostCenterY // height][(ghostCenterX + factor) // width] < 3: # if square next to is free 
                    possibleGhostDirections4[0] = True # opposite direction
    
    else:
        possibleGhostDirections4[0] = True
        possibleGhostDirections4[1] = True

    return possibleGhostDirections4

def checkPelletsAndPowerUps(score, powerUps, powerUpActive):
    if 0 < playerX < 810: # only do check if inside the board otherwise an error is thrown as it cannot check for squares outside the board
        if board[playerCenterY // height][playerCenterX // width] == 1: # If player is on a pellet
            board[playerCenterY // height][playerCenterX // width] = 0 # Remove pellet
            score += 10
        if board[playerCenterY // height][playerCenterX // width] == 2: # If player is on a powerUp
            board[playerCenterY // height][playerCenterX // width] = 0 # Remove powerUp
            score += 50
            powerUps += 1

    return score, powerUps, powerUpActive

def movePlayer(playerX, playerY):
    # R, L, U, D

    # Move player
    if direction == 0 and possibleDirection[0] == True:
        playerX += speed
    elif direction == 1 and possibleDirection[1] == True:
        playerX -= speed
    elif direction == 2 and possibleDirection[2] == True:
        playerY -= speed
    elif direction == 3 and possibleDirection[3] == True:
        playerY += speed
    return playerX, playerY

def moveGhost1(ghostX1, ghostY1, ghostDirection1):
    # R, L, U, D

    # Every True False combination excluding FFF
    # TTT
    # TFT
    # TTF
    # TFF
    # FTF
    # FTT
    # FFT

    choice = random.randint(1,8)

    if ghostDirection1 == 0:
        if (possibleGhostDirection1[2] == True or possibleGhostDirection1[3] == True) and choice == 1:
            if possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[2] == True:
                ghostDirection1 = 2
                ghostY1 -= ghostSpeed
            elif possibleGhostDirection1[3] == True:
                ghostDirection1 = 3
                ghostY1 += ghostSpeed

        elif possibleGhostDirection1[0] == True:
            ghostX1 += ghostSpeed
        elif possibleGhostDirection1[0] == False:
            if possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice != 4:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice != 4:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == False:
                ghostDirection1 = 1
                ghostX1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == False:
                ghostDirection1 = 2
                ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == True:
                ghostDirection1 = 3
                ghostY1 += ghostSpeed

                #

    elif ghostDirection1 == 1:
        if (possibleGhostDirection1[2] == True or possibleGhostDirection1[3] == True) and choice == 1:
            if possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[2] == True:
                ghostDirection1 = 2
                ghostY1 -= ghostSpeed
            elif possibleGhostDirection1[3] == True:
                ghostDirection1 = 3
                ghostY1 += ghostSpeed

        elif possibleGhostDirection1[1] == True:
            ghostX1 -= ghostSpeed
        elif possibleGhostDirection1[1] == False:
            if possibleGhostDirection1[0] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[0] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed
                elif choice != 4:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[0] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed
                elif choice != 4:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[0] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == False:
                ghostDirection1 = 0
                ghostX1 += ghostSpeed

            elif possibleGhostDirection1[0] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == False:
                ghostDirection1 = 2
                ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[0] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[0] == False and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == True:
                ghostDirection1 = 3
                ghostY1 += ghostSpeed

                #

    elif ghostDirection1 == 2:
        if (possibleGhostDirection1[0] == True or possibleGhostDirection1[1] == True) and choice == 1:
            if possibleGhostDirection1[0] == True and possibleGhostDirection1[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[0] == True:
                ghostDirection1 = 0
                ghostX1 += ghostSpeed
            elif possibleGhostDirection1[1] == True:
                ghostDirection1 = 1
                ghostX1 -= ghostSpeed

        elif possibleGhostDirection1[2] == True:
            ghostY1 -= ghostSpeed
        elif possibleGhostDirection1[2] == False:
            if possibleGhostDirection1[1] == True and possibleGhostDirection1[0] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[0] == False and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 4:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[0] == True and possibleGhostDirection1[3] == False:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[0] == False and possibleGhostDirection1[3] == False:
                ghostDirection1 = 1
                ghostX1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[0] == True and possibleGhostDirection1[3] == False:
                ghostDirection1 = 0
                ghostX1 += ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[0] == True and possibleGhostDirection1[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection1 = 3
                    ghostY1 += ghostSpeed
                elif choice != 4:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == False and possibleGhostDirection1[3] == True:
                ghostDirection1 = 3
                ghostY1 += ghostSpeed

    elif ghostDirection1 == 3:
        if (possibleGhostDirection1[0] == True or possibleGhostDirection1[1] == True) and choice == 1:
            if possibleGhostDirection1[0] == True and possibleGhostDirection1[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[0] == True:
                ghostDirection1 = 0
                ghostX1 += ghostSpeed
            elif possibleGhostDirection1[1] == True:
                ghostDirection1 = 1
                ghostX1 -= ghostSpeed

        elif possibleGhostDirection1[3] == True:
            ghostY1 += ghostSpeed
        elif possibleGhostDirection1[3] == False:
            if possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[0] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[0] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 2:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == True and possibleGhostDirection1[0] == False:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection1 = 1
                    ghostX1 -= ghostSpeed
                elif choice == 4:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == True and possibleGhostDirection1[2] == False and possibleGhostDirection1[0] == False:
                ghostDirection1 = 1
                ghostX1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[0] == False:
                ghostDirection1 = 2
                ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == True and possibleGhostDirection1[0] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection1 = 0
                    ghostX1 += ghostSpeed
                elif choice == 4:
                    ghostDirection1 = 2
                    ghostY1 -= ghostSpeed

            elif possibleGhostDirection1[1] == False and possibleGhostDirection1[2] == False and possibleGhostDirection1[0] == True:
                ghostDirection1 = 0
                ghostX1 += ghostSpeed
    
    if ghostX1 < -30:
        ghostX1 = 900
    elif ghostX1 > 900:
        ghostX1 = -30
    return ghostX1, ghostY1, ghostDirection1

def moveGhost2(ghostX2, ghostY2, ghostDirection2):
    # R, L, U, D

    # Every True False combination excluding FFF
    # TTT
    # TFT
    # TTF
    # TFF
    # FTF
    # FTT
    # FFT

    choice = random.randint(1,8)

    if ghostDirection2 == 0:
        if (possibleGhostDirection2[2] == True or possibleGhostDirection2[3] == True) and choice == 1:
            if possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[2] == True:
                ghostDirection2 = 2
                ghostY2 -= ghostSpeed
            elif possibleGhostDirection2[3] == True:
                ghostDirection2 = 3
                ghostY2 += ghostSpeed

        elif possibleGhostDirection2[0] == True:
            ghostX2 += ghostSpeed
        elif possibleGhostDirection2[0] == False:
            if possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice != 4:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice != 4:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == False:
                ghostDirection2 = 1
                ghostX2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == False:
                ghostDirection2 = 2
                ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == True:
                ghostDirection2 = 3
                ghostY2 += ghostSpeed

                #

    elif ghostDirection2 == 1:
        if (possibleGhostDirection2[2] == True or possibleGhostDirection2[3] == True) and choice == 1:
            if possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[2] == True:
                ghostDirection2 = 2
                ghostY2 -= ghostSpeed
            elif possibleGhostDirection2[3] == True:
                ghostDirection2 = 3
                ghostY2 += ghostSpeed

        elif possibleGhostDirection2[1] == True:
            ghostX2 -= ghostSpeed
        elif possibleGhostDirection2[1] == False:
            if possibleGhostDirection2[0] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[0] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed
                elif choice != 4:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[0] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed
                elif choice != 4:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[0] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == False:
                ghostDirection2 = 0
                ghostX2 += ghostSpeed

            elif possibleGhostDirection2[0] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == False:
                ghostDirection2 = 2
                ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[0] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[0] == False and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == True:
                ghostDirection2 = 3
                ghostY2 += ghostSpeed

                #

    elif ghostDirection2 == 2:
        if (possibleGhostDirection2[0] == True or possibleGhostDirection2[1] == True) and choice == 1:
            if possibleGhostDirection2[0] == True and possibleGhostDirection2[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[0] == True:
                ghostDirection2 = 0
                ghostX2 += ghostSpeed
            elif possibleGhostDirection2[1] == True:
                ghostDirection2 = 1
                ghostX2 -= ghostSpeed

        elif possibleGhostDirection2[2] == True:
            ghostY2 -= ghostSpeed
        elif possibleGhostDirection2[2] == False:
            if possibleGhostDirection2[1] == True and possibleGhostDirection2[0] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[0] == False and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 4:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[0] == True and possibleGhostDirection2[3] == False:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[0] == False and possibleGhostDirection2[3] == False:
                ghostDirection2 = 1
                ghostX2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[0] == True and possibleGhostDirection2[3] == False:
                ghostDirection2 = 0
                ghostX2 += ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[0] == True and possibleGhostDirection2[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection2 = 3
                    ghostY2 += ghostSpeed
                elif choice != 4:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == False and possibleGhostDirection2[3] == True:
                ghostDirection2 = 3
                ghostY2 += ghostSpeed

    elif ghostDirection2 == 3:
        if (possibleGhostDirection2[0] == True or possibleGhostDirection2[1] == True) and choice == 1:
            if possibleGhostDirection2[0] == True and possibleGhostDirection2[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[0] == True:
                ghostDirection2 = 0
                ghostX2 += ghostSpeed
            elif possibleGhostDirection2[1] == True:
                ghostDirection2 = 1
                ghostX2 -= ghostSpeed

        elif possibleGhostDirection2[3] == True:
            ghostY2 += ghostSpeed
        elif possibleGhostDirection2[3] == False:
            if possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[0] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[0] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 2:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == True and possibleGhostDirection2[0] == False:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection2 = 1
                    ghostX2 -= ghostSpeed
                elif choice == 4:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == True and possibleGhostDirection2[2] == False and possibleGhostDirection2[0] == False:
                ghostDirection2 = 1
                ghostX2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[0] == False:
                ghostDirection2 = 2
                ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == True and possibleGhostDirection2[0] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection2 = 0
                    ghostX2 += ghostSpeed
                elif choice == 4:
                    ghostDirection2 = 2
                    ghostY2 -= ghostSpeed

            elif possibleGhostDirection2[1] == False and possibleGhostDirection2[2] == False and possibleGhostDirection2[0] == True:
                ghostDirection2 = 0
                ghostX2 += ghostSpeed
    
    if ghostX2 < -30:
        ghostX2 = 900
    elif ghostX2 > 900:
        ghostX2 = -30
    return ghostX2, ghostY2, ghostDirection2

def moveGhost3(ghostX3, ghostY3, ghostDirection3):
    # R, L, U, D

    # Every True False combination excluding FFF
    # TTT
    # TFT
    # TTF
    # TFF
    # FTF
    # FTT
    # FFT

    choice = random.randint(1,8)

    if ghostDirection3 == 0:
        if (possibleGhostDirection3[2] == True or possibleGhostDirection3[3] == True) and choice == 1:
            if possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[2] == True:
                ghostDirection3 = 2
                ghostY3 -= ghostSpeed
            elif possibleGhostDirection3[3] == True:
                ghostDirection3 = 3
                ghostY3 += ghostSpeed

        elif possibleGhostDirection3[0] == True:
            ghostX3 += ghostSpeed
        elif possibleGhostDirection3[0] == False:
            if possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice != 4:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice != 4:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == False:
                ghostDirection3 = 1
                ghostX3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == False:
                ghostDirection3 = 2
                ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == True:
                ghostDirection3 = 3
                ghostY3 += ghostSpeed

                #

    elif ghostDirection3 == 1:
        if (possibleGhostDirection3[2] == True or possibleGhostDirection3[3] == True) and choice == 1:
            if possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[2] == True:
                ghostDirection3 = 2
                ghostY3 -= ghostSpeed
            elif possibleGhostDirection3[3] == True:
                ghostDirection3 = 3
                ghostY3 += ghostSpeed

        elif possibleGhostDirection3[1] == True:
            ghostX3 -= ghostSpeed
        elif possibleGhostDirection3[1] == False:
            if possibleGhostDirection3[0] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[0] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed
                elif choice != 4:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[0] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed
                elif choice != 4:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[0] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == False:
                ghostDirection3 = 0
                ghostX3 += ghostSpeed

            elif possibleGhostDirection3[0] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == False:
                ghostDirection3 = 2
                ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[0] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[0] == False and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == True:
                ghostDirection3 = 3
                ghostY3 += ghostSpeed

                #

    elif ghostDirection3 == 2:
        if (possibleGhostDirection3[0] == True or possibleGhostDirection3[1] == True) and choice == 1:
            if possibleGhostDirection3[0] == True and possibleGhostDirection3[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[0] == True:
                ghostDirection3 = 0
                ghostX3 += ghostSpeed
            elif possibleGhostDirection3[1] == True:
                ghostDirection3 = 1
                ghostX3 -= ghostSpeed

        elif possibleGhostDirection3[2] == True:
            ghostY3 -= ghostSpeed
        elif possibleGhostDirection3[2] == False:
            if possibleGhostDirection3[1] == True and possibleGhostDirection3[0] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[0] == False and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 4:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[0] == True and possibleGhostDirection3[3] == False:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[0] == False and possibleGhostDirection3[3] == False:
                ghostDirection3 = 1
                ghostX3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[0] == True and possibleGhostDirection3[3] == False:
                ghostDirection3 = 0
                ghostX3 += ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[0] == True and possibleGhostDirection3[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection3 = 3
                    ghostY3 += ghostSpeed
                elif choice != 4:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == False and possibleGhostDirection3[3] == True:
                ghostDirection3 = 3
                ghostY3 += ghostSpeed

    elif ghostDirection3 == 3:
        if (possibleGhostDirection3[0] == True or possibleGhostDirection3[1] == True) and choice == 1:
            if possibleGhostDirection3[0] == True and possibleGhostDirection3[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[0] == True:
                ghostDirection3 = 0
                ghostX3 += ghostSpeed
            elif possibleGhostDirection3[1] == True:
                ghostDirection3 = 1
                ghostX3 -= ghostSpeed

        elif possibleGhostDirection3[3] == True:
            ghostY3 += ghostSpeed
        elif possibleGhostDirection3[3] == False:
            if possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[0] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[0] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 2:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == True and possibleGhostDirection3[0] == False:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection3 = 1
                    ghostX3 -= ghostSpeed
                elif choice == 4:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == True and possibleGhostDirection3[2] == False and possibleGhostDirection3[0] == False:
                ghostDirection3 = 1
                ghostX3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[0] == False:
                ghostDirection3 = 2
                ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == True and possibleGhostDirection3[0] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection3 = 0
                    ghostX3 += ghostSpeed
                elif choice == 4:
                    ghostDirection3 = 2
                    ghostY3 -= ghostSpeed

            elif possibleGhostDirection3[1] == False and possibleGhostDirection3[2] == False and possibleGhostDirection3[0] == True:
                ghostDirection3 = 0
                ghostX3 += ghostSpeed
    
    if ghostX3 < -30:
        ghostX3 = 900
    elif ghostX3 > 900:
        ghostX3 = -30
    return ghostX3, ghostY3, ghostDirection3

def moveGhost4(ghostX4, ghostY4, ghostDirection4):
    # R, L, U, D

    # Every True False combination excluding FFF
    # TTT
    # TFT
    # TTF
    # TFF
    # FTF
    # FTT
    # FFT

    choice = random.randint(1,8)

    if ghostDirection4 == 0:
        if (possibleGhostDirection4[2] == True or possibleGhostDirection4[3] == True) and choice == 1:
            if possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[2] == True:
                ghostDirection4 = 2
                ghostY4 -= ghostSpeed
            elif possibleGhostDirection4[3] == True:
                ghostDirection4 = 3
                ghostY4 += ghostSpeed

        elif possibleGhostDirection4[0] == True:
            ghostX4 += ghostSpeed
        elif possibleGhostDirection4[0] == False:
            if possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice != 4:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice != 4:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == False:
                ghostDirection4 = 1
                ghostX4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == False:
                ghostDirection4 = 2
                ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == True:
                ghostDirection4 = 3
                ghostY4 += ghostSpeed

                #

    elif ghostDirection4 == 1:
        if (possibleGhostDirection4[2] == True or possibleGhostDirection4[3] == True) and choice == 1:
            if possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[2] == True:
                ghostDirection4 = 2
                ghostY4 -= ghostSpeed
            elif possibleGhostDirection4[3] == True:
                ghostDirection4 = 3
                ghostY4 += ghostSpeed

        elif possibleGhostDirection4[1] == True:
            ghostX4 -= ghostSpeed
        elif possibleGhostDirection4[1] == False:
            if possibleGhostDirection4[0] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[0] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed
                elif choice != 4:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[0] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == False:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed
                elif choice != 4:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[0] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == False:
                ghostDirection4 = 0
                ghostX4 += ghostSpeed

            elif possibleGhostDirection4[0] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == False:
                ghostDirection4 = 2
                ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[0] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[0] == False and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == True:
                ghostDirection4 = 3
                ghostY4 += ghostSpeed

                #

    elif ghostDirection4 == 2:
        if (possibleGhostDirection4[0] == True or possibleGhostDirection4[1] == True) and choice == 1:
            if possibleGhostDirection4[0] == True and possibleGhostDirection4[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[0] == True:
                ghostDirection4 = 0
                ghostX4 += ghostSpeed
            elif possibleGhostDirection4[1] == True:
                ghostDirection4 = 1
                ghostX4 -= ghostSpeed

        elif possibleGhostDirection4[2] == True:
            ghostY4 -= ghostSpeed
        elif possibleGhostDirection4[2] == False:
            if possibleGhostDirection4[1] == True and possibleGhostDirection4[0] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[0] == False and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 4:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[0] == True and possibleGhostDirection4[3] == False:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[0] == False and possibleGhostDirection4[3] == False:
                ghostDirection4 = 1
                ghostX4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[0] == True and possibleGhostDirection4[3] == False:
                ghostDirection4 = 0
                ghostX4 += ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[0] == True and possibleGhostDirection4[3] == True:
                choice = random.randint(1, 8)
                if choice == 4:
                    ghostDirection4 = 3
                    ghostY4 += ghostSpeed
                elif choice != 4:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == False and possibleGhostDirection4[3] == True:
                ghostDirection4 = 3
                ghostY4 += ghostSpeed

    elif ghostDirection4 == 3:
        if (possibleGhostDirection4[0] == True or possibleGhostDirection4[1] == True) and choice == 1:
            if possibleGhostDirection4[0] == True and possibleGhostDirection4[1] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[0] == True:
                ghostDirection4 = 0
                ghostX4 += ghostSpeed
            elif possibleGhostDirection4[1] == True:
                ghostDirection4 = 1
                ghostX4 -= ghostSpeed

        elif possibleGhostDirection4[3] == True:
            ghostY4 += ghostSpeed
        elif possibleGhostDirection4[3] == False:
            if possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[0] == True:
                choice = random.randint(1, 5)
                if choice == 3:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif 1 >= choice <= 2:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed
                elif 4 >= choice <= 5:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[0] == True:
                choice = random.randint(1, 2)
                if choice == 1:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 2:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == True and possibleGhostDirection4[0] == False:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection4 = 1
                    ghostX4 -= ghostSpeed
                elif choice == 4:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == True and possibleGhostDirection4[2] == False and possibleGhostDirection4[0] == False:
                ghostDirection4 = 1
                ghostX4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[0] == False:
                ghostDirection4 = 2
                ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == True and possibleGhostDirection4[0] == True:
                choice = random.randint(1, 8)
                if choice != 4:
                    ghostDirection4 = 0
                    ghostX4 += ghostSpeed
                elif choice == 4:
                    ghostDirection4 = 2
                    ghostY4 -= ghostSpeed

            elif possibleGhostDirection4[1] == False and possibleGhostDirection4[2] == False and possibleGhostDirection4[0] == True:
                ghostDirection4 = 0
                ghostX4 += ghostSpeed
    
    if ghostX4 < -30:
        ghostX4 = 900
    elif ghostX4 > 900:
        ghostX4 = -30
    return ghostX4, ghostY4, ghostDirection4
    

def activatePowerUp(powerUps, ghostDirection1, ghostDirection2, ghostDirection3, ghostDirection4):
    powerUpActive = True
    powerUps -= 1
    powerUpCounter = 0
    if ghostDirection1 == 0:
        ghostDirection1 = 1
    elif ghostDirection1 == 1:
        ghostDirection1 = 0
    elif ghostDirection1 == 2:
        ghostDirection1 = 3
    elif ghostDirection1 == 3:
        ghostDirection1 = 2

    if ghostDirection2 == 0:
        ghostDirection2 = 1
    elif ghostDirection2 == 1:
        ghostDirection2 = 0
    elif ghostDirection2 == 2:
        ghostDirection2 = 3
    elif ghostDirection2 == 3:
        ghostDirection2 = 2

    if ghostDirection3 == 0:
        ghostDirection3 = 1
    elif ghostDirection3 == 1:
        ghostDirection3 = 0
    elif ghostDirection3 == 2:
        ghostDirection3 = 3
    elif ghostDirection3 == 3:
        ghostDirection3 = 2

    if ghostDirection4 == 0:
        ghostDirection4 = 1
    elif ghostDirection4 == 1:
        ghostDirection4 = 0
    elif ghostDirection4 == 2:
        ghostDirection4 = 3
    elif ghostDirection4 == 3:
        ghostDirection4 = 2
    

    return powerUps, powerUpActive, powerUpCounter, ghostDirection1, ghostDirection2, ghostDirection3, ghostDirection4


run = True

while run:
    timer.tick(fps)

    # For iterating though pacman images and flickering of powerUps
    if counter < 23:
        counter += 1
        if counter > 12:
            flickering = True

    else:
        counter = 0 # Reset counter to start at first pacman image
        flickering = False # Turning flickering off to make powerUp disappear briefly to simulate flickering

    # Flickering of game ending screen
    if endGameCounter < 60:
        endGameCounter += 1
        if (endGameCounter >= 0 and endGameCounter <= 40):
            endGameFlickering = True
        else:
            endGameFlickering = False 

    else:
        endGameCounter = 0 
        endGameFlickering = False 


    # Game Start Up
    if startUpCounter < 180:
        moving = False
        # Game Start
        startUpCounter += 1
    elif gameEnd == True:
        moving == False
        # Game over
    else:
        moving = True

    if powerUpActive == True and powerUpCounter < 600: # If powerUp is active and has been active for less than 10 seconds
        powerUpCounter += 1
    elif powerUpActive == True and powerUpCounter >= 600: # If powerUp is active but has been active for 10 or more seconds
        powerUpCounter = 0
        powerUpActive = False

    screen.fill("black")
    drawBoard(board)

    playerCenterX = playerX + 13 # Center x coordinate of player
    playerCenterY = playerY + 13 # Center y coordinate of player

    ghostCenterX1 = ghostX1 + 13
    ghostCenterY1 = ghostY1 + 13

    ghostCenterX2 = ghostX2 + 13
    ghostCenterY2 = ghostY2 + 13

    ghostCenterX3 = ghostX3 + 13
    ghostCenterY3 = ghostY3 + 13

    ghostCenterX4 = ghostX4 + 13
    ghostCenterY4 = ghostY4 + 13

    playerHitbox = pygame.draw.circle(screen, "black", (playerCenterX, playerCenterY), 11, 2)
    drawPacman(playerX, playerY)
    drawTrademark()

    ghostHitbox1 = drawGhost(ghostX1, ghostY1, ghostDirection1, ghost1)
    ghostHitbox2 = drawGhost(ghostX2, ghostY2, ghostDirection2, ghost2)
    ghostHitbox3 = drawGhost(ghostX3, ghostY3, ghostDirection3, ghost3)
    ghostHitbox4 = drawGhost(ghostX4, ghostY4, ghostDirection4, ghost4)
    drawScoreboardAndPowerUps(powerUps, padding, powerUpCounter)
    drawLives(lives)

    if startUpCounter < 180:
        drawStartGame(startUpCounter)

    if gameEnd == True:
        drawEndGame()

    # Testing
    # pygame.draw.circle(screen, "white", (playerCenterX, playerCenterY), 2)
    # pygame.draw.circle(screen, "white", (ghostCenterX1, ghostCenterY1), 2)
    # pygame.draw.circle(screen, "pink", (ghostCenterX2, ghostCenterY2), 2)
    # pygame.draw.circle(screen, "green", (ghostCenterX3, ghostCenterY3), 2)
    # pygame.draw.circle(screen, "yellow", (ghostCenterX4, ghostCenterY4), 2)

    possibleDirection = positionCheck(playerCenterX, playerCenterY)

    possibleGhostDirection1 = positionCheckGhost1(ghostCenterX1, ghostCenterY1)
    possibleGhostDirection2 = positionCheckGhost2(ghostCenterX2, ghostCenterY2)
    possibleGhostDirection3 = positionCheckGhost3(ghostCenterX3, ghostCenterY3)
    possibleGhostDirection4 = positionCheckGhost4(ghostCenterX4, ghostCenterY4)

    if moving == True:
        playerX, playerY = movePlayer(playerX, playerY)

        if ghostAlive1 == False:
            if powerUpCounter == 0:
                ghostAlive1 = True
                ghostEaten1 = False
        if ghostAlive2 == False:
            if powerUpCounter == 0:
                ghostAlive2 = True
                ghostEaten2 = False
        if ghostAlive3 == False:
            if powerUpCounter == 0:
                ghostAlive3 = True
                ghostEaten3 = False
        if ghostAlive4 == False:
            if powerUpCounter == 0:
                ghostAlive4 = True
                ghostEaten4 = False
                

        # If powerup not active
        if powerUpActive != True and powerUpCounter == 0:
            ghost1 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
            ghost2 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
            ghost3 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))
            ghost4 = pygame.transform.scale(pygame.image.load(f"images//ghosts/ghost.png"), (24, 24))

            ghostSpeed = 3

            ghostX1, ghostY1, ghostDirection1 = moveGhost1(ghostX1, ghostY1, ghostDirection1)
            ghostX2, ghostY2, ghostDirection2 = moveGhost2(ghostX2, ghostY2, ghostDirection2)
            ghostX3, ghostY3, ghostDirection3 = moveGhost3(ghostX3, ghostY3, ghostDirection3)
            ghostX4, ghostY4, ghostDirection4 = moveGhost4(ghostX4, ghostY4, ghostDirection4)

        # If powerup is active and ghost is not eaten
        if powerUpActive == True and powerUpCounter > 0 and (ghostEaten1 == False or \
            ghostEaten2 == False or \
            ghostEaten3 == False or \
            ghostEaten4 == False):

            if score > 2000:
                ghostSpeed = 4
            elif score <= 2000:
                ghostSpeed = 2

            if ghostEaten1 == False:
                ghost1 = pygame.transform.scale(pygame.image.load(f"images//ghosts/scaredGhost.png"), (24, 24))
                ghostX1, ghostY1, ghostDirection1 = moveGhost1(ghostX1, ghostY1, ghostDirection1)

            if ghostEaten2 == False:
                ghost2 = pygame.transform.scale(pygame.image.load(f"images//ghosts/scaredGhost.png"), (24, 24))
                ghostX2, ghostY2, ghostDirection2 = moveGhost2(ghostX2, ghostY2, ghostDirection2)

            if ghostEaten3 == False:
                ghost3 = pygame.transform.scale(pygame.image.load(f"images//ghosts/scaredGhost.png"), (24, 24))
                ghostX3, ghostY3, ghostDirection3 = moveGhost3(ghostX3, ghostY3, ghostDirection3)

            if ghostEaten4 == False:
                ghost4 = pygame.transform.scale(pygame.image.load(f"images//ghosts/scaredGhost.png"), (24, 24))
                ghostX4, ghostY4, ghostDirection4 = moveGhost4(ghostX4, ghostY4, ghostDirection4)

    score, powerUps, powerUpActive = checkPelletsAndPowerUps(score, powerUps, powerUpActive)

    # If collision and no powerUp active
    if powerUpActive == False:
        if (playerHitbox.colliderect(ghostHitbox1) and ghostAlive1 == True) or \
        (playerHitbox.colliderect(ghostHitbox2) and ghostAlive2 == True) or \
        (playerHitbox.colliderect(ghostHitbox3) and ghostAlive3 == True) or \
        (playerHitbox.colliderect(ghostHitbox4) and ghostAlive4 == True):
            
            if lives > 0:
                lives -= 1
                startUpCounter = 0

                # Reset
                playerX = 10 
                playerY = 395 
                direction = 0
                directionChoice = 0  

                ghostX1 = 32
                ghostY1 = 812
                ghostDirection1 = 0
                ghostAlive1 = True

                ghostX2 = 782
                ghostY2 = 812
                ghostDirection2 = 0
                ghostAlive2 = True

                ghostX3 = 32
                ghostY3 = 31
                ghostDirection3 = 0
                ghostAlive3 = True

                ghostX4 = 782
                ghostY4 = 31
                ghostDirection4 = 0
                ghostAlive4 = True

            elif lives <= 0:
                lives -= 1
                moving = False
                gameEnd = True

    # If collision and powerUp active
    if powerUpActive == True and ((playerHitbox.colliderect(ghostHitbox1) and ghostAlive1 == True) or \
        (playerHitbox.colliderect(ghostHitbox2) and ghostAlive2 == True) or \
        (playerHitbox.colliderect(ghostHitbox3) and ghostAlive3 == True) or \
        (playerHitbox.colliderect(ghostHitbox4) and ghostAlive4 == True)):
        score += 200
        transparent = (0, 0, 0, 0)

        # Reset ghost in box
        if playerHitbox.colliderect(ghostHitbox1) and ghostAlive1 == True:
            ghostEaten1 = True
            ghostAlive1 = False
            ghostX1 = 390
            ghostY1 = 400
            ghostDirection1 = 2
            ghost1.fill(transparent)

        if playerHitbox.colliderect(ghostHitbox2) and ghostAlive2 == True:
            ghostEaten2 = True
            ghostAlive2 = False
            ghostX2 = 390
            ghostY2 = 400
            ghostDirection2 = 2
            ghost2.fill(transparent)

        if playerHitbox.colliderect(ghostHitbox3) and ghostAlive3 == True:
            ghostEaten3 = True
            ghostAlive3 = False
            ghostX3 = 390
            ghostY3 = 400
            ghostDirection3 = 2
            ghost3.fill(transparent)

        if playerHitbox.colliderect(ghostHitbox4) and ghostAlive4 == True:
            ghostEaten4 = True
            ghostAlive4 = False
            ghostX4 = 390
            ghostY4 = 400
            ghostDirection4 = 2
            ghost4.fill(transparent)


    for event in pygame.event.get(): # gets the input of keyboard
        if event.type == pygame.QUIT: # if the user quits
            run = False

        if moving == True:
            if event.type == pygame.KEYDOWN: # If the user presses a key
                if event.key == pygame.K_d:
                    directionChoice = 0 
                if event.key == pygame.K_a:
                    directionChoice = 1
                if event.key == pygame.K_w:
                    directionChoice = 2
                if event.key == pygame.K_s:
                    directionChoice = 3

                # activate powerUp

                if event.key == pygame.K_e:
                    if powerUps >= 1: # if there is a powerUp available
                        # When powerUp active, ghost changes direction
                        powerUps, powerUpActive, powerUpCounter, ghostDirection1, ghostDirection2, ghostDirection3, ghostDirection4 = activatePowerUp(powerUps, ghostDirection1, ghostDirection2, ghostDirection3, ghostDirection4)

            if event.type == pygame.KEYUP: # if the user holds down a key and is in the previous direction
                if event.key == pygame.K_d and directionChoice == 0:
                    directionChoice == direction
                if event.key == pygame.K_a and directionChoice == 1:
                    directionChoice == direction
                if event.key == pygame.K_w and directionChoice == 2:
                    directionChoice == direction
                if event.key == pygame.K_s and directionChoice == 3:
                    directionChoice == direction

    for i in range(len(possibleDirection)): # for each direction, if the user chooses a direction that they can go in, that direction is now the new direction
        if directionChoice == i and possibleDirection[i] == True:
            direction = i

    # check if player has gone through tunnel to other side of map
    if playerX > WIDTH:
        playerX = -45 # -50 is off board, -45 is slightly on board so pacman doesn't appear to disappear
    elif playerX < -50: # -50 is off board
        playerX = (WIDTH - 5) # WIDTH is off the board, -5 puts pacman slightly back on the board

    pygame.display.flip() # updates screen

pygame.quit()