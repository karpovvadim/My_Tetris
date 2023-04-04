from __future__ import annotations
import curses
from manager_windows import ManagerWindows, ManagerWindowsStatus
from key_score import KeyScore
import json
import urllib.parse
import urllib.request
import urllib.error
import socket
from urllib.request import build_opener


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def to_json(top_dict):
    dict_json = {}
    for key, value in top_dict.items():
        dict_json[value] = key.__dict__
    return dict_json


class TopPlayers:
    manager_window: ManagerWindows()
    window: curses.window
    actual_sorted: bool
    top_dict: dict
    sorted_list: list

    def __init__(self, args):
        self.args = args
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

    @staticmethod
    def convert_to_format(sec):
        hour = sec // 3600
        sec %= 3600
        minuts = sec // 60
        sec %= 60
        return "%d:%02d:%02d" % (hour, minuts, sec)

    @staticmethod
    def convert_to_sec(str_time):
        hour = int(str_time[0:2])
        minuts = int(str_time[3:5])
        sec = minuts * 60 + int(str_time[6:])
        return sec

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
        with open("top_players.json", "w") as write_file:
            json.dump(to_json(self.top_dict), write_file, default=default, indent=4)

    def load_from_db(self, data=None):
        url = f"http://{self.args.ip}:{self.args.port}/get_top_players"  # URL, отправляющий данные
        with urllib.request.urlopen(url) as response:
            values = response.read().decode()
            data_dict = json.loads(values)

            for key, data in data_dict.items():
                time = int(TopPlayers.convert_to_sec(data[-9:-1]))
                data_tuple = data.partition(',')
                name = data_tuple[0][1:]
                score = int(data_tuple[2].partition(',')[0])
                self.top_dict[KeyScore(score, time)] = name

    def compare_result(self):
        if self.top_dict == {}:
            self.top_dict[KeyScore(self.score, self.time)] = self.name
            self.actual_sorted = False
        else:
            result_in_top = False
            sort_key = sorted(self.top_dict.keys())
            true_index = -1
            for _ in sort_key:
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

        if self.args.ip:
            self.set_request()
        else:
            self.save_to_json()
        # self.save_to_file()
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

    def set_request(self):  # установить запрос
        str_time = TopPlayers.convert_to_format(self.time)
        values = {'name': self.name,
                  'score': self.score,
                  'time': str_time}

        url = f"http://{self.args.ip}:{self.args.port}/add_new_score"  # URL - адрес, получающий данные

        data = str(json.dumps(values))

        data = data.encode('utf-8')  # данные должны быть байтами
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
            response.read()
