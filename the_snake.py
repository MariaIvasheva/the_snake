from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, который представляет собой визуальный объект.
    Он содержит общие атрибуты игровых объектов.
    """

    def __init__(self, body_color=None):
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.body_color = body_color
        self.next_direction = None

    def draw(self):
        """Метод определяет, как объект будет отрисовываться на экране."""
        pass


class Snake(GameObject):
    """Класс, описывающий отрисовку, обработку событий (нажата клавиша)
    и аспекты поведения змейки в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1
        self.last = None

    def draw(self, surface):
        """Метод для отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.positions[0]
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
        self.positions = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def draw(self, surface):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        return rect

    def randomize_position(self):
        """
        Метод устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        self.position = (
            randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
            randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
        )
        return self.position


def handle_keys(game_object):
    """
    Метод обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Основной цикл игры
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            if apple.randomize_position() in snake.positions:
                apple.randomize_position()
                apple.draw(screen)

        # Проверка на столкновение змейки с собой
        if snake.position[0] in snake.position[2:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction !=
# RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction !=
# LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
