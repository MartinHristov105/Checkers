import pygame
from pygame import Surface
from typing import *

# Window and playing field dimensions
WIDTH, HEIGHT = 800, 800

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Load and scale the crown image
CROWN = pygame.transform.scale(pygame.image.load('src/assets/crown.png'), (44, 25))