import random
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (150, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 250, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0,
                             32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Это базовый класс, он содержит общие атрибуты игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует базовые атрибуты объекта"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        raise NotImplementedError('Будет реализован в дочернем классе.')


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self,
                 body_color=APPLE_COLOR,
                 ):
        """Задает цвет яблока и вызывает метод"""
        super().__init__(body_color)
        self.randomize_position(occupied_cell=(self.position,))

    def randomize_position(self, occupied_cell):
        """Устанавливает начальную позицию яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cell:
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    Этот класс управляет её движением,
    отрисовкой, а также обрабатывает действия пользователя.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки."""
        head_coordinate_x, head_coordinate_y = self.get_head_position()
        first_x, first_y = self.direction
        second_x = (head_coordinate_x + first_x * GRID_SIZE) % SCREEN_WIDTH
        second_y = (head_coordinate_y + first_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head_coordinate = (second_x, second_y)
        self.positions.insert(0, new_head_coordinate)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP
                    and game_object.direction != DOWN):
                game_object.next_direction \
                    = UP
            elif (event.key == pg.K_DOWN
                  and game_object.direction != UP):
                game_object.next_direction \
                    = DOWN
            elif (event.key == pg.K_LEFT
                  and game_object.direction != RIGHT):
                game_object.next_direction \
                    = LEFT
            elif (event.key == pg.K_RIGHT
                  and game_object.direction != LEFT):
                game_object.next_direction \
                    = RIGHT


def main():
    """Происходит обновление состояний объектов."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1::]:
            snake.reset()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
