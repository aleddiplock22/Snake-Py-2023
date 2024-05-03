"""
Run app from here.
"""
import pygame
import sys
import random

from . import snake as snk

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
HEAD_COLOUR = (0,220,0)
TAIL_COLOUR = (25,200,25)
BERRY_COLOUR = (200, 15, 15)
BLOCK_SIZE = 20
GAME_DIM = 32
WINDOW_HEIGHT = BLOCK_SIZE*GAME_DIM
WINDOW_WIDTH = BLOCK_SIZE*GAME_DIM


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    FONT = pygame.font.SysFont("Verdana", 35)
    snake = snk.Snake()
    berry = snk.Berry(snake)
    game = snk.SnakeGame(snake)

    while True:
        pygame.event.get()
        # BACKGROUND
        SCREEN.fill(WHITE)
        drawGrid()
        # SNAKE DETAILS
        speed = 1.0 / snake.get_length().__float__()
        adding_block = False
        # SCORE
        drawScore(snake, FONT, speed)
        # BERRY DETAILS AND IMPLEMENTATION
        berry.check_consumption()
        if berry.consumption_energy:
            adding_block = True
            berry.consumption_energy = False # make sure only consume once!
        if (random.random() < 0.06) and berry.can_respawn:
            berry.respawn()
        drawBerry(berry)
        # SNAKE IMPLEMENTATION
        game.play(speed, adding_block)
        drawSnake(snake)
        
        # Q, wall-collision, or self-collision causes gameover
        if not game.active:
            pygame.quit()
            sys.exit()

        pygame.display.update()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

def drawSnake(snake : snk.Snake):
    snake_body = snake.snake_body_as_tuple_list()

    # head
    x, y = snake_body[0]
    rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, HEAD_COLOUR, rect)

    # tail
    for x, y in snake_body[1:]:
        rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, TAIL_COLOUR, rect)

def drawBerry(berry : snk.Berry):
    if berry.consumed:
        return
    loc = berry.tuple_representation()

    x, y = loc
    rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, BERRY_COLOUR, rect)

def drawScore(snake : snk.Snake, font, speed):
    length = snake.get_length()
    label = font.render(f'SCORE: {length} | SPEED: {speed:.2f}', True, (255,170,220))
    SCREEN.blit(label, (7*BLOCK_SIZE, 2*BLOCK_SIZE))


if __name__ == "__main__":
    print("Starting...")
    main()