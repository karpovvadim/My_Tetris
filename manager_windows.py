import curses
import time
from enum import Enum


class ManagerWindowsStatus(Enum):
    RESUME = 1
    START_GAME = 2
    MENU = 3
    PAUSE = 4
    EXIT = 5
    PLAY = 6
    END_GAME = 7
    TOP_PLAYERS = 8
    INFO = 9


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class ManagerWindows(Singleton):
    window_score_timer: curses.window
    window_magic_creater: curses
    window_field: curses
    _is_init: bool = False
    game_status: ManagerWindowsStatus

    def __init__(self, depth_win=None, weight_win=None, corner_win_y=None, corner_win_x=None):
        if ManagerWindows._is_init is False:
            self.weight_win = weight_win
            self.depth_win = depth_win
            self.corner_win_y = corner_win_y
            self.corner_win_x = corner_win_x
            self.char = None

            self.window_menu = curses.newwin(13, 20, 3, 10)
            self.window_score_timer = curses.newwin(7, 12, 10, 18)
            self.window_magic_creater = curses.newwin(6, 12, 3, 18)
            self.window_field = curses.newwin(self.depth_win, self.weight_win, self.corner_win_y, self.corner_win_x)
            self.window_top_players = curses.newwin(22, 37, 1, 6)
            self.window_info = curses.newwin(20, 37, 3, 4)
            self.game_status = ManagerWindowsStatus.MENU
            ManagerWindows._is_init = True

    def run_events(self):
        if self.game_status is ManagerWindowsStatus.MENU or self.game_status is ManagerWindowsStatus.PAUSE:
            self.window_menu.refresh()
        elif self.game_status is ManagerWindowsStatus.START_GAME or self.game_status is ManagerWindowsStatus.RESUME:
            self.window_field.refresh()

        time.sleep(0.06)
        self.char = self.window_field.getch()  # получить символ
        self.passiv_window()

    def passiv_window(self):
        if self.game_status is ManagerWindowsStatus.PLAY:
            self.window_menu.clear()
            self.window_menu.refresh()
        else:
            self.window_field.clear()
            self.window_field.refresh()
            self.window_info.clear()
            self.window_info.refresh()
            self.window_top_players.clear()
            self.window_top_players.refresh()

    def get_char(self):
        return self.char

    def clear_get(self):
        """
        очистка полученных символов
        """
        while -1 != self.window_field.getch():
            pass

    def set_status(self, status):
        self.game_status = status   # установка статуса

    def get_status(self):
        return self.game_status    #  получение статуса


