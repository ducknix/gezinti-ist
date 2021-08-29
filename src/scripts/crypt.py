#!/usr/bin/env python
# coding: utf-8

import base64

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

salt = b'\xe7\x00<\xb4\x97\x90\xd6`v\x89\xa6R\x18\x1d\x82\xbd'
init_v = b'\xd2\xd1\xe2ys\x01\xb6>\x93\x069\x0b3^\xe6t'
count = 5000  # default: 1000000


def create_key(usermail: str, password: str):
    master_key = usermail+password  # secret key for cipher_key
    return PBKDF2(master_key, salt, 32, count=count,
                  hmac_hash_module=SHA512)  # cipher key


def aes_encrypt(data: str, usermail: str, password: str, que) -> str:
    cipher_key = create_key(usermail, password)
    aes = AES.new(cipher_key, AES.MODE_CBC, init_v)
    data = pad(data.encode('utf-8'), 32)
    enc = aes.encrypt(data)
    base = base64.b32encode(enc).decode('utf-8')
    que.put(base)
    return base


def aes_decrypt(data: str, usermail: str, password: str, que) -> str:
    cipher_key = create_key(usermail, password)
    aes = AES.new(cipher_key, AES.MODE_CBC, init_v)
    data = base64.b32decode(data, '')
    dec = aes.decrypt(data)
    base = unpad(dec, 32).decode('utf-8')
    que.put(base)
    return base
