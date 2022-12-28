# Import the necessary libraries
import pygame
import sys

# Initialize pygame
pygame.init()

# Set the window size
window_size = (600, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Pac-Man")

# Set the background color
bg_color = (0, 0, 0)

# Set the dimensions of the Pac-Man character
pacman_size = (50, 50)

# Load the Pac-Man image and get its rect
pacman_image = pygame.image.load("pacman.png")
pacman_rect = pacman_image.get_rect()

# Set the initial position of the Pac-Man character
pacman_rect.x = 275
pacman_rect.y = 275

# Set the movement speed of the Pac-Man character
pacman_speed = 5

# Set the dimensions of the ghost character
ghost_size = (50, 50)

# Load the ghost image and get its rect
ghost_image = pygame.image.load("ghost.png")
ghost_rect = ghost_image.get_rect()

# Set the initial position of the ghost character
ghost_rect.x = 50
ghost_rect.y = 50

# Set the movement speed of the ghost character
ghost_speed = 5

# Set the game loop to run indefinitely
while True:
    # Check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check for arrow key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_rect.x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman_rect.x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_rect.y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman_rect.y += pacman_speed

    # Move the ghost towards the Pac-Man character
    if ghost_rect.x < pacman_rect.x:
        ghost_rect.x += ghost_speed
    if ghost_rect.x > pacman_rect.x:
        ghost_rect.x -= ghost_speed
    if ghost_rect.y < pacman_rect.y:
        ghost_rect.y += ghost_speed
    if ghost_rect.y > pacman_rect.y:
        ghost_rect.y -= ghost_speed

    # Draw the background
    screen.fill(bg_color)

    # Draw the Pac-Man character
    screen.blit(pacman_image, pacman_rect)

    # Draw the ghost character
    screen.blit(ghost_image, ghost_rect)

    # Update the display
    pygame.display.flip()
