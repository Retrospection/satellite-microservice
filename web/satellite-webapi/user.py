from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=['GET'])
def register():
    return 'hello,world'
