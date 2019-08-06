from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re


def validate_username(username):
    if len(username) < 6:
        return False
    result = re.match('[0-9]|[a-z]|[A-Z]|@', username)
    if result is None:
        return False
    return True

