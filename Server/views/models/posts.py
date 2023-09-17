import os
from peewee import *
from dotenv import load_dotenv
from users import User

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class Post(Model):
    user = ForeignKeyField(User, backref='posts')
    caption = TextField(default='') # Empty string creates optional effect
    image_url = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db
