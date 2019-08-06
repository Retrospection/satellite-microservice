from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import zerorpc
import service
import yaml
import logging
from logging.config import dictConfig
import os
import consul


def register(server_name, ip, port):
    c = consul.Consul()
    print(f"开始注册服务{server_name}")
    check = consul.Check.tcp(ip, port, "10s")
    c.agent.service.register(server_name, f"{server_name}-{ip}-{port}", address=ip, port=port, check=check)
    print(f"注册服务{server_name}成功")


def unregister(server_name, ip, port):
    c = consul.Consul()
    print(f"开始退出服务{server_name}")
    c.agent.service.deregister(f'{server_name}-{ip}-{port}')


class UserRpcServer(object):

    def register(self, username, password, cellphone, birthday):
        return service.register(username, password, cellphone, birthday)

    def login(self, username, password):
        return service.login(username, password)

    def validate_or_refresh_token(self, token):
        return service.validate_or_refresh_token(token)

    def get_user_info(self, username):
        return service.get_user_info(username)


def setup_logging(default_path='logger.yaml', default_level=logging.INFO):
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        print('the input path doesn\'t exist')


def main():
    setup_logging()
    server = zerorpc.Server(UserRpcServer())
    server.bind('tcp://0.0.0.0:2531')
    server.run()


if __name__ == '__main__':
    try:
        register('user-server', 'localhost', 2531)
        main()
    finally:
        unregister('user-server', 'localhost', 2531)
