from flask import (Blueprint)

import json

with open('./data/lang/tr.json', "r") as stream:
    tr_stream = stream.read()
    tr_pack = json.loads(tr_stream)

with open('./data/lang/en.json', 'r') as stream:
    en_stream = stream.read()
    en_pack = json.loads(en_stream)


class UserRoute():
    bp = Blueprint("user", __name__, url_prefix="/user")

    @bp.route('/')
    def index() -> str:
        return "Hello from user"
