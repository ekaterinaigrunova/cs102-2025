"""
Прототип игры Жизнь
"""

import itertools
import random
import typing as tp

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """
    Класс для описания игры "Жизнь"
    """

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание сетки для первого раза
        self.grid: Grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.create_grid()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_grid()
            # Отрисовка линий
            self.draw_lines()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        cell_height = self.cell_height
        cell_width = self.cell_width

        out = [[random.randint(0, int(randomize)) for i in range(cell_width)] for j in range(cell_height)]
        return out

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        --   --------
        out : Cells
            Список соседних клеток.
        """
        out: Cells = []
        grid = self.grid
        for i in itertools.product([1, -1, 0], repeat=2):
            if i != (0, 0):
                # координата соседа
                x, y = [cell[0] + i[0], cell[1] + i[1]]
                # если сосед внутри поля
                if self.cell_height > x >= 0 and self.cell_width > y >= 0:
                    out.append(grid[x][y])
        return out

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(False)
        old_grid = self.grid
        for i, row in enumerate(old_grid):
            for j, cell in enumerate(row):
                list_neighbors = sum(self.get_neighbours((i, j)))

                # существо умирает
                if not (list_neighbors in [2, 3]):
                    new_grid[i][j] = 0
                # существо появляется
                elif list_neighbors == 3 and cell == 0:
                    new_grid[i][j] = 1
                # иначе выживает
                elif cell == 1:
                    new_grid[i][j] = 1

        return new_grid

"""
game = GameOfLife(320, 240, 40)
game.run()
"""