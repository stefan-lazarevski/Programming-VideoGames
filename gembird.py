import pygame
import sys
import random

WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
paddle_speed = 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BALL_RADIUS = 10
ball_speed_x = 4
ball_speed_y = 4
speed_increase = 0.5 #speed after each paddle kick

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
font = pygame.font.SysFont('freesansbold.ttf', 30)

clock = pygame.time.Clock()


def reset_game():
    paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT) #top, left, width, height
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    score = 0
    paused = False
    game_over = False
    return paddle, ball, 4, 4, score, paused, game_over

def main():
    paddle, ball, ball_speed_x, ball_speed_y, score, paused, game_over = reset_game()
    move_up = False
    move_down = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not game_over:
                    paused = not paused #flip the current value
                if event.key == pygame.K_r and game_over:
                    paddle, ball, ball_speed_x, ball_speed_y, score, paused, game_over = reset_game()
                #when its pressed
                if event.key == pygame.K_UP:
                    move_up = True
                elif event.key == pygame.K_DOWN:
                    move_down = True
            #when released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    move_up = False
                elif event.key == pygame.K_DOWN:
                    move_down = False
        #move up and down
        if not paused and not game_over:
            if move_up and paddle.top > 0:
                paddle.y -= paddle_speed
            if move_down and paddle.bottom < HEIGHT:
                paddle.y += paddle_speed
            #move the ball by adding velocity to the position
            ball.x += ball_speed_x
            ball.y += ball_speed_y
            #reverse the direction of the ball
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y = -ball_speed_y
            #reverse the direction of the ball
            if ball.right >= WIDTH:
                ball_speed_x = -ball_speed_x

            if ball.colliderect(paddle):
                ball_speed_x = abs(ball_speed_x) + speed_increase #positive value and bounces right ALWAYS
                ball_speed_y += random.randint(-2, 2) #random da odi
                score += 1

            if ball.left <= 0:
                game_over = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, RED, ball)

        score_surf = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(WIDTH // 2, 20))
        screen.blit(score_surf, score_rect)

        if paused and not game_over:
            pause_surf = font.render("PAUSED - Press P to Resume", True, GREEN)
            pause_rect = pause_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pause_surf, pause_rect)

        if game_over:
            gameover_surf = font.render(f"Game Over! Final Score: {score}", True, RED)
            gameover_rect = gameover_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(gameover_surf, gameover_rect)

            restart_surf = font.render("Press R to Restart", True, RED)
            restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(restart_surf, restart_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()