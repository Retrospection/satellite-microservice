from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from flask import Flask


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    from . import user, config

    app.register_blueprint(user.bp)
    app.register_blueprint(config.bp)

    return app
