import pygame
import random, sys, time, copy
from Constantes import *
from Main import *
from Funciones import *

pygame.init()

def run():
    
    tablero_principal = Nuevo_Tablero()
    Reiniciar_Tablero(tablero_principal)
    ayuda = False
    turno = 'Jogador'

    # Draw the starting board and ask the jugador what color they want.
    Dibujar_Tablero(tablero_principal)
    jugador, ficha_karen = Ficha_Player()

    # Make the Surface and Rect objects for the "New Game" and "aiura" buttons
    nuevo_juegoSurf = FONT.render('Nuevo Juego', True, COLOR_FUENTE, TXT2)
    nuevo_juegoRect = nuevo_juegoSurf.get_rect()
    nuevo_juegoRect.topleft = (5, 10)
    aiuraSurf = FONT.render('Aiura', True, COLOR_FUENTE, TXT2)
    aiuraRect = aiuraSurf.get_rect()
    aiuraRect.topright = (WIDTH - 5, 10)

    while True:
        if turno == 'Jogador':
            if Mov_Valido(tablero_principal, jugador) == []:
                break
            xy = None
            while xy == None:
                if ayuda:
                    tablero = Aiuras(tablero_principal, jugador)
                else:
                    tablero = tablero_principal
                Quit()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if nuevo_juegoRect.collidepoint( (mousex, mousey) ):
                            return True
                        elif aiuraRect.collidepoint( (mousex, mousey) ):
                            # Toggle aiura mode
                            ayuda = not ayuda
                        xy = getSpaceClicked(mousex, mousey)
                        if xy != None and not isValidMove(tablero_principal, jugador, xy[0], xy[1]):
                            xy = None

                # Dibujar Tablero
                Dibujar_Tablero(tablero)
                Info(tablero, jugador, ficha_karen, turno)
                # Dibuja botones "juego nuevo" y "aiura"
                Win.blit(nuevo_juegoSurf, nuevo_juegoRect)
                Win.blit(aiuraSurf, aiuraRect)

                main_clock.tick(FPS)
                pygame.display.update()

            # Mueve y termina turno
            Mover(tablero_principal, jugador, xy[0], xy[1], True)
            if Mov_Valido(tablero_principal, ficha_karen) != []:
                turno = 'Karen'
        else:
            # Computadora
            if Mov_Valido(tablero_principal, ficha_karen) == []:
                break
            # Tablero.
            Dibujar_Tablero(tablero_principal)
            Info(tablero_principal, jugador, ficha_karen, turno)

            # Dibuja "Juego nuevo" y "aiura".
            Win.blit(nuevo_juegoSurf, nuevo_juegoRect)
            Win.blit(aiuraSurf, aiuraRect)
            #pausa
            pausa = time.time() + random.randint(5, 10) * 0.1
            while time.time() < pausa:
                pygame.display.update()

            # Mueve y termina el turno.
            x, y = getComputerMove(tablero_principal, ficha_karen)
            Mover(tablero_principal, ficha_karen, x, y, True)
            if Mov_Valido(tablero_principal, jugador) != []:
                # Only set for the jugador's turno if they can make a move.
                turno = 'Jogador'

    # Display the final score.
    Dibujar_Tablero(tablero_principal)
    scores = Puntuacion_Actual(tablero_principal)

    # Determine the txt of the message to display.
    if scores[jugador] > scores[ficha_karen]:
        txt = '¡Habeis ganado por %s pointos! Congratulaciones!' % \
               (scores[jugador] - scores[ficha_karen])
    elif scores[jugador] < scores[ficha_karen]:
        txt = '¡Habeis perdido por %s pointos! Congratulacionesn´t!' % \
               (scores[ficha_karen] - scores[jugador])
    else:
        txt = '¡Empate!'

    txtSurf = FONT.render(txt, True, COLOR_FUENTE, TXT1)
    txtRect = txtSurf.get_rect()
    txtRect.center = (int(WIDTH / 2), int(HEIGHT / 2))
    Win.blit(txtSurf, txtRect)

    # Display the "Play again?" txt with cis and No buttons.
    txt2Surf = BIGFONT.render('¿Jugar de Nuevo?', True, COLOR_FUENTE, TXT1)
    txt2Rect = txt2Surf.get_rect()
    txt2Rect.center = (int(WIDTH / 2), int(HEIGHT / 2) + 50)

    # Make "cis" button.
    cisSurf = BIGFONT.render('Cis', True, COLOR_FUENTE, TXT1)
    cisRect = cisSurf.get_rect()
    cisRect.center = (int(WIDTH / 2) - 60, int(HEIGHT / 2) + 90)

    # Make "non" button.
    nonSurf = BIGFONT.render('Non', True, COLOR_FUENTE, TXT1)
    nonRect = nonSurf.get_rect()
    nonRect.center = (int(WIDTH / 2) + 60, int(HEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on cis or non.
        Quit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if cisRect.collidepoint( (mousex, mousey) ):
                    return True
                elif nonRect.collidepoint( (mousex, mousey) ):
                    return False
        Win.blit(txtSurf, txtRect)
        Win.blit(txt2Surf, txt2Rect)
        Win.blit(cisSurf, cisRect)
        Win.blit(nonSurf, nonRect)
        pygame.display.update()
        main_clock.tick(FPS)
