import psycopg2
from psycopg2 import Error
from flask import Flask, request, render_template

app = Flask(__name__)


def query_bd_players(start, end):
    connection = None
    try:
        connection = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="123",
            database="players"
        )
        connection.autocommit = True

        insert_query = f"SELECT * FROM (SELECT ROW_NUMBER() OVER () num, players_sort\
                       FROM (SELECT name, score, time FROM players ORDER BY score DESC, time)\
                       AS players_sort) AS players_sor_num\
                       WHERE num >= {start} AND num <= {end};"

        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            values = cursor.fetchall()

    except (Exception, Error) as _error:
        print("Ошибка при работе с PostgreSQL", _error)
    finally:
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")
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
    count_lines = 5
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
    start_count_lines = 5
    count_lines = 5
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
            disabled_left = 'anabled'
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
    app.run(debug=True, host='localhost', port=5055)
