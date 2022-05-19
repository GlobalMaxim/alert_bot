from datetime import datetime
from distutils.debug import DEBUG
import mysql.connector
from mysql.connector import Error
import redis

from telegram_redis.redisPreparation import Redis_Preparation
import logging

logging.basicConfig(filename='log/database-log.txt', level=logging.DEBUG)
def connect():
    try:
        connection = mysql.connector.connect(user='admin', password='Vfrcbv19981408', port='3306', host='alerttelegrambot.cfhtqnpm0xnk.us-east-2.rds.amazonaws.com', database="alert_telegram_bot")
        return connection
    except Exception :
            logging.exception('\n'+'Connection Failed Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

def get_user(user_id):
    try:
        query = 'SELECT user_id, username, first_name, last_name, language_code, count_exec_script FROM users WHERE user_id=%s'
        atr = (user_id,)
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query, atr)
        user_data = cursor.fetchall()
        return(user_data)
    except Exception :
            logging.exception('\n'+'Get User Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    finally:
        cursor.close()
        connection.close()

def add_new_user(message):
    # user_id = message
    try:
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
        else:
            query = 'INSERT IGNORE INTO users (user_id, first_name, last_name, username, language_code, count_exec_script) VALUES (%s, %s, %s, %s, %s, 1)'
            atr = (user_id,first_name, last_name, username, language_code)
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(query, atr)
            connection.commit()
    except Exception :
            logging.exception('\n'+'Add New User Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    finally:
        cursor.close()
        connection.close()


def count_users():
    try:
        query = 'SELECT COUNT(DISTINCT user_id) from users'
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        users_count = cursor.fetchall()
        cursor.close()
        connection.close()
        return(users_count[0][0])
    except Exception :
            logging.exception('\n'+'Count All Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def count_requests():
    try:
        query = 'SELECT SUM(count_exec_script) from users where user_id not in (389837052, 2121074781)'
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        count_requests = cursor.fetchall()
        return(count_requests[0][0])
    except Exception :
            logging.exception('\n'+'Count Requests Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_new_users_from_redis_to_db():
    # try:
        r = Redis_Preparation()
        users = r.get_new_users_from_redis()

        # print(users)
        if users != None:
            users_arr = []
            for key, values in users.items():
                users_arr.append((values['user_id'], values['first_name'], values['last_name'], values['username'], values['language_code'], values['count_exec_script'], values['created_at'], values['modified_at']))
            connection = connect()
            cursor = connection.cursor()
            query = 'INSERT IGNORE INTO users (user_id, first_name, last_name, username, language_code, count_exec_script, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.executemany(query, users_arr)
            connection.commit()
            # return users_arr
        # print('adding executed')
        # return
    # except Exception as ex :
    #         print('New users exception')
    #         print(str(ex))
    #         logging.exception('\n'+'Add New Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    # finally:
    #     cursor.close()
    #     connection.close()

def add_user_updates_from_redis_to_db():
    try:
        r = Redis_Preparation()
        users = r.get_new_updates_from_redis()
        if users is not None:
            users_arr = []
            for key, values in users.items():
                users_arr.append((values['count_exec_script'], values['modified_at'],values['user_id']))
            connection = connect()
            cursor = connection.cursor()
            query = 'UPDATE users set count_exec_script = count_exec_script + %s, modified_at = %s where user_id = %s'
            cursor.executemany(query, users_arr)
            connection.commit()
            # return users_arr
    except Exception as ex :
            print(str(ex))
            logging.exception('\n'+'Add New Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    finally:
        cursor.close()
        connection.close()

def save_data():
    add_new_users_from_redis_to_db()
    print('new users saved')
    add_user_updates_from_redis_to_db()
    print('added updates')
    r = redis.Redis(db=1)
    r.delete('updates')
    r.delete('users')
    print('Cache deleted')
    
# new_users = {'389837052': {'user_id': 389837052, 'first_name': 'Maxim', 'last_name': None, 'username': 'GlobalMaxim', 'language_code': 'ru', 'count_exec_scripts': 1, 'created_at': '19-05-2022 02:12', 'modified_at': '19-05-2022 02:12'}, '2121074781': {'user_id': 2121074781, 'first_name': 'Игорь', 'last_name': None, 'username': None, 'language_code': 'ru', 'count_exec_scripts': 1, 'created_at': '19-05-2022 02:12', 'modified_at': '19-05-2022 02:12'}}

# add_new_users_from_redis_to_db()
# add_user_updates_from_redis_to_db()
# add_users_from_redis()
# count_requests()
# get_user('389837053')
# add_new_user(2147483647)