#!/usr/bin/env python
# coding: utf-8

from flask import (
    Blueprint,
    request,
    render_template
)

from scripts import check

import json
import random
import asyncio

with open('./data/lang/tr.json', "r") as stream:
    tr_stream = stream.read()
    tr_pack = json.loads(tr_stream)

with open('./data/lang/en.json', 'r') as stream:
    en_stream = stream.read()
    en_pack = json.loads(en_stream)


def bg_code():
    return random.choice(range(1, 16))


class IndexRouteEn():
    bp = Blueprint("en", __name__, url_prefix="/en")

    @bp.route('/')
    def index() -> str:
        en_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("index.html", **en_pack)

    @bp.route('/signin')
    def signin() -> str:
        en_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("login.html", **en_pack)

    @bp.route('/signup')
    def signup() -> str:
        en_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("register.html", **en_pack)


class IndexRoute():
    bp = Blueprint("index", __name__, url_prefix="/")
    bp.register_blueprint(IndexRouteEn.bp)

    @bp.route('/')
    def index() -> str:
        tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("index.html", **tr_pack)

    @bp.route('/giris', methods=['GET', 'POST'])
    def signin() -> str:
        if request.method == 'GET':
            tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
            return render_template("login.html", **tr_pack)
        
        elif request.method == 'POST':
            usermail = request.form['usermail']
            password = request.form['password']
            
            return usermail + " " + password

    @bp.route('/kayit', methods=['GET', 'POST'])
    def signup() -> str:
        if request.method == 'GET':
            tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
            return render_template("register.html", **tr_pack)
        
        elif request.method == 'POST':
            usermail = request.form['usermail']
            password = request.form['password']
            phonenum = request.form['phonenumber']
            username = request.form['username']
            
            async def control():
                UMOK = await check.check_email(usermail)
                UNOK = await check.check_invalidchars(username)
                PNOK = await check.check_invalidchars(phonenum)
                PNOK = await check.check_phonenum(phonenum)
                PSOK = await check.check_password(password)
                
                if (not PSOK):
                    return "Hatalı parola"
                
                elif (not PNOK):
                    return "Hatalı telefon"
                
                elif (not UNOK):
                    return "Hatalı isim"
                
                elif (not UMOK):
                    return "Hatalı kullanıcı mail"
                
                else:
                    return "All is well"
                
        return asyncio.run(control())
