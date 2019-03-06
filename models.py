import datetime
import re
import random

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


def slugify(s):
    return re.sub('[^a-z0-9_\-]+', '-', s.lower())


class Entry(Model):
    title = CharField(max_length=200)
    slug = CharField(unique=True)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    learned = TextField()
    resources = TextField()
    tags = CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + "-" + str(random.randint(1, 100))
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        database = DATABASE
        order_by = ('-date',)


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User], safe=True)
    DATABASE.close()
