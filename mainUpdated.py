import pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 600
BOXSIZE = 80
GAPSIZE = 10
COLORBOXSIZE = 50

BOARDWIDTH = 5
BOARDHEIGHT = 5

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = 50


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BGCOLOR = WHITE
BOXCOLOR = GRAY
COLORS = [RED, GREEN, BLUE, YELLOW]


def generateEmptyBoard():
    return [[None] * BOARDHEIGHT for _ in range(BOARDWIDTH)]


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def drawBoard(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            color = board[boxx][boxy] if board[boxx][boxy] else BOXCOLOR
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, BOXSIZE, BOXSIZE), 2)


def drawColorMenu():
    menuY = YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE) + 20
    gap = 20
    for i, color in enumerate(COLORS):
        left = XMARGIN + i * (COLORBOXSIZE + gap)
        top = menuY
        pygame.draw.rect(DISPLAYSURF, color, (left, top, COLORBOXSIZE, COLORBOXSIZE))
        if color == selectedColor:
            pygame.draw.rect(DISPLAYSURF, GRAY, (left - 2, top - 2, COLORBOXSIZE + 4, COLORBOXSIZE + 4), 3)


def handleColorMenuClick(mousex, mousey):
    global selectedColor
    menuY = YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE) + 20
    gap = 20
    for i, color in enumerate(COLORS):
        left = XMARGIN + i * (COLORBOXSIZE + gap)
        if left <= mousex <= left + COLORBOXSIZE and menuY <= mousey <= menuY + COLORBOXSIZE:
            selectedColor = color
            break


def isValidMove(board, boxx, boxy, color):
    neighbors = getNeighbors(board, boxx, boxy)
    for neighbor in neighbors:
        if board[neighbor[0]][neighbor[1]] == color:
            return False
    return True


def getNeighbors(board, boxx, boxy):
    neighbors = []
    if boxx > 0:
        neighbors.append((boxx - 1, boxy))
    if boxx < BOARDWIDTH - 1:
        neighbors.append((boxx + 1, boxy))
    if boxy > 0:
        neighbors.append((boxx, boxy - 1))
    if boxy < BOARDHEIGHT - 1:
        neighbors.append((boxx, boxy + 1))
    return neighbors


def isBoardComplete(board):
    for row in board:
        if None in row:
            return False
    return True


def showWinMessage():
    font = pygame.font.Font(None, 72)
    text = font.render('You did it!', True, WHITE, GREEN)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()


def drawMessage(message):
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, WHITE, RED)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()


def showInstructions():
    fontTitle = pygame.font.Font(None, 64)
    fontText = pygame.font.Font(None, 30)

    title = fontTitle.render("Hello there!", True, WHITE)
    instructions = [
        "Rules:",
        "- Color all the fields.",
        "- Pick a color from the menu below.",
        "- Click on any empty field to color it.",
        "- Adjacent fields must not be the same color!",
        "- You are allowed 3 wrong moves;",
        " after that, you lose!",
        "Click to start."
    ]

    titleRect = title.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 7))
    instructionRects = []
    for i, line in enumerate(instructions):
        text = fontText.render(line, True, BLACK)
        rect = text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + i * 30))
        instructionRects.append((text, rect))

    while True:
        DISPLAYSURF.fill(GRAY)
        DISPLAYSURF.blit(title, titleRect)
        for text, rect in instructionRects:
            DISPLAYSURF.blit(text, rect)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()


def main():
    global FPSCLOCK, DISPLAYSURF, selectedColor
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Fill Game')

    showInstructions()

    board = generateEmptyBoard()
    selectedColor = COLORS[0]
    invalidMoves = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        font = pygame.font.Font(None, 36)
        invalidMovesText = font.render(f"Wrong Moves: {invalidMoves}", True, GRAY)
        DISPLAYSURF.blit(invalidMovesText, (XMARGIN, YMARGIN - 40))
        drawBoard(board)
        drawColorMenu()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if mousey > YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE):
                    handleColorMenuClick(mousex, mousey)
                else:
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    if board[boxx][boxy] is None:
                        if isValidMove(board, boxx, boxy, selectedColor):
                            board[boxx][boxy] = selectedColor
                            if isBoardComplete(board):
                                drawBoard(board)
                                showWinMessage()
                                pygame.time.wait(5000)
                                pygame.quit()
                                sys.exit()
                        else:
                            invalidMoves += 1

                            if invalidMoves > 3:
                                drawMessage("You lost :(")
                                pygame.time.wait(3000)
                                pygame.quit()
                                sys.exit()
                            else:
                                drawMessage("Wrong move!")
                                pygame.time.wait(1000)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()