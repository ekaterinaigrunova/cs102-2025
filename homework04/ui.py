"""
Базовый класс UI для игры "Жизнь".
"""

import abc

from life import GameOfLife


class UI(abc.ABC):
    "Родительский класс UI для реализации дизайна"

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        """
        Метод для реализации дизайна
        :return:
        """
        pass
