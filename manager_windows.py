import curses
from game_field import GameField
from magic_creater import MagicCrearter
from score_time import ScoreTime
import time


class ManagerWindows:
    window_score_timer: curses
    window_magic_creater: curses
    window_field: curses

    def __init__(self, depth_win: int, weight_win: int, corner_win_y: int, corner_win_x: int):
        self.weight_win = weight_win
        self.depth_win = depth_win
        self.corner_win_y = corner_win_y
        self.corner_win_x = corner_win_x
        self.char = None

        self.window_score_timer = curses.newwin(7, 12, 10, 18)
        self.window_magic_creater = curses.newwin(6, 12, 3, 18)
        self.window_field = curses.newwin(self.depth_win, self.weight_win, self.corner_win_y, self.corner_win_x)

    def get_window(self, whom):
        window = None
        if isinstance(whom, GameField) is True:
            window = self.window_field
        elif isinstance(whom, ScoreTime) is True:
            window = self.window_score_timer
        elif isinstance(whom, MagicCrearter) is True:
            window = self.window_magic_creater
        return window

    def run_events(self):
        time.sleep(0.05)
        self.char = self.window_field.getch()  # нажать клавишу
        self.window_field.border(0)
        self.window_field.refresh()

    def get_char(self):
        return self.char

    def clear_get(self):
        while -1 != self.window_field.getch():
            pass
        self.window_field.border(0)
        self.window_field.refresh()

