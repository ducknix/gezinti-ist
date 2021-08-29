#!/usr/bin/env python
# coding: utf-8

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

sqlserver = mysql.connector.connect(**auth_data)
cursor = sqlserver.cursor()


def add_user(username: str, password: str,
             phonenum: str, usermail: str) -> bool:

    sql_param = 'INSERT INTO userdata (username, email, phonenum, password, 2fact, secret_key) VALUES ("{}","{}","{}","{}",FALSE,"A");'

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
        cursor.execute(sql_param.format(data[0], data[1],
                                        data[2], data[3]))
        sqlserver.commit()

    except mysql.connector.Error as error:
        return error.errno

    return True


def check_user(email: str, phonenum: str):
    return
