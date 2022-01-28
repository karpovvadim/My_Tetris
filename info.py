from __future__ import annotations
import curses
from manager_windows import ManagerWindows, ManagerWindowsStatus


class Info:
    def __init__(self):
        self.manager_window = ManagerWindows()
        self.window = self.manager_window.window_info
        self.window.keypad(True)
        self.current_color = 10
        self.normal_color = 12
        self.current_position = 0
        self.pointer = "->"

    def exit_to_menu(self):
        self.manager_window.set_status(ManagerWindowsStatus.MENU)

    def draw(self):
        self.window.addstr(15, 2, str("Pres 'Enter' to exit the menu"), curses.color_pair(14))
        c = self.manager_window.get_char()
        if c == curses.KEY_ENTER or c == 10 or c == 13:
            self.exit_to_menu()
        self.window.addstr(1, 12, "info:", curses.color_pair(11))
        self.window.border()
        self.window.refresh()
