from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from model import User
import constants
import encrypt
import logging
import jwt
import datetime


def register(username, password, cellphone, birthday):
    if User.get_or_none(username=username) is not None:
        logging.info('用户{}已存在'.format(username))
        return constants.USER_EXISTS, '用户{}已存在'.format(username), None
    try:
        user = User.create(username=username, password=encrypt.encrypt_password(password), cellphone=cellphone, birthday=birthday)
    except Exception as e:
        logging.error('创建用户{}出错'.format(username), exc_info=True)
        return constants.DATABASE_ERROR, '创建用户{}出错'.format(username), None
    if user is None:
        logging.error('创建用户{}出错'.format(username), exc_info=True)
        return constants.DATABASE_ERROR, '创建用户{}出错'.format(username), None
    return constants.OK, '创建成功'


def login(username, password):
    user = User.get_or_none(username=username)
    if user is None:
        return constants.USER_NOT_EXISTS, '用户{}不存在'.format(username), None
    if encrypt.encrypt_password(password) != user.password:
        return constants.PASSWORD_ERROR, '密码错误', None
    return constants.OK, '登录成功', {'token': _generate_jwt_token(username)}


def validate_or_refresh_token(token):
    payload = jwt.decode(token, 'satellite')
    expireTime = payload['expireTime']
    deltaTime = datetime.datetime.fromtimestamp(expireTime) - datetime.datetime.now()
    if deltaTime.total_seconds() < 0:
        return constants.TOKEN_EXPIRED, 'Token已过期', None
    if 0 < deltaTime.seconds < 10 * 60:
        return constants.TOKEN_REFRESHED, 'Token已刷新', _generate_jwt_token(payload['username'])
    return constants.OK, '有效Token'


def get_user_info(username):
    user = User.get_or_none(username=username)
    if user is None:
        return constants.USER_NOT_EXISTS, '用户{}不存在'.format(username), None
    return constants.OK, '成功', {
        'username': username,
        'cellphone': user.cellphone,
        'birthday': user.birthday
    }


def _generate_jwt_token(username):
    payload = {
        'username': username,
        'expireTime': int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    }
    return jwt.encode(payload, 'satellite').decode()

