from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


from peewee import MySQLDatabase, Model, IntegerField, CharField, DateField

database = MySQLDatabase('satellite-user', host='localhost', port=53100, user='root', password='123456')


class User(Model):

    id = IntegerField(primary_key=True)
    username = CharField(max_length=255)
    password = CharField(max_length=1023)  # 加盐存储
    cellphone = CharField(max_length=20)
    birthday = DateField()

    class Meta:
        database = database

