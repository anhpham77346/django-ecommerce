from mongoengine import Document, StringField, DateField, IntField, ObjectIdField
from bson import ObjectId

class Book(Document):
    meta = {'collection': 'book'} # Collection name in MongoDB

    id = ObjectIdField(default=ObjectId, primary_key=True)
    title = StringField(max_length=255, required=True)
    author = StringField(max_length=255, required=True)
    published_date = DateField(required=True)
    isbn = StringField(max_length=13, required=True)
    description = StringField()
    price = IntField(required=True)
    image_url = StringField(max_length=500, default="")

    def __str__(self):
        return self.title
