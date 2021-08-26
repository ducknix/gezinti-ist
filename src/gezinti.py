#!/usr/bin/env python
# coding: utf-8

from flask import Flask, send_from_directory
from views import index, user, api

import os.path

settings = {
    "import_name": __name__,
    "static_url_path": "/public",
    "static_folder": "./static",
    "template_folder": "./templates",
}


def main():
    gezinti = Flask(**settings)
    gezinti.secret_key = 'secret_key4debug'

    # blueprints being registered
    gezinti.register_blueprint(blueprint=index.IndexRoute.bp)  # file: /
    gezinti.register_blueprint(blueprint=user.UserRoute.bp)  # file: /user/

    # setting favicon access route
    @gezinti.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(gezinti.root_path, 'static'),
                                   'favicon.png', mimetype='image/png')

    # application run on testing port with debug mode
    gezinti.run(host="localhost", port=8080, debug=True)


# main function - start point
if __name__ == '__main__':
    main()
