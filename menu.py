from __future__ import annotations
import curses
from manager_windows import ManagerWindows, ManagerWindowsStatus


class Menu:

    def __init__(self):
        self.manager_window = ManagerWindows()
        self.window = self.manager_window.window_menu
        self.window.keypad(True)
        self.current_color = 10
        self.normal_color = 12
        self.disable_color = 14
        self.current_position = 1
        self.pointer = "->"
        self.inactive_resume_game = True
        self.menu_list = [(3, 2, "resume game"), (5, 2, "start new game"), (7, 2, "top ten players"),
                          (9, 2, "info"), (11, 2, "exit")]

    def resume_game(self):
        self.manager_window.set_status(ManagerWindowsStatus.RESUME)

    def start_new_game(self):
        self.manager_window.set_status(ManagerWindowsStatus.START_GAME)

    def score(self):
        self.manager_window.set_status(ManagerWindowsStatus.TOP_PLAYERS)

    def exit(self):
        self.manager_window.set_status(ManagerWindowsStatus.EXIT)

    def info(self):
        self.manager_window.set_status(ManagerWindowsStatus.INFO)

    def from_end_game(self):
        self.current_position = 1
        self.inactive_resume_game = True

    def menu_from_pause(self):
        self.current_position = 0
        self.inactive_resume_game = False

    def pointer_up(self):
        self.current_position -= 1
        if self.current_position <= 0 and self.inactive_resume_game is True:
            self.current_position = 4
        elif self.current_position <= -1 and self.inactive_resume_game is False:
            self.current_position = 4

    def pointer_down(self):
        self.current_position += 1
        if self.current_position >= len(self.menu_list):
            if self.inactive_resume_game is False:
                self.current_position = 0
            else:
                self.current_position = 1

    def draw(self):
        self.window.clear()
        c = self.manager_window.get_char()
        if c == curses.KEY_UP:
            self.pointer_up()
        elif c == curses.KEY_DOWN:
            self.pointer_down()
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            match self.current_position:
                case 0:
                    self.resume_game()
                case 1:
                    self.start_new_game()
                case 2:
                    self.score()
                case 3:
                    self.info()
                case 4:
                    self.exit()

        self.window.addstr(1, 7, "menu:", curses.color_pair(11))
        for index in range(len(self.menu_list)):
            y, x, str_val = self.menu_list[index]
            if index == self.current_position:
                temp_color = self.current_color
                x = 1
                str_val = self.pointer + " " + str_val
            elif index == 0 and self.inactive_resume_game is True:
                temp_color = self.disable_color
            else:
                temp_color = self.normal_color
            self.window.addstr(y, x, str_val, curses.color_pair(temp_color))
        self.window.border()
        self.window.refresh()
