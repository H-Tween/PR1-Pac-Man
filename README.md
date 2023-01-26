# Pac-Man Requirements

* Harrison Tween
* Aaron Temiwoluwa

## Description

In this game, the character "Pac-Man" will be able to move around a maze using arrow keys whilst trying to avoid the ghosts. There will also be pellets to pick up which will increase the score and cherries which can be used to eat the ghost.

## User Requirements

1. The user can move around the screen, following the path on the screen.
2. Ghosts (opposition) will be moving around randomly through the same paths. 
3. If the ghost touches Pac-Man, the game resets and a life is lost. Pac-Man will be 2 spare lives.
4. Pellets will be scattered around the paths. Collecting them will increase your score. 
5. There will also be cherries that can be picked up and stored, allowing Pac-Man to eat the ghosts. This effect will last for 10 seconds and then the game will revert back to normal.
6. Once all the pellets are gone, the game will end and the score will be displayed. The user will then be prompted to exit the game with a button.

## Proposed Development

* IDE: Visual Studio Code
* Programming Language: Python
* Game Engine: pygame

## Installing the python packages

Using the virtual environment manager of your choice (venv, conda, etc.), install the python packages

`pip install -r requirements.txt`
