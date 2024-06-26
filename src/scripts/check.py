#!/usr/bin/env python
# coding: utf-8

import re


async def check_phonenum(phonenumber: str) -> bool:
    allowed_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+']

    if (len(phonenumber) != 13):
        return False

    for i in list(phonenumber):
        if (not (i in allowed_chars)):
            return False

    return True


async def check_email(email: str) -> bool:
    domain = email.split('@')[1]

    with open('../data/mailwhitelist.txt', 'r') as fs:
        whitelist = fs.readlines()
        fs.close()

    if not (domain in whitelist):
        return False

    return True


async def check_invalidchars(var: str) -> bool:
    disallowed_chars = ['\'', '-', '=', ';', '"', '\\']

    for i in list(var):
        if i in disallowed_chars:
            return False

        return True


async def check_password(password: str) -> bool:
    p = '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&İıĞğŞşÖöÇçÜü*]).{12,128})'

    if not bool(re.match(p, password)):
        return False

    return True


def replace_char(data: str) -> str:  # kontrol edilecek
    for i in ['ç', 'ı', 'ö', 'Ö' 'ç', 'Ç', 'ş', 'Ş', 'ğ', 'Ğ', 'ü', 'Ü', 'İ', 'Ö']:
        data = data.replace(i, '#', -1)
    return data
