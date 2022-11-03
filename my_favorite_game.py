from magic_creater import MagicCrearter
from game_field import GameField
from score_time import ScoreTime
from manager_windows import ManagerWindows, ManagerWindowsStatus
from menu import Menu
from top_players import TopPlayers
from info import Info
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
    manager_window: ManagerWindows

    def __init__(self, depth_win: int, weight_win: int, corner_win_y: int, corner_win_x: int):
        self.weight_win = weight_win
        self.depth_win = depth_win
        self.corner_win_y = corner_win_y
        self.corner_win_x = corner_win_x
        self.manager_window = ManagerWindows(self.depth_win, self.weight_win, self.corner_win_y, self.corner_win_x)
        self.magic_creater = MagicCrearter()
        self.score_timer = ScoreTime()
        self.game_field = GameField(self.magic_creater, self.score_timer)
        self.menu: Menu = Menu()
        self.top_players: TopPlayers = TopPlayers()
        #    self.top_players.load_from_file()
        self.top_players.load_from_json()
        self.info: Info = Info()
        self.score: int = 0
        self.time: int = 0

    def run_game(self):
        while True:
            self.manager_window.run_events()  # запуск событий после нажатий клавиш
            kb_push = self.manager_window.get_char()  # получение нажатий клавиш
            match self.manager_window.get_status():
                case ManagerWindowsStatus.START_GAME:
                    self.score_timer.reset()
                    self.game_field.reset()
                    self.manager_window.set_status(ManagerWindowsStatus.PLAY)

                case ManagerWindowsStatus.RESUME:
                    self.score_timer.pause_stop()
                    self.game_field.pause_stop()
                    self.manager_window.set_status(ManagerWindowsStatus.PLAY)

                case ManagerWindowsStatus.PLAY:
                    self.game_field.draw()
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
                    if kb_push == ord("p"):
                        self.manager_window.set_status(ManagerWindowsStatus.PAUSE)

                case ManagerWindowsStatus.END_GAME:
                    self.menu.from_end_game()
                    self.top_players.set_score_time(self.score_timer.get_score(), self.score_timer.get_time())
                    curses.echo()
                    curses.curs_set(1)
                    self.top_players.draw()

                case ManagerWindowsStatus.PAUSE:
                    self.score_timer.pause_start()
                    self.game_field.pause_start()
                    self.menu.menu_from_pause()
                    self.manager_window.set_status(ManagerWindowsStatus.MENU)

                case ManagerWindowsStatus.EXIT:
                    #  self.top_players.save_to_file()
                    self.top_players.save_to_json()
                    break

                case ManagerWindowsStatus.MENU:
                    self.menu.draw()

                case ManagerWindowsStatus.TOP_PLAYERS:
                    curses.noecho()
                    curses.curs_set(0)
                    self.top_players.draw()

                case ManagerWindowsStatus.INFO:
                    self.info.draw()

            self.manager_window.clear_get()  # очистка полученных символов


def main():
    try:
        curses.initscr()
        curses.noecho()  # отключает отображение клавиш на экране
        curses.cbreak()  # реагирование на клавиши без Enter
        curses.curs_set(0)  # невидимый курсор
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(3, 51, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(10, 48, curses.COLOR_BLACK)
        curses.init_pair(11, 155, curses.COLOR_BLACK)
        curses.init_pair(12, 255, curses.COLOR_BLACK)
        curses.init_pair(13, 25, curses.COLOR_BLACK)
        curses.init_pair(14, 200, curses.COLOR_BLACK)
        time.time()
        game = MyFavoriteGame(14, 12, 3, 3)
        game.run_game()

    finally:
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main()
