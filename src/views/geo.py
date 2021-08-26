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


class GeoRoute():
    bp = Blueprint("geo", __name__, url_prefix="/geo")

    @bp.route('/')
    def index() -> str:
        return "Hello from geo"

    @bp.route('/rota')
    def rota() -> str:
        a_pos = request.args.get('a_pos')  # Kalkış noktası
        gtype = request.args.get('gtype')  # Gidiş aracı: yaya, bisiklet, araç
