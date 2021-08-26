#!/usr/bin/env python
# coding: utf-8

from flask import (
    Blueprint,
    request,
    render_template
)


import json
import random

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
        return render_template("login.html", **en_pack)

    @bp.route('/signup')
    def signup() -> str:
        return render_template("register.html", **en_pack)


class IndexRoute():
    bp = Blueprint("index", __name__, url_prefix="/")
    bp.register_blueprint(IndexRouteEn.bp)

    @bp.route('/')
    def index() -> str:
        tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("index.html", **tr_pack)

    @bp.route('/giris')
    def signin() -> str:
        tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("login.html", **tr_pack)

    @bp.route('/kayit')
    def signup() -> str:
        tr_pack.update({"random_bg_photo": f"/public/res/bg/{bg_code()}.png"})
        return render_template("register.html", **tr_pack)
