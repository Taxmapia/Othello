import pygame
import os
WIDTH , HEIGHT = 800 , 800

FILAS, COLUMNAS = 6, 6

CASILLA = pygame.image.load(os.path.join("imagenes","casilla.png"))
F_A = pygame.image.load(os.path.join("imagenes","Ficha_Azul.png"))
F_R = pygame.image.load(os.path.join("imagenes","Ficha_Roja.png"))

BLOQUE_SIZE = WIDTH//COLUMNAS

#RGB
R = (255,0,0)
G = (0,255,0)
B = (0,0,255)

NEGRO = (0,0,0)
BLANCO = (255,255,255)
