from __future__ import annotations
import curses
import time as lib_time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager_windows import ManagerWindows


class ScoreTime:
    manager_window: ManagerWindows
    window: curses
    score: int
    time: int
    last_time: float
    work_timer: bool

    def __init__(self, manager_window: ManagerWindows, score: int = 0, time: int = 0) -> None:
        self.window = manager_window.get_window(self)
        self.window.border(0)
        self.window.refresh()
        self.window.keypad(True)  # режим клавивиатуры
        self.score = score
        self.time = time
        self.last_time = lib_time.time()
        self.work_timer = False
        self.start_pause_time = 0
        self.pause_time = 0

    def score_destroy_line(self, n: int):     #  К-во убираемых строк, подсчёт очков по линиям
        if n == 1:
            self.score += 5
        elif n == 2:
            self.score += 15
        elif n == 3:
            self.score += 35
        elif n == 4:
            self.score += 75

    def score_from_figure(self, count: int):   #    подсчёт очков за фигуру
        self.score += count

    def timer_start(self):
        self.work_timer = True

    def timer_pause(self):
        if self.work_timer:
            self.work_timer = False
            self.start_pause_time = lib_time.time()
        elif not self.work_timer:
            self.work_timer = True
            self.pause_time += lib_time.time() - self.start_pause_time

    def timer_stop(self):
        self.work_timer = False

    def timer_reset(self):
        if not self.work_timer:
            self.work_timer = False
        else:
            self.last_time = lib_time.time() - self.pause_time
            self.window.clear()
            self.window.border(0)
            self.work_timer = True

    def draw(self):   #  Отображение очков и времени
        if self.work_timer:
            self.time = int(lib_time.time() - self.pause_time - self.last_time)
            # self.pause_time = 0
        self.window.addstr(1, 1, "Time play:", curses.color_pair(1))
        self.window.addstr(2, 1, str(self.time), curses.color_pair(1))
        self.window.addstr(4, 1, "Score:", curses.color_pair(3))
        self.window.addstr(5, 1, str(self.score), curses.color_pair(3))
        self.window.refresh()
