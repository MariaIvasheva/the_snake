import sys
from random import randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, который представляет собой визуальный объект.
    Он содержит общие атрибуты игровых объектов.
    """

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод определяет, как объект будет отрисовываться на экране."""
        raise NotImplementedError(
            'Реализация метода определена в дочерних классах')


class Snake(GameObject):
    """Класс, описывающий отрисовку, обработку событий (нажата клавиша)
    и аспекты поведения змейки в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.next_direction = None
        self.last = None
        self.reset()

    def draw(self, surface):
        """Метод для отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pg.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        # change cells
        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змейки после нажатия
        на кнопку.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """
        Метод возвращает позицию головы змейки (первый элемент в списке
        positions).
        """
        return self.positions[0]

    def reset(self):
        """
        Метод сбрасывает змейку в начальное состояние после столкновения
        с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR, occupied_position=[]):
        super().__init__(body_color)
        self.randomize_position(occupied_position)

    def draw(self, surface):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)
        return rect

    def randomize_position(self, occupied_position=[]):
        """
        Метод устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        И проверяет, чтобы яблоко не появлялось на змейке.
        """
        while True:

            self.position = (
                randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
            )
            # Проверяем, не находится ли новая позиция яблока в змее.
            if self.position not in occupied_position:
                return self.position


def handle_keys(game_object):
    """
    Метод обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки и выйти из игры.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

            # Нажали escape, для выхода из игры.
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()


def main():
    """Основной цикл игры."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(occupied_position=snake.positions)

    while True:
        clock.tick(SPEED)

        # Основной цикл игры
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.position)

        # Проверка на столкновение змейки с собой
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw(screen)
        snake.draw(screen)

        pg.display.update()


if __name__ == "__main__":
    main()
