#!/usr/bin/env python
# coding: utf-8

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    make_response
)

from scripts import check, sql

import json
import random
import asyncio

from scripts.crypt import aes_decrypt, aes_encrypt

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
        tr_pack.update(
            {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})

        res = make_response(render_template("index.html", **tr_pack))

        return res

    @bp.route('/giris', methods=['GET', 'POST'])
    def signin() -> str:
        if request.method == 'GET':
            tr_pack.update(
                {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})

            res = make_response(render_template("login.html", **tr_pack))
            return res

        elif request.method == 'POST':
            usermail = request.form['usermail']
            password = request.form['password']

            def control():
                enc_usermail = aes_encrypt(usermail, '', '', None)
                enc_password = aes_encrypt(password, usermail, password, None)

                db_data = sql.collect_user(enc_usermail, enc_password)

                # email var mı kontrol et varsa parola uyuyor mu
                if (sql.sign_check_user(enc_usermail, enc_password)):
                    pass
                else:
                    return redirect('/giris/hata/107', 302)

                res = make_response(redirect('/user'))

                res.set_cookie("usermail", usermail)
                res.set_cookie("password", enc_password)

                res.set_cookie(
                    "username",
                    aes_decrypt(db_data[0], usermail, password, None)
                    )

                res.set_cookie(
                    "phonenum", aes_decrypt(db_data[2], usermail, password, None)
                )

                return res

            return control()

    @bp.route('/giris/hata/<errcode>')
    def signinerr(errcode) -> str:
        try:
            errmsg = tr_pack['error_msgs'][errcode]
        except KeyError:
            return redirect('/')

        tr_pack.update(
                {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        tr_pack.update({"status_msg": errmsg})

        res = make_response(render_template("login.html", **tr_pack))

        return res

    @bp.route('/kayit', methods=['GET', 'POST'])
    def signup() -> str:
        if request.method == 'GET':

            cookie_usermail = request.cookies.get('usermail')
            cookie_password = request.cookies.get('password')

            if (sql.sign_check_user(cookie_usermail, cookie_password)):
                return redirect('/user', 300)

            tr_pack.update(
                {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})

            res = make_response(render_template("register.html", **tr_pack))

            return res

        elif request.method == 'POST':
            usermail = request.form['usermail']
            password = request.form['password']
            phonenum = request.form['phonenumber']
            username = request.form['username']

            async def control():
                if (not await check.check_password(password)):
                    return redirect('/kayit/hata/100', 302)

                elif (not await check.check_phonenum(phonenum)):
                    return redirect('/kayit/hata/101', 302)

                elif (not await check.check_invalidchars(username)):
                    return redirect('/kayit/hata/102', 302)

                elif (not await check.check_invalidchars(usermail)):
                    return redirect('/kayit/hata/103', 302)

                elif (sql.reg_check_user(usermail, phonenum)):
                    return

                else:
                    # Kayıt işlemi veri tabanına geçilecek
                    if (sql.add_user(username, password, phonenum, usermail)):
                        return redirect('/kayit/basarili', 302)

                    return redirect('/kayit/hata/105', 302)

        return asyncio.run(control())

    @bp.route('/kayit/hata/<errcode>')
    def signuperr(errcode) -> str:
        try:
            errmsg = tr_pack['error_msgs'][errcode]
        except KeyError:
            return redirect('/')

        tr_pack.update(
                {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        tr_pack.update({"status_msg": errmsg})

        res = make_response(render_template("register.html", **tr_pack))

        return res

    @bp.route('/kayit/<msg>')
    def signsuccess(msg) -> str:
        try:
            msg = tr_pack["success_msg"][msg]
        except KeyError:
            redirect('/')

        tr_pack.update(
                {"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        tr_pack.update(
            {"status_msg": msg})

        res = make_response(render_template("login.html", **tr_pack))
        return res
