from __future__ import annotations
import curses
import time as lib_time
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from manager_windows import ManagerWindows


def convert_to_format(sec):
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    return "%d:%02d:%02d" % (hour, minutes, sec)


class ScoreTime:
    manager_window: ManagerWindows
    window: curses
    score: int
    time: int
    last_time: float
    _status: bool

    def __init__(self, score: int = 0, time: int = 0) -> None:
        self.window = ManagerWindows().window_score_timer
        self.score = score
        self.time = time
        self.last_time = lib_time.time()
        self.start_pause_timer = 0
        self.pause_timer = 0

    def score_destroy_line(self, n: int):  # К-во убираемых строк, подсчёт очков по линиям
        if n == 1:
            self.score += 5
        elif n == 2:
            self.score += 15
        elif n == 3:
            self.score += 35
        elif n == 4:
            self.score += 75

    def score_from_figure(self, count: int):  # подсчёт очков за фигуру
        self.score += count

    def get_score(self):
        return self.score

    def get_time(self):
        return self.time

    def pause_start(self):
        self.start_pause_timer = lib_time.time()

    def pause_stop(self):
        self.pause_timer += lib_time.time() - self.start_pause_timer

    def reset(self):
        self.last_time = lib_time.time()
        self.pause_timer = 0
        self.score = 0

    def draw(self):  # Отображение очков и времени
        self.window.clear()
        str_time = convert_to_format(self.time)
        self.time = int(lib_time.time() - self.pause_timer - self.last_time)
        self.window.addstr(1, 1, "Time play:", curses.color_pair(1))
        self.window.addstr(2, 1, str_time, curses.color_pair(1))
        self.window.addstr(4, 1, "Score:", curses.color_pair(3))
        self.window.addstr(5, 1, str(self.score), curses.color_pair(3))
        self.window.border()
        self.window.refresh()
