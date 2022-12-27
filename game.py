## base game
from board import board
import pygame

pygame.init()

quadSize = 10

WIDTH = 840
HEIGHT = 890
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60

def drawBoard(board):
    height = ((HEIGHT - 50) // 30) # -50 for padding and 32 is height of board
    width = ((WIDTH // 28)) # 30 is width of board ####### double check
    for i in range(len(board)): # each row
        for j in range(len(board[i])): # each column in row
            if board[i][j] == 1:
                pygame.draw.circle(screen, "white", (j * width + (0.5 * width), i * height + (0.5 * height)), 4) # location, colour, the square it is in and coordinate shifted to centre, radius
            if board[i][j] == 2:
                pygame.draw.circle(screen, "white", (j * width + (0.5 * width), i * height + (0.5 * height)), 10) # location, colour, the square it is in and coordinate shifted to centre, radius
            if board[i][j] == 3:
                #pygame.draw.rect(screen, "blue", ((WIDTH // width) * j, HEIGHT // height * i, j + width, i + height))
                x = width * j
                y = height * i
                pygame.draw.rect(screen, "red",(x, y, width+2, height+2))
                pygame.draw.rect(screen, "blue",(x, y, width, height))
            if board[i][j] == 4:
                x = width * j
                y = height * i
                pygame.draw.rect(screen, "red",(x, y, width+2, height+2))
                pygame.draw.rect(screen, "white",(x, y, width, height))




run = True

while run:
    timer.tick(fps)
    screen.fill("black")
    drawBoard(board)

    for event in pygame.event.get(): # gets the input of keyboard
        if event.type == pygame.QUIT: # if the user quits
            run = False

    pygame.display.flip() # updates screen

pygame.quit()


