import random, sys, time, copy
import pygame
from Run import *
from pygame.locals import *
from Constantes import *

pygame.init()

def translateBoardToPixelCoord(x, y):
    return Margen_x + x * SPACESIZE + int(SPACESIZE / 2), Margen_y + y * SPACESIZE + int(SPACESIZE / 2)


def Dibujar_Tablero(board):
    # Draw background of board.
    Win.blit(fondo, fondo.get_rect())

    # Draw grid lines of the board.
    for x in range(FILAS + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + Margen_x
        starty = Margen_y
        endx = (x * SPACESIZE) + Margen_x
        endy = Margen_y + (COLUMNAS * SPACESIZE)
        pygame.draw.line(Win, LINEAS, (startx, starty), (endx, endy))
    for y in range(COLUMNAS + 1):
        # Draw the vertical lines.
        startx = Margen_x
        starty = (y * SPACESIZE) + Margen_y
        endx = Margen_x + (FILAS * SPACESIZE)
        endy = (y * SPACESIZE) + Margen_y
        pygame.draw.line(Win, LINEAS, (startx, starty), (endx, endy))

    # Draw the NEGRO & BLANCO tiles or hint spots.
    for x in range(FILAS):
        for y in range(COLUMNAS):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == FICHA_B or board[x][y] == FICHA_N:
                if board[x][y] == FICHA_B:
                    tileColor = ROJO
                else:
                    tileColor = NEGRO
                pygame.draw.circle(Win, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            if board[x][y] == AYUDA:
                pygame.draw.rect(Win, COLOR_AYUDA, (centerx - 4, centery - 4, 6, 6))


def getSpaceClicked(mousex, mousey):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(FILAS):
        for y in range(COLUMNAS):
            if mousex > x * SPACESIZE + Margen_x and \
               mousex < (x + 1) * SPACESIZE + Margen_x and \
               mousey > y * SPACESIZE + Margen_y and \
               mousey < (y + 1) * SPACESIZE + Margen_y:
                return (x, y)
    return None


def Info(board, jugador, ficha_karen, turno):
    # Draws scores and whose turno it is at the bottom of the screen.
    scores = Puntuacion_Actual(board)
    scoreSurf = FONT.render("Tu puntaje: %s    Puntaje Adversario: %s    Turno de: %s" % (str(scores[jugador]), str(scores[ficha_karen]), turno.title()), True, COLOR_FUENTE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, HEIGHT - 5)
    Win.blit(scoreSurf, scoreRect)


def Reiniciar_Tablero(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(FILAS):
        for y in range(COLUMNAS):
            board[x][y] = VACIO

    # Add starting pieces to the center
    board[2][2] = FICHA_B
    board[2][3] = FICHA_N
    board[3][2] = FICHA_N
    board[3][3] = FICHA_B


def Nuevo_Tablero():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(FILAS):
        board.append([VACIO] * COLUMNAS)

    return board


def Valida_Mov(board, tile, xstart, ystart):
    # Returns False if the jugador's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != VACIO or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == FICHA_B:
        otherTile = FICHA_N
    else:
        otherTile = FICHA_B

    flip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other jugador next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    flip.append([x, y])

    board[xstart][ystart] = VACIO # make space empty
    if len(flip) == 0: # If no tiles flipped, this move is invalid
        return False
    return flip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < FILAS and y >= 0 and y < COLUMNAS


def Aiuras(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in Mov_Valido(dupeBoard, tile):
        dupeBoard[x][y] = AYUDA
    return dupeBoard


def Mov_Valido(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(FILAS):
        for y in range(COLUMNAS):
            if Valida_Mov(board, tile, x, y):
                validMoves.append((x, y))
    return validMoves


def Puntuacion_Actual(board):
    # Determine the score by counting the tiles.
    xscore = 0
    oscore = 0
    for x in range(FILAS):
        for y in range(COLUMNAS):
            if board[x][y] == FICHA_B:
                xscore += 1
            if board[x][y] == FICHA_N:
                oscore += 1
    return {FICHA_B:xscore, FICHA_N:oscore}


def Ficha_Player():
    # Create the txt.
    txtSurf = FONT.render('¿Quieres ser ROJO o NEGRO?', True, COLOR_FUENTE, TXT1)
    txtRect = txtSurf.get_rect()
    txtRect.center = (int(WIDTH / 2), int(HEIGHT / 2))

    xSurf = BIGFONT.render('ROJO', True, COLOR_FUENTE, TXT1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WIDTH / 2) - 60, int(HEIGHT / 2) + 40)

    oSurf = BIGFONT.render('NEGRO', True, COLOR_FUENTE, TXT1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WIDTH / 2) + 60, int(HEIGHT / 2) + 40)

    while True:
        # Keep looping until the jugador has clicked on a color.
        Quit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [FICHA_B, FICHA_N]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [FICHA_N, FICHA_B]

        # Draw the screen.
        Win.blit(txtSurf, txtRect)
        Win.blit(xSurf, xRect)
        Win.blit(oSurf, oRect)
        pygame.display.update()
        main_clock.tick(FPS)


def Mover(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    flip = Valida_Mov(board, tile, xstart, ystart)

    if flip == False:
        return False

    board[xstart][ystart] = tile

    for x, y in flip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == FILAS and y == 0) or \
           (x == 0 and y == COLUMNAS) or \
           (x == FILAS and y == COLUMNAS)


def getComputerMove(board, ficha):
    posible = Mov_Valido(board, ficha)

    # randomize the order of the possible moves
    random.shuffle(posible)

    # always go for a corner if available.
    for x, y in posible:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in posible:
        dupeBoard = copy.deepcopy(board)
        Mover(dupeBoard, ficha, x, y)
        score = Puntuacion_Actual(dupeBoard)[ficha]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def Quit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()