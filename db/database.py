from matplotlib.style import use
import mysql.connector
from mysql.connector import Error
# from create_table import create_table_query


def connect():
    try:
        connection = mysql.connector.connect(user='admin', password='Vfrcbv19981408', port='3306', host='alerttelegrambot.cfhtqnpm0xnk.us-east-2.rds.amazonaws.com', database="alert_telegram_bot")
        # if connection.is_connected():
        #     print('Connected!')
        return connection
    except Error as er:
        with open('database_log.txt') as f:
            f.write(er)

def get_user(user_id):
    query = 'SELECT user_id, username, first_name, last_name, language_code, count_exec_script FROM users WHERE user_id=%s'
    atr = (user_id,)
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, atr)
    user_data = cursor.fetchall()
    return(user_data)


def add_new_user(message):

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code

    if len(get_user(user_id)) > 0:
        query = 'UPDATE users SET count_exec_script = count_exec_script + 1 WHERE user_id=%s'
        apt=(user_id,)
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query, apt)
        connection.commit()
        return

    query = 'INSERT INTO users (user_id, first_name, last_name, username, language_code, count_exec_script) VALUES (%s, %s, %s, %s, %s, 1)'
    atr = (user_id,first_name, last_name, username, language_code)
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, atr)
    connection.commit()

def count_users():
    query = 'SELECT COUNT(DISTINCT user_id) from users'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    users_count = cursor.fetchall()
    return(users_count[0][0])

def count_requests():
    query = 'SELECT SUM(count_exec_script) from users where user_id not in (389837052, 2121074781)'
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    count_requests = cursor.fetchall()
    return(count_requests[0][0])

# count_requests()
# get_user('389837053')
# add_new_user()

