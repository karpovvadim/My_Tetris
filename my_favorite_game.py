
from magic_creater import MagicCrearter
from game_field import GameField
from score_time import ScoreTime
from manager_windows import ManagerWindows
import curses
import time


class MyFavoriteGame:
    weight_win: int
    dept_win: int
    corner_win_y: int
    corner_win_x: int
    score_timer: ScoreTime
    magic_creater: MagicCrearter
    game_field: GameField
    manager_windows: ManagerWindows

    def __init__(self, depth_win: int, weight_win: int, corner_win_y: int, corner_win_x: int):
        self.weight_win = weight_win
        self.depth_win = depth_win
        self.corner_win_y = corner_win_y
        self.corner_win_x = corner_win_x

        self.manager_windows = ManagerWindows(self.depth_win, self.weight_win, self.corner_win_y, self.corner_win_x)
        self.magic_creater = MagicCrearter(self.manager_windows)
        self.score_timer = ScoreTime(self.manager_windows)
        self.game_field = GameField(self.manager_windows, self.magic_creater, self.score_timer)

    def run_game(self):
        while True:
            self.manager_windows.run_events()
            """
            появление изображения в окне window_score_timer
            """
            self.score_timer.draw()
            """
            появление изображения в окне window_magic_creater
            """
            self.magic_creater.draw()
            """
            создание переменной, в к-рой хранится значение нажатой клавиши
            """
            kb_push = self.manager_windows.get_char()
            if kb_push == ord("p"):
                self.score_timer.timer_pause()
                self.game_field.pause_game()
            if kb_push == ord("r"):
                self.score_timer.timer_reset()
            if kb_push == ord("q"):
                break

            if self.game_field.status() == 1:
                self.game_field.draw()

            if self.game_field.status() == 5:
                self.score_timer.timer_stop()
            self.manager_windows.clear_get()


def main():
    try:
        curses.initscr()
        curses.noecho()  # отключает отображение клавиш на экране
        curses.cbreak()  # реагирование на клавиши без Enter
        curses.curs_set(0)  # невидимый курсор
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)
        time.time()
        game = MyFavoriteGame(14, 12, 3, 2)
        game.score_timer.timer_start()
        game.run_game()

    finally:
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main()
