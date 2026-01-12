"""
Разработка игры "Жизнь"
"""

import copy
import itertools
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """
    Класс игры GameOfLife
    """

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

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
        cell_height = self.rows
        cell_width = self.cols

        Grid = [[random.randint(0, int(randomize)) for i in range(cell_width)] for j in range(cell_height)]
        return Grid

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
        grid = self.curr_generation
        for i in itertools.product([1, -1, 0], repeat=2):
            if i != (0, 0):
                # координата соседа
                x, y = [cell[0] + i[0], cell[1] + i[1]]
                # если сосед внутри поля
                if self.rows > x >= 0 and self.cols > y >= 0:
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
        old_grid = self.curr_generation
        for i, row in enumerate(old_grid):
            for j, cell in enumerate(row):
                list_neighbors = sum(self.get_neighbours((i, j)))

                # существо умирает
                if not list_neighbors in (2,3):
                    new_grid[i][j] = 0
                # существо появляется
                elif list_neighbors == 3 and cell == 0:
                    new_grid[i][j] = 1
                # иначе выживает
                elif cell == 1:
                    new_grid[i][j] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if not self.max_generations:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(f"{filename}", "r", encoding = "utf-8") as f:
            new_grid = []
            for line in f:
                row = list(map(int, line.replace("\n", "").strip()))
                new_grid.append(row)

        rows = len(new_grid)
        cols = len(new_grid[0]) if rows > 0 else 0
        game = GameOfLife((rows, cols), randomize=False, max_generations=None)
        game.curr_generation = new_grid
        """
        for i, line in enumerate(new_grid):
            for j, symbol in enumerate(line):
                game.curr_generation[i][j] = int(symbol == 1)
                """
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding = "utf-8") as file:
            for row in self.curr_generation:
                line = "".join(str(col) for col in row)
                file.write(f"{line}\n")
