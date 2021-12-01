from __future__ import annotations
import curses
import random
from current_object7 import Figura7
from current_object6 import Figura6
from current_object5 import Figura5
from current_object4 import Figura4
from current_object3 import Figura3
from current_object2 import Figura2
from current_object1 import Figura1
from typing import Union
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager_windows import ManagerWindows


class MagicCrearter:
    manager_window: ManagerWindows
    start_x: int
    start_y: int
    current_object: Union[None, Figura1, Figura2, Figura3, Figura4, Figura5, Figura6, Figura7] = None
    window: curses

    def __init__(self, manager_window: ManagerWindows):
        """
        window_magic_creater
        :param manager_window: ManagerWindows
        """
        self.window = manager_window.get_window(self)
        self.window.border(0)
        self.window.refresh()
        self.window.keypad(True)  # режим клавивиатуры
        self.start_x = 5
        self.start_y = 2
        self.current_object = None
        self.create()

    def create(self) -> Union[Figura1, Figura2, Figura3, Figura4, Figura5, Figura6, Figura7]:
        prev_obj = self.current_object
        rd = random.randint(1, 20)
        if rd == 1:
            self.current_object = Figura3(self.start_x, self.start_y, self.window)
        elif rd == 2:
            self.current_object = Figura3(self.start_x, self.start_y, self.window, 1)
        elif rd == 3:
            self.current_object = Figura3(self.start_x, self.start_y, self.window, 2)
        elif rd == 4:
            self.current_object = Figura3(self.start_x, self.start_y, self.window, 3)
        elif rd == 5:
            self.current_object = Figura1(self.start_x, self.start_y, self.window)
        elif rd == 6:
            self.current_object = Figura1(self.start_x, self.start_y, self.window, 1)
        elif rd == 7:
            self.current_object = Figura2(self.start_x, self.start_y, self.window)
        elif rd == 8:
            self.current_object = Figura2(self.start_x, self.start_y, self.window, 1)
        elif rd == 9:
            self.current_object = Figura2(self.start_x, self.start_y, self.window, 2)
        elif rd == 10:
            self.current_object = Figura2(self.start_x, self.start_y, self.window, 3)
        elif rd == 11:
            self.current_object = Figura4(self.start_x, self.start_y, self.window)
        elif rd == 12:
            self.current_object = Figura4(self.start_x, self.start_y, self.window, 1)
        elif rd == 13:
            self.current_object = Figura4(self.start_x, self.start_y, self.window, 2)
        elif rd == 14:
            self.current_object = Figura4(self.start_x, self.start_y, self.window, 3)
        elif rd == 15:
            self.current_object = Figura5(self.start_x, self.start_y, self.window)
        elif rd == 16:
            self.current_object = Figura5(self.start_x, self.start_y, self.window, 1)
        elif rd == 17:
            self.current_object = Figura6(self.start_x, self.start_y, self.window)
        elif rd == 18:
            self.current_object = Figura6(self.start_x, self.start_y, self.window, 1)
        elif rd == 19 or 20:
            self.current_object = Figura7(self.start_x, self.start_y, self.window)

        return prev_obj

    def draw(self):
        self.window.clear()
        self.current_object.draw()
        self.window.border(0)
        self.window.refresh()



