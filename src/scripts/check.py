#!/usr/bin/env python
# coding: utf-8

import random

async def check_phonenum(phonenumber:str) -> bool:
    allowed_chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+']

async def check_email(email:str) -> bool:
    domain = email.split('@')[1]
    with open('../data/mailwhitelist.txt', 'r') as fs:
        whitelist = fs.readlines()
        
    if domain in whitelist:
        return True
    else:
        False

async def check_invalidchars(var:str) -> bool:
    disallowed_chars = ['\'', '-', '=', ';', '"', '\\']
    
    for i in list(var):
        if i in disallowed_chars:
            return False
        
        return True
    
async def check_password(password:str) -> bool:
    pass