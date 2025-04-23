import pygame
from pygame.math import Vector2
import sys
import random


# snake class
class SNAKE:
    def __init__(self):
        # starting position of snake
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_segment = False

        # heads
        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        # tails
        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        # body
        self.body_vertical = pygame.image.load(
            "Graphics/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            "Graphics/body_horizontal.png"
        ).convert_alpha()

        # curved
        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        # draw each segment
        for index, segment in enumerate(self.body):
            # rectabgle for positioning
            x_pos = int(segment.x * cell_size)
            y_pos = int(segment.y * cell_size)
            segment_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # direction of face
            if index == 0:
                screen.blit(self.head, segment_rect)

            elif index == len(self.body) - 1:
                screen.blit(self.tail, segment_rect)

            else:
                prev_segment = self.body[index + 1] - segment
                next_segment = self.body[index - 1] - segment

                # in line segments
                if prev_segment.x == next_segment.x:
                    screen.blit(self.body_vertical, segment_rect)

                elif prev_segment.y == next_segment.y:
                    screen.blit(self.body_horizontal, segment_rect)

                # corners
                else:
                    if (
                        prev_segment.x == -1
                        and next_segment.y == -1
                        or prev_segment.y == -1
                        and next_segment.x == -1
                    ):
                        screen.blit(self.body_tl, segment_rect)

                    elif (
                        prev_segment.x == -1
                        and next_segment.y == 1
                        or prev_segment.y == 1
                        and next_segment.x == -1
                    ):
                        screen.blit(self.body_bl, segment_rect)

                    elif (
                        prev_segment.x == 1
                        and next_segment.y == -1
                        or prev_segment.y == -1
                        and next_segment.x == 1
                    ):
                        screen.blit(self.body_tr, segment_rect)

                    elif (
                        prev_segment.x == 1
                        and next_segment.y == 1
                        or prev_segment.y == 1
                        and next_segment.x == 1
                    ):
                        screen.blit(self.body_br, segment_rect)

    def update_head_graphics(self):
        # see the relative position of second segment to determine which way head faces
        head_dir = self.body[1] - self.body[0]
        if head_dir == Vector2(1, 0):
            self.head = self.head_left
        elif head_dir == Vector2(-1, 0):
            self.head = self.head_right
        elif head_dir == Vector2(0, 1):
            self.head = self.head_up
        elif head_dir == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_dir = self.body[-2] - self.body[-1]
        if tail_dir == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_dir == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_dir == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_dir == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_segment:
            body_copy = self.body[:]
            self.new_segment = False
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_segment(self):
        self.new_segment = True


# create the fruit class
class FRUIT:
    def __init__(self):
        self.random_pos()

    def draw_fruit(self):
        # create rectangle
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size,
        )
        # draw rectangle
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)

    def random_pos(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# main class and loop
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_eat()
        self.check_death()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_eat(self):
        if self.fruit.pos == self.snake.body[0]:
            # make new fruit
            self.fruit.random_pos()
            # extend body
            self.snake.add_segment()

    def check_death(self):
        # check is snake hits screen
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not 0 <= self.snake.body[0].y < cell_number
        ):
            self.game_over()
        # check if snake hits itself
        for segment in self.snake.body[1:]:
            if segment == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


# create a pygame instance
pygame.init()

# define cells of the grid we are moving around
cell_size = 40
cell_number = 20

# display surface
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

# Clock, keep the speed consistent
clock = pygame.time.Clock()

# load images
apple = pygame.image.load("Graphics/apple.png").convert_alpha()

# event timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

main_game = MAIN()

while True:
    # draw all our elements
    for event in pygame.event.get():
        # if exit then close pygame and any other sys functions
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    # run at 60 frames per second
    clock.tick(60)
