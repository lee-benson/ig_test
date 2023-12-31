import os
from peewee import *
from dotenv import load_dotenv
from users import User
from posts import Post

load_dotenv()

db = PostgresqlDatabase(
    'ig_test_devdb',
    user=os.environ.get('SUP_USER'),
    password=os.environ.get('SUP_USERPW'),
    host='localhost',
    port=5432,
)

# Remember foreignkeyfields make a many-to-one/ one-to-many relation.
# E.g. there can be multiple comments on one post and multiple comments from one user. (Many to one)


class Comment(Model):
    user = ForeignKeyField(User, backref='comments')
    post = ForeignKeyField(Post, backref='comments')
    text = TextField()
    timestamp = DateTimeField()

    class Meta:
        database = db
    
    def serialize(self):
        return {
            'id': self.id,
            'user': self.user,
            'post': self.post,
            'text': self.text,
            'timestamp': self.timestamp,
        }
    
print("models/comments executed")