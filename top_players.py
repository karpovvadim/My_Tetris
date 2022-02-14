from __future__ import annotations
import curses
from manager_windows import ManagerWindows, ManagerWindowsStatus
from key_score import KeyScore
import json
from to_json import ToJson
from to_json import default


class TopPlayers:
    def __init__(self):
        self.manager_window = ManagerWindows()
        self.window = self.manager_window.window_top_players
        self.window.keypad(True)
        self.name = str()
        self.score = 0
        self.time = 0
        self.current_color = 10
        self.normal_color = 12
        self.actual_sorted = False
        self.top_dict = {}
        self.sorted_list = []
        self.to_json = ToJson(self.top_dict)

    @staticmethod
    def convert_to_format(sec):
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%d:%02d:%02d" % (hour, min, sec)

    def exit_to_menu(self):
        self.manager_window.set_status(ManagerWindowsStatus.MENU)

    def exit_to_top(self):
        self.manager_window.set_status(ManagerWindowsStatus.TOP_PLAYERS)

    def set_score_time(self, score, time):
        self.score = score
        self.time = time

    def load_from_file(self):
        try:
            with open("top_players") as filename:
                for line in filename:
                    read_str = line.split(";")
                    if read_str[2][-1] == "\n":
                        value = read_str[2][0:-1]
                    else:
                        value = read_str[2]
                    self.top_dict[KeyScore(int(read_str[0]), int(read_str[1]))] = value
        except FileNotFoundError:
            return None

    def save_to_file(self):
        with open("top_players", "w") as filename:
            for key, value in self.top_dict.items():
                write_str = str(key.score) + ";" + str(key.time) + ";" + value
                filename.write(write_str)
                filename.write("\n")

    def load_from_json(self):
        try:
            with open("top_players.json") as filename:
                file_json = json.load(filename)
                x_file = [line for line in file_json]
                for i in x_file:
                    self.top_dict[KeyScore(file_json[i]["score"], file_json[i]["time"])] = i
        except FileNotFoundError:
            return None

    def save_to_json(self):
        dict_json = self.to_json.to_json()
        with open("top_players.json", "w") as write_file:
            json.dump(dict_json, write_file, default=default, indent=4)

    def compare_result(self):
        if self.top_dict == {}:
            self.top_dict[KeyScore(self.score, self.time)] = self.name
            self.actual_sorted = False
        else:
            result_in_top = False
            sort_key = sorted(self.top_dict.keys())
            true_index = -1
            for data in sort_key:
                true_index += 1
                if true_index >= 10:
                    break
            if sort_key[true_index].score < self.score or true_index < 10:
                result_in_top = True
            elif sort_key[true_index].score == self.score and sort_key[true_index].time >= self.time:
                result_in_top = True
            if result_in_top is True:
                self.top_dict[KeyScore(self.score, self.time)] = self.name
                self.actual_sorted = False
        self.name = str()
        self.score = 0
        self.time = 0

    def draw(self):
        self.window.addstr(1, 10, "top players:", curses.color_pair(11))
        self.window.addstr(2, 1, "№  score   time      name        ", curses.COLOR_YELLOW)
        if self.actual_sorted is False:
            self.sorted_list = sorted(self.top_dict.items())
            self.actual_sorted = True
        n: int = 3
        for key, name in self.sorted_list:
            str_time = TopPlayers.convert_to_format(key.time)
            top_str = str(n - 2).ljust(3) + str(key.score).ljust(8) + str(str_time).ljust(10) + str(name).ljust(12)
            self.window.addstr(n, 1, top_str, curses.color_pair(10))
            n += 1
            if n > 12:
                break
        x_name: int = 22
        if self.manager_window.get_status() == ManagerWindowsStatus.END_GAME:
            str_time = TopPlayers.convert_to_format(self.time)
            self.window.border()
            self.window.refresh()
            self.window.addstr(n + 2, 1, str("Enter your name. Do not use ';'"), curses.color_pair(12))
            self.window.addstr(n + 3, 1, str("and no more than 12 characters."), curses.color_pair(12))
            self.window.addstr(n + 4, 1, str("And then press 'Enter'"), curses.color_pair(12))
            self.window.addstr(n + 1, 4, str(self.score), curses.color_pair(14))
            self.window.addstr(n + 1, 12, str_time, curses.color_pair(14))
            self.window.addstr(n + 1, x_name, str("____________"), curses.color_pair(14))
            self.name = str(self.window.getstr(n + 1, x_name, 12))
            while self.name.find(";") != -1:
                self.window.addstr(n + 1, x_name, str("____________"), curses.color_pair(14))
                self.window.border()
                self.window.refresh()
                self.name = str(self.window.getstr(n + 1, x_name, 12))
            self.name = self.name[2:-1]
            self.compare_result()
            self.exit_to_top()
            self.window.border()
            self.window.refresh()
        elif self.manager_window.get_status() == ManagerWindowsStatus.TOP_PLAYERS:
            self.window.addstr(15, 2, str("Press 'Enter' to exi the menu"), curses.color_pair(14))
            c = self.manager_window.get_char()
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                self.exit_to_menu()
            self.window.border()
            self.window.refresh()
