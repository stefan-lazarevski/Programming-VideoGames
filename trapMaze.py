# import random, pygame, sys
# from pygame.locals import *
#
# pygame.init()
#
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600
# FPS=30
#
# GRAY = (128, 128, 128)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# WHITE = (255, 255, 255)
#
# BOARD_WIDTH = 15
# BOARD_HEIGHT = 5
#
# CELL_SIZE = 30
#
# X_MARGIN = int((WINDOW_WIDTH-(CELL_SIZE*BOARD_WIDTH))/2)
# Y_MARGIN = int((WINDOW_HEIGHT-(CELL_SIZE*BOARD_HEIGHT))/2)
#
# FONT = pygame.font.Font('freesansbold.ttf', 20)
# DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
# LEFT = 'left'
# RIGHT = 'right'
# UP = 'up'
# DOWN = 'down'
#
# def makeText(text, color, bgcolor, left, top):
#     textSurface = FONT.render(text, True, color, bgcolor)
#     textRect = textSurface.get_rect()
#     textRect.topleft = (left, top)
#     return textSurface, textRect
#
# def getLeftTopOfBox(boxx, boxy):
#     left = X_MARGIN + (boxx * CELL_SIZE)
#     top = Y_MARGIN + (boxy * CELL_SIZE)
#     return left, top
#
#
# def getBoxAtPixel(mousex, mousey):
#     for boxx in range(BOARD_WIDTH):
#         for boxy in range(BOARD_HEIGHT):
#             left, top = getLeftTopOfBox(boxx, boxy)
#             boxRect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
#             if boxRect.collidepoint(mousex, mousey):
#                 return boxx, boxy
#     return None, None
#
#
# def isValidMove(direction, player):
#     if direction == LEFT:
#         if player[0] - 1 >= 0:
#             return True
#         else:
#             return False
#     elif direction == RIGHT:
#         if player[0] + 1 < BOARD_WIDTH:
#             return True
#         else:
#             return False
#     elif direction == UP:
#         if player[1] - 1 >= 0:
#             return True
#         else:
#             return False
#     else:
#         if player[1] + 1 < BOARD_HEIGHT:
#             return True
#         else:
#             return False
#
#
# def errorMessage(text):
#     error_move_surf, error_move_rect = makeText(text, RED, GRAY, WINDOW_WIDTH / 2, 15)
#     DISPLAY.blit(error_move_surf, error_move_rect)
#     pygame.display.update()
#     pygame.time.wait(500)
#
#
# def drawBoard(player, exit, ):
#     DISPLAY.fill(GRAY)
#     for x in range(BOARD_WIDTH):
#         for y in range(BOARD_HEIGHT):
#             left, top = getLeftTopOfBox(x, y)
#             pygame.draw.rect(DISPLAY, WHITE, (left, top, CELL_SIZE, CELL_SIZE), 1)
#             if (x, y) == exit:
#                 pygame.draw.rect(DISPLAY, GREEN, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))
#             if (x, y) == player:
#                 pygame.draw.rect(DISPLAY, BLUE, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))
#
#
#
# def drawTraps(traps):
#     for x in range(BOARD_WIDTH):
#         for y in range(BOARD_HEIGHT):
#             left, top = getLeftTopOfBox(x, y)
#             if (x, y) in traps:
#                 pygame.draw.rect(DISPLAY, RED, (left + 5, top + 5, CELL_SIZE - 10, CELL_SIZE - 10))
#
#
# def main():
#     FPSCLOCK = pygame.time.Clock()
#
#     lives = 3
#     moves = 0
#     player = (1, 1)
#     traps = [(2, 2), (3, 4)]
#     exit = (10, 4)
#
#     game_state = "REVEAL"
#
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if game_state == "PLAY":
#                 if event.type == KEYDOWN:
#                     if event.key == K_ESCAPE:
#                         pygame.quit()
#                         sys.exit()
#                     if event.key == K_r:
#                         player = (0, 0)
#                         lives = 3
#                         moves = 0
#
#                     elif event.key == K_LEFT:
#                         if (player[0] - 1, player[1]) in traps:
#                             if lives == 1:
#                                 errorMessage("Game Over!")
#                                 pygame.quit()
#                                 sys.exit()
#                             else:
#                                 errorMessage("Stepped on trap!")
#                                 player = (0, 0)
#                                 lives -= 1
#                         elif isValidMove(LEFT, player):
#                             player = (player[0] - 1, player[1])
#                             moves += 1
#                         else:
#                             errorMessage("Invalid move")
#
#                     elif event.key == K_RIGHT:
#                         if (player[0] + 1, player[1]) in traps:
#                             if lives == 1:
#                                 errorMessage("Game Over!")
#                                 pygame.quit()
#                                 sys.exit()
#                             else:
#                                 errorMessage("Stepped on trap!")
#                                 player = (0, 0)
#                                 lives -= 1
#                         elif isValidMove(RIGHT, player):
#                             player = (player[0] + 1, player[1])
#                             moves += 1
#                         else:
#                             errorMessage("Invalid move")
#
#                     elif event.key == K_UP:
#                         if (player[0], player[1] - 1) in traps:
#                             if lives == 1:
#                                 errorMessage("Game Over!")
#                                 pygame.quit()
#                                 sys.exit()
#                             else:
#                                 errorMessage("Stepped on trap!")
#                                 player = (0, 0)
#                                 lives -= 1
#                         elif isValidMove(UP, player):
#                             player = (player[0], player[1] - 1)
#                             moves += 1
#                         else:
#                             errorMessage("Invalid move")
#
#                     elif event.key == K_DOWN:
#                         if (player[0], player[1] + 1) in traps:
#                             if lives == 1:
#                                 errorMessage("Game Over!")
#                                 pygame.quit()
#                                 sys.exit()
#                             else:
#                                 errorMessage("Stepped on trap!")
#                                 player = (0, 0)
#                                 lives -= 1
#                         elif isValidMove(DOWN, player):
#                             player = (player[0], player[1] + 1)
#                             moves += 1
#                         else:
#                             errorMessage("Invalid move")
#             else:
#                 drawBoard(player, exit)
#                 drawTraps(traps)
#                 pygame.display.update()
#                 pygame.time.wait(1000)
#                 game_state = "PLAY"
#
#         drawBoard(player, exit)
#         pygame.display.update()
#         FPSCLOCK.tick(FPS)
#
#
#
# if __name__ == "__main__":
#     main()


import random, pygame, sys
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30

GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_WIDTH = 15
BOARD_HEIGHT = 5

CELL_SIZE = 30

X_MARGIN = int((WINDOW_WIDTH - (CELL_SIZE * BOARD_WIDTH)) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (CELL_SIZE * BOARD_HEIGHT)) / 2)

FONT = pygame.font.Font('freesansbold.ttf', 20)
BIG_FONT = pygame.font.Font('freesansbold.ttf', 48)
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

def makeText(text, color, bgcolor, left, top):
    textSurface = FONT.render(text, True, color, bgcolor)
    textRect = textSurface.get_rect()
    textRect.topleft = (int(left), int(top))
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


def isValidMove(direction, player):
    if direction == LEFT:
        return player[0] - 1 >= 0
    elif direction == RIGHT:
        return player[0] + 1 < BOARD_WIDTH
    elif direction == UP:
        return player[1] - 1 >= 0
    else:
        return player[1] + 1 < BOARD_HEIGHT


def errorMessage(text):
    # Small temporary message near top center
    error_move_surf, error_move_rect = makeText(text, RED, GRAY, WINDOW_WIDTH / 2 - 80, 15)
    DISPLAY.blit(error_move_surf, error_move_rect)
    pygame.display.update()
    pygame.time.wait(500)


def drawBoard(player, exit):
    DISPLAY.fill(GRAY)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)
            pygame.draw.rect(DISPLAY, WHITE, (left, top, CELL_SIZE, CELL_SIZE), 1)
            if (x, y) == exit:
                pygame.draw.rect(DISPLAY, GREEN, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))
            if (x, y) == player:
                pygame.draw.rect(DISPLAY, BLUE, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))


def drawTraps(traps):
    # Only used in REVEAL state in the original code; kept same behavior
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)
            if (x, y) in traps:
                pygame.draw.rect(DISPLAY, RED, (left + 5, top + 5, CELL_SIZE - 10, CELL_SIZE - 10))


# def draw_hud(moves, lives):
#     # Draw moves and lives at top-left
#     moves_surf, moves_rect = makeText(f"Moves: {moves}", BLACK, GRAY, 10, 5)
#     DISPLAY.blit(moves_surf, moves_rect)
#     lives_surf, lives_rect = makeText(f"Lives: {lives}", BLACK, GRAY, 10, 30)
#     DISPLAY.blit(lives_surf, lives_rect)
#
#
# def draw_center_message(text, color):
#     surf = BIG_FONT.render(text, True, color)
#     rect = surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
#     DISPLAY.blit(surf, rect)


def main():
    FPSCLOCK = pygame.time.Clock()

    lives = 3
    moves = 0
    player = (1, 1)
    # example traps; you can randomize later if you want
    traps = [(2, 2), (3, 4)]
    exit = (10, 4)

    game_state = "REVEAL"  # shows traps briefly, then switches to PLAY

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Handle keys that are allowed in any state
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_r:
                    # restart game (resets everything)
                    lives = 3
                    moves = 0
                    player = (1, 1)
                    game_state = "REVEAL"
                    # optionally you could reshuffle traps here
                    continue

            # Only handle movement when in PLAY state
            if game_state == "PLAY":
                if event.type == KEYDOWN:
                    # Movement handling with unified logic to avoid repetition
                    moved = False
                    next_pos = player
                    if event.key == K_LEFT:
                        next_pos = (player[0] - 1, player[1])
                        if not isValidMove(LEFT, player):
                            errorMessage("Invalid move")
                            continue
                        moved = True
                    elif event.key == K_RIGHT:
                        next_pos = (player[0] + 1, player[1])
                        if not isValidMove(RIGHT, player):
                            errorMessage("Invalid move")
                            continue
                        moved = True
                    elif event.key == K_UP:
                        next_pos = (player[0], player[1] - 1)
                        if not isValidMove(UP, player):
                            errorMessage("Invalid move")
                            continue
                        moved = True
                    elif event.key == K_DOWN:
                        next_pos = (player[0], player[1] + 1)
                        if not isValidMove(DOWN, player):
                            errorMessage("Invalid move")
                            continue
                        moved = True

                    if moved:
                        # Apply the move
                        player = next_pos
                        moves += 1

                        # If stepped on trap:
                        if player in traps:
                            lives -= 1
                            if lives <= 0:
                                # Game over: stop accepting moves, show message
                                game_state = "GAMEOVER"
                            else:
                                # Reset player position to start after trap
                                player = (1, 1)
                                # brief feedback
                                errorMessage("Stepped on trap!")
                        # If reached exit:
                        if player == exit and game_state != "GAMEOVER":
                            game_state = "VICTORY"

        # Draw everything each frame
        drawBoard(player, exit)

        # If we are still revealing traps, show them for 1 second then switch to PLAY
        if game_state == "REVEAL":
            drawTraps(traps)
            pygame.display.update()
            pygame.time.wait(1000)
            game_state = "PLAY"
            # continue to next frame to show PLAY immediately

        # # Draw HUD regardless of state
        # draw_hud(moves, lives)
        #
        # # If game over or victory, overlay centered message
        # if game_state == "GAMEOVER":
        #     draw_center_message("Game Over!", RED)
        # elif game_state == "VICTORY":
        #     draw_center_message("Victory!", GREEN)

        # Draw moves at top-left
        moves_surf = FONT.render(f"Moves: {moves}", True, BLACK, GRAY)
        DISPLAY.blit(moves_surf, (10, 5))

        # Draw lives at top-left below moves
        lives_surf = FONT.render(f"Lives: {lives}", True, BLACK, GRAY)
        DISPLAY.blit(lives_surf, (10, 30))

        # Draw game over or victory messages in the center
        if game_state == "GAMEOVER":
            gameover_surf = BIG_FONT.render("Game Over!", True, RED)
            gameover_rect = gameover_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            DISPLAY.blit(gameover_surf, gameover_rect)
        elif game_state == "VICTORY":
            victory_surf = BIG_FONT.render("Victory!", True, GREEN)
            victory_rect = victory_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            DISPLAY.blit(victory_surf, victory_rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
