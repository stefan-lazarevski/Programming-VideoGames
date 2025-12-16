import random, pygame, sys, os
from pygame.locals import *

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
FPS = 30

# Board settings
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
CELL_SIZE = 64

# Calculate margins to center the board
X_MARGIN = int((WINDOW_WIDTH - (CELL_SIZE * BOARD_WIDTH)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (CELL_SIZE * BOARD_HEIGHT)) / 2) + 30

# Colors
GRAY = (40, 40, 45)
DARK_GRAY = (25, 25, 28)
WHITE = (255, 255, 255)
RED = (220, 80, 80)
BLUE = (80, 120, 220)
GREEN = (80, 220, 120)
PURPLE = (200, 80, 200)
YELLOW = (255, 255, 0)
GRID_COLOR = (60, 60, 65)

# Candy types
RED_CANDY = "red"
BLUE_CANDY = "blue"
GREEN_CANDY = "green"
PURPLE_CANDY = "purple"
ALL_CANDIES = [RED_CANDY, BLUE_CANDY, GREEN_CANDY, PURPLE_CANDY]

# Candy image files
ASSET_FILES = [
    "candy1.png",
    "candy2.png",
    "candy3.png",
    "candy4.png",
]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Candy Crush Clone")
FONT = pygame.font.SysFont("arial", 24, bold=True)


def loadCandyImages():
    images = {}

    # Uncomment this section if you have candy image files (candy1.png, candy2.png, etc.)
    # found_all = all(os.path.exists(p) for p in ASSET_FILES)
    # if found_all:
    #     img1 = pygame.image.load(ASSET_FILES[0]).convert_alpha()
    #     img1 = pygame.transform.smoothscale(img1, (CELL_SIZE, CELL_SIZE))
    #     images[RED_CANDY] = img1
    #
    #     img2 = pygame.image.load(ASSET_FILES[1]).convert_alpha()
    #     img2 = pygame.transform.smoothscale(img2, (CELL_SIZE, CELL_SIZE))
    #     images[BLUE_CANDY] = img2
    #
    #     img3 = pygame.image.load(ASSET_FILES[2]).convert_alpha()
    #     img3 = pygame.transform.smoothscale(img3, (CELL_SIZE, CELL_SIZE))
    #     images[GREEN_CANDY] = img3
    #
    #     img4 = pygame.image.load(ASSET_FILES[3]).convert_alpha()
    #     img4 = pygame.transform.smoothscale(img4, (CELL_SIZE, CELL_SIZE))
    #     images[PURPLE_CANDY] = img4
    # else:

    # Create nice colored shapes as fallback
    colors_map = {
        RED_CANDY: (220, 80, 80),
        BLUE_CANDY: (80, 120, 220),
        GREEN_CANDY: (80, 220, 120),
        PURPLE_CANDY: (200, 80, 200)
    }

    for candy_type, color in colors_map.items():
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE), border_radius=12)
        pygame.draw.rect(surf, (255, 255, 255, 40), pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE), 4, border_radius=12)
        images[candy_type] = surf

    return images


def makeText(text, color, left, top):
    textSurface = FONT.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.topleft = (left, top)
    return textSurface, textRect


def getLeftTopOfBox(boxx, boxy):
    left = X_MARGIN + (boxx * CELL_SIZE)
    top = Y_MARGIN + (boxy * CELL_SIZE)
    return left, top


def getBoxAtPixel(mousex, mousey):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
            if boxRect.collidepoint(mousex, mousey):
                return boxx, boxy
    return None, None


def checkValidSecondSelection(firstSelection, secondSelection):
    # Allow adjacent moves (up, down, left, right, and DIAGONALS)
    x1, y1 = firstSelection
    x2, y2 = secondSelection

    # Check if exactly one position away (includes diagonals)
    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2):
        return True
    return False


def checkBoardForMatches(board):
    matches = []

    # Check horizontal matches
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] != None:
                candy = board[x][y]
                if y <= BOARD_HEIGHT - 3:
                    if candy == board[x][y + 1] and candy == board[x][y + 2]:
                        i = y
                        while i < BOARD_HEIGHT and board[x][i] == candy:
                            matches.append((x, i))
                            i += 1

    # Check vertical matches
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[x][y] != None:
                candy = board[x][y]
                if x <= BOARD_WIDTH - 3:
                    if candy == board[x + 1][y] and candy == board[x + 2][y]:
                        i = x
                        while i < BOARD_WIDTH and board[i][y] == candy:
                            matches.append((i, y))
                            i += 1

    # # Check diagonal matches (top-left to bottom-right)
    # for x in range(BOARD_WIDTH - 2):
    #     for y in range(BOARD_HEIGHT - 2):
    #         if board[x][y] != None:
    #             candy = board[x][y]
    #             if candy == board[x + 1][y + 1] == board[x + 2][y + 2]:
    #                 i = 0
    #                 while (x + i < BOARD_WIDTH and y + i < BOARD_HEIGHT and board[x + i][y + i] == candy):
    #                     matches.append((x + i, y + i))
    #                     i += 1

    # # Check diagonal matches (top-right to bottom-left)
    # for x in range(BOARD_WIDTH - 2):
    #     for y in range(2, BOARD_HEIGHT):
    #         if board[x][y] != None:
    #             candy = board[x][y]
    #             if candy == board[x + 1][y - 1] == board[x + 2][y - 2]:
    #                 i = 0
    #                 while (x + i < BOARD_WIDTH and y - i >= 0 and board[x + i][y - i] == candy):
    #                     matches.append((x + i, y - i))
    #                     i += 1

    return matches


def removeMatches(board, matches):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if (x, y) in matches:
                board[x][y] = None


def slideDownCandy(board):
    for x in range(BOARD_WIDTH):
        column = []
        # Collect non-empty candies from top to bottom
        for y in range(BOARD_HEIGHT):
            if board[x][y] is not None:
                column.append(board[x][y])

        # Place candies back from bottom to top
        for y in range(BOARD_HEIGHT - 1, -1, -1):
            if column:
                board[x][y] = column.pop()
            else:
                board[x][y] = random.choice(ALL_CANDIES)


def drawBoard(board, firstSelection, candy_images):
    screen.fill(DARK_GRAY)

    # Draw candies
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)

            # Draw candy image
            if board[x][y] is not None:
                candy_img = candy_images[board[x][y]]
                screen.blit(candy_img, (left, top))

            # Draw grid lines
            pygame.draw.rect(screen, GRID_COLOR, (left, top, CELL_SIZE, CELL_SIZE), 1)

            # Highlight selected candy
            if (x, y) == firstSelection:
                pygame.draw.rect(screen, YELLOW, (left - 3, top - 3, CELL_SIZE + 6, CELL_SIZE + 6), 4)


def generateRandomBoard(BOARD_WIDTH, BOARD_HEIGHT):
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(random.choice(ALL_CANDIES))
        board.append(column)
    return board


def main():
    global score
    FPSCLOCK = pygame.time.Clock()

    # Load candy images
    candy_images = loadCandyImages()

    firstSelection = None
    secondSelection = None
    board = generateRandomBoard(BOARD_WIDTH, BOARD_HEIGHT)
    score = 0
    gameStarted = False

    mousex = 0
    mousey = 0

    while True:
        drawBoard(board, firstSelection, candy_images)
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    board = generateRandomBoard(BOARD_WIDTH, BOARD_HEIGHT)
                    score = 0
                    gameStarted = False

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not firstSelection and mouseClicked:
                firstSelection = (boxx, boxy)
                gameStarted = True

            if firstSelection and mouseClicked and (boxx, boxy) != firstSelection:
                secondSelection = (boxx, boxy)
                if checkValidSecondSelection(firstSelection, secondSelection):
                    # Swap candies
                    temp1 = board[firstSelection[0]][firstSelection[1]]
                    board[firstSelection[0]][firstSelection[1]] = board[secondSelection[0]][secondSelection[1]]
                    board[secondSelection[0]][secondSelection[1]] = temp1

                    firstSelection = None
                    secondSelection = None
                else:
                    # Invalid move - show message
                    invalidSurf, invalidRect = makeText("Invalid Move!", RED, WINDOW_WIDTH // 2 - 80, 10)
                    screen.blit(invalidSurf, invalidRect)
                    pygame.display.update()
                    pygame.time.wait(800)
                    firstSelection = None
                    secondSelection = None

        # Check for matches
        matches = checkBoardForMatches(board)
        if matches:
            if gameStarted:
                score += len(matches) * 10
            removeMatches(board, matches)
            drawBoard(board, firstSelection, candy_images)
            scoreSurf, scoreRect = makeText(f"Поени: {score}", WHITE, 20, 10)
            screen.blit(scoreSurf, scoreRect)
            pygame.display.update()
            pygame.time.wait(500)
            slideDownCandy(board)

        # Draw score
        scoreSurf, scoreRect = makeText(f"Поени: {score}", WHITE, 20, 10)
        screen.blit(scoreSurf, scoreRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()