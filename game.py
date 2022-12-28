## base game
from board import board
import pygame

pygame.init()

WIDTH = 840
HEIGHT = 890
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
pacmanImages = []
pacmanX = 10
pacmanY = 394
direction = 0
counter = 0

for i in range(1, 4):
    image = pygame.image.load(f"images/pacman{i}.png")
    pacmanImages.append(pygame.transform.scale(pygame.image.load(f"images/P{i}.png"), (25, 24)))

def drawBoard(board):
    height = ((HEIGHT - 50) // 30) # -50 for padding and 32 is height of board
    width = ((WIDTH // 28)) # 30 is width of board ####### double check
    for i in range(len(board)): # each row
        for j in range(len(board[i])): # each column in row
            if board[i][j] == 1:
                pygame.draw.circle(screen, "white", (j * width + (0.5 * width), i * height + (0.5 * height)), 4) # location, colour, the square it is in and coordinate shifted to centre, radius
            if board[i][j] == 2:
                pygame.draw.circle(screen, "white", (j * width + (0.5 * width), i * height + (0.5 * height)), 8) # location, colour, the square it is in and coordinate shifted to centre, radius
            if board[i][j] == 3:
                #pygame.draw.rect(screen, "blue", ((WIDTH // width) * j, HEIGHT // height * i, j + width, i + height))
                x = width * j
                y = height * i
                pygame.draw.rect(screen, "red",(x, y, width+2, height+2))
                pygame.draw.rect(screen, "blue",(x, y, width, height))
            if board[i][j] == 4:
                x = width * j
                y = height * i
                pygame.draw.line(screen, "white", (x, y + (0.5 * height)), (x + width, y + (0.5*height)), 3)
                
def drawPacman():
    # Right, left, up, down
    imageCounter = counter // 8
    if direction == 0:
        screen.blit(pacmanImages[imageCounter], (pacmanX, pacmanY)) 
    elif direction == 1:
        screen.blit(pygame.transform.flip(pacmanImages[imageCounter], True, False), (pacmanX, pacmanY))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], 90), (pacmanX, pacmanY))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], 270), (pacmanX, pacmanY))



run = True

while run:
    timer.tick(fps)
    if counter < 23:
        counter += 1

    else:
        counter = 0

    screen.fill("black")
    drawBoard(board)
    drawPacman()

    for event in pygame.event.get(): # gets the input of keyboard
        if event.type == pygame.QUIT: # if the user quits
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction = 0 
            if event.key == pygame.K_a:
                direction = 1
            if event.key == pygame.K_w:
                direction = 2
            if event.key == pygame.K_s:
                direction = 3

    pygame.display.flip() # updates screen

pygame.quit()


