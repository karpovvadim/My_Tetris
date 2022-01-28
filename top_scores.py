import os.path


class TopScores:
    def __init__(self, score, time):
        self.score = score
        self.time = time


"""Пример открытия файла для чтения"""


def read_file(fname):
    """
    Функция для чтения файла fname и вывода его содержимого на экран
    """
    file = open(fname, 'r')           # Открытие файла для чтения
    print('File ' + fname + ':')        # Вывод названия файла
    # Чтение содержимого файла построчно
    for line in file:
        # Вывод строки s.  Перевод строки в файле сохраняется в строке, поэтому
        # выводим без дополнительного перевода строки.
        print(line, end='')
    file.close()   # Закрытие файла


if __name__ == '__main__':       # Функция os.path.join соединяет части пути в файловой системе требуемым
    read_file(os.path.join('top_players'))  # для данной платформы разделителем
