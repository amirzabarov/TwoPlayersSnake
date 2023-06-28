import pygame

# Отрисовка, окно
OFFSET = 4
CELL_COUNT = 20
WIN_SIZE = 720
WIN_SIZE = WIN_SIZE - WIN_SIZE % CELL_COUNT
FPS = 120
CELL_SIZE = WIN_SIZE // CELL_COUNT
# Игра
APPLES_COUNT = 4
LEN_PER_APPLE = 1
WALL_DIE = False
# Скорость
# Змейки
first_snake = ([pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], 1, (255, 255, 0),
               (0, 204, 102), (CELL_SIZE, CELL_SIZE))
second_snake = ([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], 2, (139, 0, 139),
                (255, 153, 51), (WIN_SIZE - CELL_SIZE*2, WIN_SIZE - CELL_SIZE*2))
