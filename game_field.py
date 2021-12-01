from __future__ import annotations
import time
from magic_creater import MagicCrearter
from score_time import ScoreTime
import curses
from typing import Union
from current_object7 import Figura7
from current_object6 import Figura6
from current_object5 import Figura5
from current_object4 import Figura4
from current_object3 import Figura3
from current_object2 import Figura2
from current_object1 import Figura1
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager_windows import ManagerWindows


class GameField:
    magic_creater: MagicCrearter
    score_object: ScoreTime
    manager_window: ManagerWindows
    window: curses
    max_x: int
    max_y: int
    start_x: int
    start_y: int
    arr: list
    cur_figura: Union[Figura1, Figura2, Figura3, Figura4, Figura5, Figura6, Figura7]
    last_time: float

    def __init__(self, manager_window: ManagerWindows, magic_creater: MagicCrearter, score_object: ScoreTime):
        self.magic_creater = magic_creater
        self.score_object = score_object
        self.manager_window = manager_window
        """
        window_field
        :param window: window
        """
        self.window = manager_window.get_window(self)
        self.max_x = self.window.getmaxyx()[1]-2
        self.max_y = self.window.getmaxyx()[0]-2
        self.start_x = 5
        self.start_y = 2
        self.arr = [0 for v in range(self.max_x * self.max_y)]
        self._status = 1
        self.cur_figura = self.magic_creater.create()
        self.cur_figura.re_init_window(self.window, self.start_x, self.start_y, self.arr)
        self.window.border(0)
        self.window.keypad(True)  # режим клавивиатуры
        self.window.nodelay(True)
        self.last_time = time.time()
        self.pause_timer = 0
        self.start_pause_timer = 0

    def status(self):
        return self._status

    def pause_game(self):
        if self._status == 1:
            self._status = 3
            self.start_pause_timer = time.time()
        elif self._status == 3:
            self._status = 1
            self.pause_timer = time.time() - self.start_pause_timer

    def _work_down(self):
        """
        условие выполнение кода в блоке if, если фигура опустилась до конца, то exist is False
        """
        if self.cur_figura.exist is False:
            """
            вызов метода score_from_figure() для подсчёта очков, к-рому отдали количество очков из
            метода get_score() объекта фигуры
            """
            self.score_object.score_from_figure(self.cur_figura.get_score())
            """
            передача созданной ранее фигуры в окно game_field и создание нового объекта фигуры
            """
            self.cur_figura = self.magic_creater.create()
            """
            передача параметров полей нового объекта в window_magic_creater, window_field
            """
            self.cur_figura.re_init_window(self.window, self.start_x, self.start_y, self.arr)
            if self.cur_figura.exist is False:
                """
                Стакан полный. Игра время игры остановились.
                """
                self._status = 5

    def draw(self):
        """
        очистка изображения предыдущих клеток
        """
        self.window.clear()
        """
        условие выполнение кода в блоке if через время задержки после вызова метода draw() объекта класса GameField
        """
        if time.time() - self.pause_timer - self.last_time > 0.5:
            self.pause_timer = 0
            """
            фиксация last_time для нового отсчёта времени изменения положения по оси y
            """
            self.last_time = time.time()
            """
            вызов метода down() у текущего объекта фигуры, перемещение вниз по оси y, или остановка движения по оси y и
            изменение элементов списка self.arr с 0 на 1 соответственно фиксации положения фигуры
            """
            self.cur_figura.down()
            self._work_down()
        c = self.manager_window.get_char()
        if c == curses.KEY_LEFT:
            self.cur_figura.left()
        elif c == curses.KEY_RIGHT:
            self.cur_figura.right()
        elif c == curses.KEY_UP:
            self.cur_figura.rotate()
        elif c == curses.KEY_DOWN:
            self.cur_figura.down()
            self._work_down()
        """
        проверка и подсчёт целых строк
        """
        n = 0
        index_in = 0
        for i in range(0, len(self.arr), self.max_x):
            if sum(self.arr[i:i+self.max_x]) == self.max_x:
                n += 1
                index_in = i
                self.arr[i:i + self.max_x] = [0] * self.max_x
        """
        стирание целых строк и сдвиг вниз остальных строк
        """
        for index_out in range(index_in - self.max_x, 0, -self.max_x):
            if sum(self.arr[index_out:index_out + self.max_x]) > 0:
                self.arr[index_in:index_in + self.max_x] = self.arr[index_out:index_out + self.max_x]
                self.arr[index_out:index_out + self.max_x] = [0] * self.max_x
                index_in = index_in - self.max_x
        """
        передача (n) стёртых строк в self.score_object.score_destroy_line(), для подсчёте очков за стёртые строк
        """
        self.score_object.score_destroy_line(n)
        """
        вывод на экран игрового поля 
        """
        for i in range(len(self.arr)):
            if self.arr[i] == 1:
                self.window.addstr(i // self.max_x + 1, i % self.max_x + 1, "#", curses.color_pair(1))
        """
        вызов метода draw() у текущего объекта фигуры по коорд x и y
        """
        self.cur_figura.draw()


