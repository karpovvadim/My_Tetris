import curses
from typing import Union


class Figura1:
    exist: bool
    window: curses

    def __init__(self, _x, _y, _window: curses, _orientation: int = 0, _arr: Union[None, list] = None, _score=4):
        """
        класс фигуры  ####
        :param _x:
        :param _y:
        :param _window: curses
        :param _orientation:
        :param _arr: list
        :param _score:
        """
        self.x = _x
        self.y = _y
        self.window = _window
        self.max_x = _window.getmaxyx()[1] - 2
        self.max_y = _window.getmaxyx()[0] - 2
        self.exist = True
        self.arr = _arr
        self.score = _score
        self.orientation = _orientation
        self.__fix_x_y()

    def __fix_x_y(self):
        if self.orientation == 0:
            self.x = 4
            self.y = 1
        if self.orientation == 1:
            self.y = 4

    def get_score(self):
        return self.score

    def re_init_window(self, window, x, y, arr):
        self.window = window
        self.x = x
        self.y = y
        self.arr = arr
        self.max_x = self.window.getmaxyx()[1] - 2
        self.max_y = self.window.getmaxyx()[0] - 2
        self.__fix_x_y()
        self.down(0)

    def left(self):
        if self.orientation == 0:
            if self.x > 1:
                self.x -= 1
                if self.arr[(self.y - 1) * self.max_x + self.x - 1] == 1:
                    self.x += 1

        if self.orientation == 1:
            if self.x > 1:
                self.x -= 1
                if self.arr[(self.y - 4) * self.max_x + self.x - 1] == 1:
                    self.x += 1
                if self.arr[(self.y - 3) * self.max_x + self.x - 1] == 1:
                    self.x += 1
                if self.arr[(self.y - 2) * self.max_x + self.x - 1] == 1:
                    self.x += 1
                if self.arr[(self.y - 1) * self.max_x + self.x - 1] == 1:
                    self.x += 1

    def right(self):
        if self.orientation == 0:
            if self.x < self.max_x - 3:
                self.x += 1
                if self.arr[(self.y - 1) * self.max_x + self.x + 2] == 1:
                    self.x -= 1

        if self.orientation == 1:
            if self.x < self.max_x:
                self.x += 1
                if self.arr[(self.y - 4) * self.max_x + self.x - 1] == 1:
                    self.x -= 1
                if self.arr[(self.y - 3) * self.max_x + self.x - 1] == 1:
                    self.x -= 1
                if self.arr[(self.y - 2) * self.max_x + self.x - 1] == 1:
                    self.x -= 1
                if self.arr[(self.y - 1) * self.max_x + self.x - 1] == 1:
                    self.x -= 1

    def rotate(self):
        if self.orientation == 0:
            if 3 < self.y <= self.max_y:
                self.orientation = 1
                if self.arr[(self.y - 4) * self.max_x + self.x - 1] == 1:
                    self.orientation = 0
                if self.arr[(self.y - 3) * self.max_x + self.x - 1] == 1:
                    self.orientation = 0
                if self.arr[(self.y - 2) * self.max_x + self.x - 1] == 1:
                    self.orientation = 0

        elif self.orientation == 1:
            if self.y <= self.max_y and self.x < self.max_x - 2:
                self.orientation = 0
                if self.arr[(self.y - 1) * self.max_x + self.x] == 1:
                    self.orientation = 1
                if self.arr[(self.y - 1) * self.max_x + self.x + 1] == 1:
                    self.orientation = 1
                if self.arr[(self.y - 1) * self.max_x + self.x + 2] == 1:
                    self.orientation = 1

    def down(self, down_y=1):
        if self.orientation == 0:
            if self.y < self.max_y:
                if self.arr[(self.y - (1 - down_y)) * self.max_x + self.x - 1] == 1 or \
                        self.arr[(self.y - (1 - down_y)) * self.max_x + self.x] == 1 or \
                        self.arr[(self.y - (1 - down_y)) * self.max_x + self.x + 1] == 1 or \
                        self.arr[(self.y - (1 - down_y)) * self.max_x + self.x + 2] == 1:
                    if down_y == 1:
                        self.arr[(self.y - 1) * self.max_x + self.x - 1] = 1
                        self.arr[(self.y - 1) * self.max_x + self.x] = 1
                        self.arr[(self.y - 1) * self.max_x + self.x + 1] = 1
                        self.arr[(self.y - 1) * self.max_x + self.x + 2] = 1
                    self.exist = False
                self.y += down_y
            else:
                self.arr[(self.y - 1) * self.max_x + self.x - 1] = 1
                self.arr[(self.y - 1) * self.max_x + self.x] = 1
                self.arr[(self.y - 1) * self.max_x + self.x + 1] = 1
                self.arr[(self.y - 1) * self.max_x + self.x + 2] = 1
                self.exist = False

        elif self.orientation == 1:
            if self.y < self.max_y:
                if self.arr[(self.y - (4 - down_y)) * self.max_x + self.x - 1] == 1 or \
                        self.arr[(self.y - (3 - down_y)) * self.max_x + self.x - 1] == 1 or \
                        self.arr[(self.y - (2 - down_y)) * self.max_x + self.x - 1] == 1 or \
                        self.arr[(self.y - (1 - down_y)) * self.max_x + self.x - 1] == 1:
                    if down_y == 1:
                        self.arr[(self.y - 4) * self.max_x + self.x - 1] = 1
                        self.arr[(self.y - 3) * self.max_x + self.x - 1] = 1
                        self.arr[(self.y - 2) * self.max_x + self.x - 1] = 1
                        self.arr[(self.y - 1) * self.max_x + self.x - 1] = 1
                    self.exist = False
                self.y += down_y
            else:
                self.arr[(self.y - 4) * self.max_x + self.x - 1] = 1
                self.arr[(self.y - 3) * self.max_x + self.x - 1] = 1
                self.arr[(self.y - 2) * self.max_x + self.x - 1] = 1
                self.arr[(self.y - 1) * self.max_x + self.x - 1] = 1
                self.exist = False

    def draw(self):
        if self.orientation == 0:
            self.window.addstr(self.y, self.x, "####", curses.color_pair(4))
        elif self.orientation == 1:
            self.window.addstr(self.y - 3, self.x, "#", curses.color_pair(4))
            self.window.addstr(self.y - 2, self.x, "#", curses.color_pair(4))
            self.window.addstr(self.y - 1, self.x, "#", curses.color_pair(4))
            self.window.addstr(self.y, self.x, "#", curses.color_pair(4))
