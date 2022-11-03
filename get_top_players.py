import json
import psycopg2
from psycopg2 import Error
from flask import Flask, request

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def hello():
    connection = None
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
        connection = psycopg2.connect(     # Подключение к существующей базе данных
            host="127.0.0.1",
            user="postgres",
            password="123",
            database="players"
        )

        connection.autocommit = True

        insert_query = """ INSERT INTO players (name, score, time)
                            VALUES (%s, %s, %s)"""
        item_tuple = (name, score, time)
        with connection.cursor() as cursor:           # cursor = connection.cursor()
            cursor.execute(insert_query, item_tuple)  # Курсор для выполнения операций с базой данных

    except (Exception, Error) as _error:
        print("Ошибка при работе с PostgreSQL", _error)
    finally:
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")
        return ''' The website value is: '''


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
