import pygame , os
from pygame.locals import *
pygame.init()

FPS = 30
WIDTH = 640
HEIGHT = 500
SPACESIZE = 75
FILAS = 6
COLUMNAS = 6
FICHA_B = 'FICHA_B'
FICHA_N = 'FICHA_N'
VACIO = 'VACIO'
AYUDA = 'AYUDA'

ANIMATIONSPEED = 30

Margen_x = int((WIDTH - (FILAS * SPACESIZE)) / 2)
Margen_y = int((HEIGHT - (COLUMNAS * SPACESIZE)) / 2)

Win = pygame.display.set_mode((WIDTH, HEIGHT))
main_clock = pygame.time.Clock()
pygame.display.set_caption('O Othello mais increible do mundo')
FONT = pygame.font.Font('freesansbold.ttf', 16)
BIGFONT = pygame.font.Font('freesansbold.ttf', 24)
boardImage = pygame.image.load(os.path.join("Imagenes","casilla.png"))
boardImage = pygame.transform.smoothscale(boardImage, (FILAS * SPACESIZE, COLUMNAS * SPACESIZE))
boardImageRect = boardImage.get_rect()
boardImageRect.topleft = (Margen_x, Margen_y)
fondo = pygame.image.load(os.path.join("imagenes","madera_oscura.png"))
fondo = pygame.transform.smoothscale(fondo, (WIDTH, HEIGHT))
fondo.blit(boardImage, boardImageRect)

#RGB
ROJO = ( 200, 0 , 0)
BLANCO = ( 175 , 175 , 175)
NEGRO = (  0 ,   0 , 0)
VERDE = (  0 , 155 , 0)
GRIS = (50 , 50 , 50)

TXT1 = GRIS
TXT2 = VERDE
LINEAS = NEGRO
COLOR_FUENTE = BLANCO
COLOR_AYUDA = VERDE