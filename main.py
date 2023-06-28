import pygame
from random import randrange
import config
from time import sleep

pygame.init()


class App:
    def __init__(self):
        self.CELL_COUNT = config.CELL_COUNT
        self.WIN_SIZE = config.WIN_SIZE
        self.WIN_SIZE = self.WIN_SIZE - self.WIN_SIZE % self.CELL_COUNT
        self.CELL_SIZE = self.WIN_SIZE // self.CELL_COUNT
        self.OFFSET = config.OFFSET
        self.APPLE_COUNT = config.APPLES_COUNT

        self.cell = (self.CELL_SIZE - self.OFFSET, self.CELL_SIZE - self.OFFSET)
        self.sc = pygame.display.set_mode((self.WIN_SIZE, self.WIN_SIZE))

    def create_snakes(self):
        self.snakes = [
            Snake(*config.first_snake),
            Snake(*config.second_snake),
        ]

    def create_playground(self):
        self.sc.fill((0, 0, 0))
        for x in range(0, self.WIN_SIZE, self.CELL_SIZE):
            for y in range(0, self.WIN_SIZE, self.CELL_SIZE):
                pygame.draw.rect(self.sc, (128, 128, 128),
                                 (x, y, self.CELL_SIZE - self.OFFSET, self.CELL_SIZE - self.OFFSET))

    def run(self):
        self.create_snakes()
        pygame.display.flip()
        clock = pygame.time.Clock()
        FPS = config.FPS
        alive = len(self.snakes)
        repeat, need = 0, 10
        apples = [Apple() for i in range(self.APPLE_COUNT)]
        while True:
            # Менеджер передвижения
            for cur_snake in self.snakes:
                cur_snake.control_man()
            # Передвижение
            if repeat == need:
                repeat = 0
                for cur_snake in self.snakes:
                    if cur_snake.die(self.snakes):
                        alive -= 1
                        cur_snake.alive = False
                    cur_snake.move()
            # Менеджен столкновения
            for cur_snake in self.snakes:
                for apple in apples:
                    if (cur_snake.x, cur_snake.y) == (apple.x, apple.y):
                        apple.create_apple()
                        cur_snake.length += config.LEN_PER_APPLE
                        pygame.display.set_caption(str(cur_snake.length))
            # Один ли жив
            if alive == 1:
                break
            # Отрисовка
            self.create_playground()
            for apple in apples:
                apple.draw_apple()
            for cur_snake in self.snakes:
                cur_snake.draw_snake()
            # Проверка выхода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            # Следующий цикл
            repeat += 1
            sleep(0.01)
            pygame.display.flip()

        self.game_over()

    def game_over(self):
        for i in self.snakes:
            if i.alive:
                print(f"Победил игрок {i.num}")
                break
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.run()
                    break


class Snake(App):
    def __init__(self, control, num, color, block_color, start_pos):
        super().__init__()
        self.control = {
            "W": control[0],
            "S": control[1],
            "A": control[2],
            "D": control[3]
        }
        self.direction = {"W": 1, "S": 1, "A": 1, "D": 1}
        self.new_direction = self.direction

        self.alive = True
        self.block_color = block_color
        self.num = num
        self.color = color
        self.length = 1
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.dx, self.dy = 0, 0
        self.snake_class_ray = [pygame.rect.Rect(self.x, self.y, *self.cell)]

    def move(self):
        self.x += self.dx * self.CELL_SIZE
        self.y += self.dy * self.CELL_SIZE
        if not config.WALL_DIE:
            if self.x >= self.WIN_SIZE:
                self.x = 0
            elif self.x < 0:
                self.x = self.WIN_SIZE - self.CELL_SIZE
            if self.y >= self.WIN_SIZE:
                self.y = 0
            elif self.y < 0:
                self.y = self.WIN_SIZE - self.CELL_SIZE
        self.direction = self.new_direction
        self.snake_class_ray.append(pygame.rect.Rect(self.x, self.y, *self.cell))
        self.snake_class_ray = self.snake_class_ray[-self.length:]

    def die(self, snakes_list):
        # Если змея стоит
        if self.dx == 0 and self.dy == 0:
            return False
        # если врезалась в стену
        if config.WALL_DIE:
            if self.x >= self.WIN_SIZE or self.x < 0:
                return True
            if self.y >= self.WIN_SIZE or self.y < 0:
                return True
        # Составление всех занятых блоков
        all_green_cells = []
        for i in snakes_list:
            for k in i.snake_class_ray:
                all_green_cells.append((k.x, k.y))
        # Вычисление следующего блока
        x = self.x + self.dx * self.CELL_SIZE
        y = self.y + self.dy * self.CELL_SIZE
        if x >= self.WIN_SIZE:
            x = 0
        elif x < 0:
            x = self.WIN_SIZE - self.CELL_SIZE
        if y >= self.WIN_SIZE:
            y = 0
        elif y < 0:
            y = self.WIN_SIZE - self.CELL_SIZE
        next_cell = (x, y)
        # Поиск следующего блока в массиве всех занятых блоков
        if next_cell in all_green_cells:
            return True
        return False

    def draw_snake(self):
        for cell in self.snake_class_ray:
            pygame.draw.rect(self.sc, self.block_color, cell)
        pygame.draw.rect(self.sc, self.color, self.snake_class_ray[-1])

    def control_man(self):
        keys = pygame.key.get_pressed()
        if keys[self.control["W"]] and self.direction["W"]:
            self.dx, self.dy = 0, -1
            self.new_direction = {"W": 1, "S": 0, "A": 1, "D": 1}
        elif keys[self.control["S"]] and self.direction["S"]:
            self.dx, self.dy = 0, 1
            self.new_direction = {"W": 0, "S": 1, "A": 1, "D": 1}
        elif keys[self.control["A"]] and self.direction["A"]:
            self.dx, self.dy = -1, 0
            self.new_direction = {"W": 1, "S": 1, "A": 1, "D": 0}
        elif keys[self.control["D"]] and self.direction["D"]:
            self.dx, self.dy = 1, 0
            self.new_direction = {"W": 1, "S": 1, "A": 0, "D": 1}


class Apple(App):
    def __init__(self):
        super().__init__()
        self.create_apple()

    def create_apple(self):
        self.x = randrange(0, self.WIN_SIZE, self.CELL_SIZE)
        self.y = randrange(0, self.WIN_SIZE, self.CELL_SIZE)

    def draw_apple(self):
        offset = (self.CELL_SIZE - self.OFFSET, self.CELL_SIZE - self.OFFSET)
        pygame.draw.rect(self.sc, (255, 0, 0), pygame.rect.Rect(self.x, self.y, *offset))


app = App()
while True:
    app.run()
    sleep(3)
