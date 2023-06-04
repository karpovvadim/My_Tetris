import argparse
import json
import psycopg2
from psycopg2 import Error
from flask import Flask, request, render_template

app = Flask(__name__)

connection = None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Change data",
        epilog="""
    run examples:
        run 'view_top_players.py'
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--db_ip', default='127.0.0.1')

    parser.add_argument('--db_port', default=5432)

    parser.add_argument('--db_user', default='postgres')

    parser.add_argument('--db_pass', default='123')

    parser.add_argument('--db_base', default='players')

    parser.add_argument('--flaskip', default='127.0.0.1')

    parser.add_argument('--flaskport', default='5000')

    return parser.parse_args()


def set_connection(db_ip, db_user, db_pass, db_base, db_port):
    global connection
    connection = psycopg2.connect(  # Подключение к существующей базе данных
        host=db_ip,
        user=db_user,
        port=db_port,
        password=db_pass,
        database=db_base
    )
    connection.autocommit = True


@app.route('/get_top_players', methods=['GET'])
def get_top_players():  # return top 10 players to My_Tetris
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT *
            FROM (SELECT ROW_NUMBER() OVER () AS num, players_sort
                FROM (SELECT name, score, time
                    FROM players ORDER BY score DESC, time)
                    AS players_sort)
                AS players_sort_num
            WHERE num < 11;
            """)
            values = dict(cursor.fetchall())

    except (Exception, Error) as _error:
        print("Ошибка при работе с PostgreSQL", _error)
    finally:
        return values


@app.route('/add_new_score', methods=['POST'])
def add_new_score():  # from My_tetris new score
    name = None
    score = None
    time = None
    if request.method == "POST":
        data = request.get_data()
        data = json.loads(data)
        print(data)
        name = data['name']
        score = data['score']
        time = data['time']

    try:
        global connection
        with connection.cursor() as cursor:  # cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO players (name, score, time)
            VALUES (%s, %s, %s)""", (name, score, time))  # Курсор для выполнения операций с базой данных

    except (Exception, Error) as _error:
        print("Ошибка при работе с PostgreSQL", _error)
    finally:
        return ''' The website value is: '''


def query_bd_players(start, end):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT *
            FROM (SELECT ROW_NUMBER() OVER () num, players_sort
                FROM (SELECT name, score, time
                    FROM players ORDER BY score DESC, time)
                    AS players_sort)
                AS players_sort_num
            WHERE num >= %s AND num <= %s;""", (start, end))
            values = cursor.fetchall()

    except (Exception, Error) as _error:
        print("Ошибка при работе с PostgreSQL", _error)
    finally:
        return values


def get_new_values(values, len_values):
    num = []
    new_values = []
    for i in range(len_values):
        num.append(str(values[i][0]))
        str_val = values[i][1]
        str_val = str_val[1:-1]
        list_val = str_val.split(",")
        new_val = num + list_val
        num = []
        new_values.append(new_val)
    return new_values


@app.route('/view_table_1', methods=['GET', 'POST'])
def view_1():
    count_lines = 10
    start = 1
    end = 0
    start_right = 0
    start_left = 0
    disabled_left = 'disabled'
    disabled_right = ''
    if request.method == 'POST':
        count_lines = request.form.get('count_lines')
        count_lines = int(count_lines)
        end = start + count_lines
    elif request.method == 'GET':
        query_right = request.args.get('query_right')
        if query_right and query_right != "":
            start = request.args.get('start_right')
            count_lines = request.args.get('count_lines')
            disabled_left = ''
        query_left = request.args.get('query_left')
        if query_left and query_left != "":
            start = request.args.get('start_left')
            count_lines = request.args.get('count_lines')
            disabled_left = ''
        count_lines = int(count_lines)
        start = int(start)
        end = start + count_lines
    val = query_bd_players(start, end)  # Получение списка из bd players
    server_message = f"Вы ввели {count_lines} строк"
    len_val = len(val)
    new_values = get_new_values(val, len_val)  # Преобразование списка в список списков
    len_new_val = len(new_values)
    end = len_new_val - 1
    start = int(start)
    if val:
        start_right = start + count_lines
        start_left = start - count_lines
        if start == 1:
            disabled_left = 'disabled'
        if len_new_val <= count_lines:
            disabled_right = 'disabled'
            end = len_new_val
    return render_template('index_1.html',
                           title="Top results",
                           start=0,
                           end=end,
                           message=new_values,
                           server_message=server_message,
                           count_lines=count_lines,
                           start_right=start_right,
                           start_left=start_left,
                           disabled_right=disabled_right,
                           disabled_left=disabled_left,
                           )


@app.route('/json-view_table', methods=['GET', 'POST'])
def view_2():
    start_count_lines = 10
    count_lines = 10
    start: int = 1
    start_right = 1
    start_left = 1
    disabled_left = 'disabled'
    disabled_right = ''
    if request.method == 'POST':
        request_data = request.get_json()
        count_lines = request_data.pop("countLines")
        start_right = request_data.pop("startRight")
        start_left = request_data.pop("startLeft")
        if start_right != 0:
            start = start_right
            end = start + count_lines
        elif start_left != 0:
            start = start_left
            end = start + count_lines
        else:
            if count_lines:
                end = start + count_lines
            else:
                end = start + start_count_lines
        server_message = f"Вы ввели {count_lines}"
    else:
        server_message = f"По умолчанию введено {start_count_lines}"
        end = start + start_count_lines
    val = query_bd_players(start, end)  # Получение списка из bd players
    len_val = len(val)
    new_values = get_new_values(val, len_val)  # Преобразование списка в список списков
    len_new_val = len(new_values)
    end = len_new_val - 1
    start = int(start)
    if val:
        start_right = start + count_lines
        start_left = start - count_lines
        if start != 1:
            disabled_left = 'enabled'
        if len_new_val <= count_lines:
            disabled_right = 'disabled'
            end = len_new_val
    return render_template('index_2.html',
                           title="Top results",
                           start=0,
                           end=end,
                           message_from_bd=new_values,
                           server_message=server_message,
                           count_lines=count_lines,
                           start_right=start_right,
                           start_left=start_left,
                           disabled_left=disabled_left,
                           disabled_right=disabled_right,
                           )


if __name__ == '__main__':
    args = parse_args()
    set_connection(args.db_ip, args.db_user, args.db_pass, args.db_base, args.db_port)
    app.run(debug=True, host=args.flaskip, port=args.flaskport)
