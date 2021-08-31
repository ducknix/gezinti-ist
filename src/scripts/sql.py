#!/usr/bin/env python
# coding: utf-8

import sys
import scripts.crypt
import mysql.connector

from queue import Queue
from threading import Thread

auth_data = {
    "user": "user",
    "password": "user",
    "host": "localhost",
    "database": "gezinti"
}
try:
    sqlserver = mysql.connector.connect(**auth_data)
    cursor = sqlserver.cursor()
except mysql.connector.errors.InterfaceError:
    print(f"Uzak MySQL sunusuna bağlanılamıyor.")
    print(f"{auth_data['host']} adresine erişilemedi.")
    exit(1)


def add_user(username: str, password: str,
             phonenum: str, usermail: str) -> bool:

    par = 'INSERT INTO userdata (username, email, phonenum, password, 2fact, secret_key) VALUES ("{}","{}","{}","{}",FALSE,"A");'

    def crypt(username, usermail, password, phonenum):
        aque, bque, cque, dque = Queue(), Queue(), Queue(), Queue()

        usernm = Thread(target=scripts.crypt.aes_encrypt,
                        args=(username, usermail, password, aque))

        passwd = Thread(target=scripts.crypt.aes_encrypt,
                        args=(password, usermail, password, bque))

        phonen = Thread(target=scripts.crypt.aes_encrypt,
                        args=(phonenum, usermail, password, cque))

        usmail = Thread(target=scripts.crypt.aes_encrypt,
                        args=(usermail, '', '', dque))

        for i in [usernm, passwd, phonen, usmail]:
            i.start()

        for i in [usernm, passwd, phonen, usmail]:
            i.join()

        return (aque.get(), dque.get(), cque.get(), bque.get())

    data = crypt(username, usermail, password, phonenum)

    try:
        cursor.execute(par.format(data[0], data[1],
                                  data[2], data[3]))
        sqlserver.commit()

    except mysql.connector.Error as error:
        return error.errno

    return True


def reg_check_user(email: str, phonenum: str):
    return


def sign_check_user(email: str, password: str) -> bool:
    par = "SELECT * from userdata where email='{0}' and password='{1}';"
    try:
        cursor.execute(par.format(email, password))
        data = cursor.fetchall()

        if (len(data) == 0):
            return False
        return True

    except mysql.connector.Error as error:
        return error.errno


def collect_user(email: str, password: str) -> list:
    par = "SELECT * from userdata where email='{0}' and password='{1}';"
    try:
        cursor.execute(par.format(email, password))
        return cursor.fetchall()

    except mysql.connector.Error as error:
        return error.errno
