import random, sys, pygame, time, copy
import Imagenes
import Constantes
import os
from pygame.locals import *
from Constantes import *




def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 24)

    # Set up the background image.
    boardImage = pygame.image.load(os.path.join("Imagenes","casilla.png")) #flyppyboard
    # Use smoothscale() to stretch the board image to fit the entire board:
    boardImage = pygame.transform.smoothscale(boardImage, (FILAS * SPACESIZE, COLUMNAS * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (Margen_x, Margen_y)
    BGIMAGE = pygame.image.load(os.path.join("imagenes","madera_oscura.png")) #flyppy brackground
    # Use smoothscale() to stretch the background image to fit the entire window:
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WIDTH, HEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    # Run the main game.
    while True:
        if runGame() == False:
            break


def runGame():
    # Plays a single game of reversi each time this function is called.

    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = random.choice(['computer', 'player'])

    # Draw the starting board and ask the player what color they want.
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    # Make the Surface and Rect objects for the "New Game" and "Hints" buttons
    newGameSurf = FONT.render('New Game', True, COLOR_FUENTE, TXT2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WIDTH - 6, 10)
    hintsSurf = FONT.render('Hints', True, COLOR_FUENTE, TXT2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WIDTH - 6, 40)

    while True: # main game loop
        # Keep looping for player and computer's turns.
        if turn == 'player':
            # Player's turn:
            if getValidMoves(mainBoard, playerTile) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                break
            movexy = None
            while movexy == None:
                # Keep looping until the player clicks on a valid space.

                # Determine which board data structure to use for display.
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            # Start a new game
                            return True
                        elif hintsRect.collidepoint( (mousex, mousey) ):
                            # Toggle hints mode
                            showHints = not showHints
                        # movexy is set to a two-item tuple XY coordinate, or None value
                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                            movexy = None

                # Draw the game board.
                drawBoard(boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)

                # Draw the "New Game" and "Hints" buttons.
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            # Make the move and end the turn.
            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) != []:
                # Only set for the computer's turn if it can make a move.
                turn = 'computer'

        else:
            # Computer's turn:
            if getValidMoves(mainBoard, computerTile) == []:
                # If it was set to be the computer's turn but
                # they can't move, then end the game.
                break

            # Draw the board.
            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)

            # Draw the "New Game" and "Hints" buttons.
            DISPLAYSURF.blit(newGameSurf, newGameRect)
            DISPLAYSURF.blit(hintsSurf, hintsRect)

            # Make it look like the computer is thinking by pausing a bit.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()

            # Make the move and end the turn.
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y, True)
            if getValidMoves(mainBoard, playerTile) != []:
                # Only set for the player's turn if they can make a move.
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)

    # Determine the text of the message to display.
    if scores[playerTile] > scores[computerTile]:
        text = 'You beat the computer by %s points! Congratulations!' % \
               (scores[playerTile] - scores[computerTile])
    elif scores[playerTile] < scores[computerTile]:
        text = 'You lost. The computer beat you by %s points.' % \
               (scores[computerTile] - scores[playerTile])
    else:
        text = 'The game was a tie!'

    textSurf = FONT.render(text, True, COLOR_FUENTE, TXT1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WIDTH / 2), int(HEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    # Display the "Play again?" text with Yes and No buttons.
    text2Surf = BIGFONT.render('Play again?', True, COLOR_FUENTE, TXT1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WIDTH / 2), int(HEIGHT / 2) + 50)

    # Make "Yes" button.
    yesSurf = BIGFONT.render('Yes', True, COLOR_FUENTE, TXT1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WIDTH / 2) - 60, int(HEIGHT / 2) + 90)

    # Make "No" button.
    noSurf = BIGFONT.render('No', True, COLOR_FUENTE, TXT1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WIDTH / 2) + 60, int(HEIGHT / 2) + 90)

    while True:
        # Process events until the user clicks on Yes or No.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def translateBoardToPixelCoord(x, y):
    return Margen_x + x * SPACESIZE + int(SPACESIZE / 2), Margen_y + y * SPACESIZE + int(SPACESIZE / 2)


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    # Draw the additional tile that was just laid down. (Otherwise we'd
    # have to completely redraw the board & the board info.)
    if tileColor == FICHA_B:
        additionalTileColor = BLANCO
    else:
        additionalTileColor = NEGRO
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == FICHA_B:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == FICHA_N:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


def drawBoard(board):
    # Draw background of board.
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

    # Draw grid lines of the board.
    for x in range(FILAS + 1):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + Margen_x
        starty = Margen_y
        endx = (x * SPACESIZE) + Margen_x
        endy = Margen_y + (COLUMNAS * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, LINEAS, (startx, starty), (endx, endy))
    for y in range(COLUMNAS + 1):
        # Draw the vertical lines.
        startx = Margen_x
        starty = (y * SPACESIZE) + Margen_y
        endx = Margen_x + (FILAS * SPACESIZE)
        endy = (y * SPACESIZE) + Margen_y
        pygame.draw.line(DISPLAYSURF, LINEAS, (startx, starty), (endx, endy))

    # Draw the NEGRO & BLANCO tiles or hint spots.
    for x in range(FILAS):
        for y in range(COLUMNAS):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == FICHA_B or board[x][y] == FICHA_N:
                if board[x][y] == FICHA_B:
                    tileColor = ROJO
                else:
                    tileColor = NEGRO
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
            if board[x][y] == AYUDA:
                pygame.draw.rect(DISPLAYSURF, COLOR_AYUDA, (centerx - 4, centery - 4, 6, 6))


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


def drawInfo(board, playerTile, computerTile, turn):
    # Draws scores and whose turn it is at the bottom of the screen.
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, COLOR_FUENTE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, HEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def resetBoard(board):
    # Blanks out the board it is passed, and sets up starting tiles.
    for x in range(FILAS):
        for y in range(COLUMNAS):
            board[x][y] = VACIO

    # Add starting pieces to the center
    board[2][2] = FICHA_B
    board[2][3] = FICHA_N
    board[3][2] = FICHA_N
    board[3][3] = FICHA_B


def getNewBoard():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(FILAS):
        board.append([VACIO] * COLUMNAS)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if board[xstart][ystart] != VACIO or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == FICHA_B:
        otherTile = FICHA_N
    else:
        otherTile = FICHA_B

    tilesToFlip = []
    # check each of the eight directions:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # The piece belongs to the other player next to our piece.
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
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = VACIO # make space empty
    if len(tilesToFlip) == 0: # If no tiles flipped, this move is invalid
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x < FILAS and y >= 0 and y < COLUMNAS


def getBoardWithValidMoves(board, tile):
    # Returns a new board with hint markings.
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = AYUDA
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of (x,y) tuples of all valid moves.
    validMoves = []

    for x in range(FILAS):
        for y in range(COLUMNAS):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def getScoreOfBoard(board):
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


def enterPlayerTile():
    # Create the text.
    textSurf = FONT.render('¿Quieres ser BLANCO o Negro?', True, COLOR_FUENTE, TXT1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WIDTH / 2), int(HEIGHT / 2))

    xSurf = BIGFONT.render('BLANCO', True, COLOR_FUENTE, TXT1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WIDTH / 2) - 60, int(HEIGHT / 2) + 40)

    oSurf = BIGFONT.render('NEGRO', True, COLOR_FUENTE, TXT1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WIDTH / 2) + 60, int(HEIGHT / 2) + 40)

    while True:
        # Keep looping until the player has clicked on a color.
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    return [FICHA_B, FICHA_N]
                elif oRect.collidepoint( (mousex, mousey) ):
                    return [FICHA_N, FICHA_B]

        # Draw the screen.
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def makeMove(board, tile, xstart, ystart, realMove=False):
    # Place the tile on the board at xstart, ystart, and flip tiles
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or \
           (x == FILAS and y == 0) or \
           (x == 0 and y == COLUMNAS) or \
           (x == FILAS and y == COLUMNAS)


def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()