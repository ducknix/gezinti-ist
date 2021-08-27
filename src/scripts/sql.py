#!/usr/bin/env python
# coding: utf-8

import mysql.connector

auth_data = {
    "user": "user",
    "password": "user",
    "host": "localhost",
    "database": "gezinti"
}

sqlserver = mysql.connector.connect(**auth_data)
cursor = sqlserver.cursor()


def add_user(username: str, password: str, phonenum: str, email: str) -> bool:

    sql_param = 'INSERT INTO userdata (username, email, phonenum, password, 2fact, secret_key) VALUES ("{}","{}","{}","{}",FALSE,"A");'

    try:
        cursor.execute(sql_param.format(username, email, phonenum, password))
        sqlserver.commit()

    except mysql.connector.Error as error:
        return error.errno

    return True


def check_user(email: str, phonenum: str):
    return
