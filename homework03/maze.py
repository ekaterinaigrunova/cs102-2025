from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

square = "■"
empty_space = " "
x_mark = "X"


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    max_y = len(grid[0]) - 1
    if choice(("up", "right")) == "up":
        if x > 1:
            grid[x - 1][y] = empty_space
        elif y < max_y - 1:
            grid[x][y + 1] = empty_space
    else:
        if y < max_y - 1:
            grid[x][y + 1] = empty_space
        elif x > 1:
            grid[x - 1][y] = empty_space

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = empty_space
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for current_cell in empty_cells:
        remove_wall(grid, current_cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = x_mark, x_mark

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == x_mark:
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    new_grid = deepcopy(grid)
    rows, cols = len(grid), len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                if x > 0 and grid[x - 1][y] == 0:
                    new_grid[x - 1][y] = k + 1
                if x < rows - 1 and grid[x + 1][y] == 0:
                    new_grid[x + 1][y] = k + 1
                if y > 0 and grid[x][y - 1] == 0:
                    new_grid[x][y - 1] = k + 1
                if y < cols - 1 and grid[x][y + 1] == 0:
                    new_grid[x][y + 1] = k + 1

    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord
    val = grid[x][y]

    if not isinstance(val, int) or val == 0:
        return None

    path = []
    rows, cols = len(grid), len(grid[0])

    while val >= 1:
        path.append((x, y))
        if val == 1:
            break

        val -= 1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == val:
                x, y = nx, ny
                break

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    neighbors = [
        (x - 1, y) if x > 0 else None,
        (x + 1, y) if x < rows - 1 else None,
        (x, y - 1) if y > 0 else None,
        (x, y + 1) if y < cols - 1 else None,
    ]

    walls = 0
    possible = sum(1 for n in neighbors if n is not None)

    for neighbor in neighbors:
        if neighbor:
            nx, ny = neighbor
            if grid[nx][ny] == square:
                walls += 1

    return walls == possible


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    doors = get_exits(grid)

    if len(doors) != 2:
        return grid, None if not doors else [doors[0]]

    start, end = doors

    if encircled_exit(grid, start):
        return grid, None

    maze = deepcopy(grid)

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == x_mark:
                maze[i][j] = 1 if (i, j) == start else 0
            elif maze[i][j] == empty_space:
                maze[i][j] = 0

    step = 1
    max_steps = len(grid) * len(grid[0])
    while maze[end[0]][end[1]] == 0 and step <= max_steps:
        maze = make_step(maze, step)
        step += 1

    if maze[end[0]][end[1]] == 0:
        return maze, None

    exit_to_enter = shortest_path(maze, end)

    if not exit_to_enter:
        return maze, None

    enter_to_exit = exit_to_enter

    return maze, enter_to_exit


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = x_mark
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
