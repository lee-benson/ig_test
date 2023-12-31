import os
from peewee import *
from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)


class User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }
    
print("models/users executed")