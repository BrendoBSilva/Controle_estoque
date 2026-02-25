import mysql.connector


def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="I6x8h5c9@",
        database="controle_estoque",
        port=3306

    )

