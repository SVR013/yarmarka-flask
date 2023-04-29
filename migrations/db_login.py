import sqlite3
# from old.db import connector, table_user
from migrations.tables import UsersT
from migrations.data_base import DataBase
def create(user, psw):
    # pattern = f'''
    #             INSERT INTO
    #                        {table_user}
    #             (user, psw)
    #                  VALUES
    #                        ('{user}', '{psw}')
    #             '''
    # cursor.execute(pattern)
    # connection.commit()
    us = DataBase(UsersT)
    us.session.add(UsersT(user=user, psw=psw))
    us.session.commit()

def readUser():
    us = DataBase(UsersT)
    return us.gettuple(us.query.one())
    # try:
    #     pattern = f'''SELECT psw, user
    #                     FROM
    #                         {table_user}
    #                     '''
    #     cursor.execute(pattern)
    #     res = cursor.fetchone()
    #     if not res:
    #         print('Пользователь не найден')
    #         return False
    #
    #     return res
    # except sqlite3.Error as e:
    #     print('Ошибка получения пароля из БД ' + str(e))

def getUser(user_id="1"):
    return readUser()
    # try:
    #     pattern = f'''SELECT id
    #                     FROM
    #                         {table_user}
    #                     '''
    #     cursor.execute(pattern)
    #     res = cursor.fetchone()
    #     if not res:
    #         print('Пользователь не найден')
    #         return False
    #     return res
    # except sqlite3.Error as e:
    #     print('Ошибка получения id из БД ' + str(e))