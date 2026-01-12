"""
1. Добавьте возможность ставить игру на паузу и снова запускать.
2. Добавьте возможность помечать состояние клеток на игровом поле, когда игра стоит на паузе.
"""

import pygame
from pygame import K_ESCAPE, K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_r
from life import GameOfLife
from ui import UI


class GUI(UI):
    """
    Подкласс родительского класса UI для дизайна граф оболочки
    """

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        # наследование всех атрибутов класса
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        # параметры экрана
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        # запускаем экран
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

        # состояние игры
        self.paused = False
        self.running = True

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        """Запустить игру"""
        clock = pygame.time.Clock()

        while self.running:
            # проверка на нажимания
            self.events()
            # заливка экрана белым, рисуем
            if not self.paused:
                self.screen.fill(pygame.Color("white"))

            self.draw_grid()
            self.draw_lines()

            font = pygame.font.SysFont(None, 30)
            text = font.render(
                f"Поколение: {self.life.generations} | {'ПАУЗА' if self.paused else 'ИГРА'}",
                True,
                pygame.Color("black"),
            )
            self.screen.blit(text, (10, 10))

            if self.paused:
                hint = font.render(
                    "ПРОБЕЛ - играть | ЛКМ - редактировать | R - рестарт | ESC - выход",
                    True,
                    pygame.Color("darkred"),
                )
                self.screen.blit(hint, (10, self.height - 40))

            if not self.paused:
                self.life.step()
            pygame.display.update()
            clock.tick(self.speed)
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.paused = False

    def events(self) -> None:
        """
        Функция для паузы, выхода, генерации нового поля и изменения состояния клетки
        :return:
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            # если нахимается не крестик
            elif event.type == KEYDOWN:
                # при нажатии пробела меняет состояние игры на противоположное
                if event.key == K_SPACE:
                    self.paused = not self.paused
                # остановка игры при нажатии ESC
                elif event.key == K_ESCAPE:
                    self.running = False
                # генерация нового случайного поля при нажатии r
                elif event.key == K_r:
                    self.life.curr_generation = self.life.create_grid(randomize=True)
                    self.life.generations = 0
            # если игру остановили, кликнули мышкой и запустили игру --> меняем состояние клетки
            elif event.type == MOUSEBUTTONDOWN and self.paused and event.button == 1:
                # определяем координату клика
                x, y = event.pos
                col = x // self.cell_size
                row = y // self.cell_size
                # если внутри поля то меняем состояние клетки на противоположное
                if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                    self.life.curr_generation[row][col] ^= 1
