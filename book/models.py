from mongoengine import Document, StringField, DateField, IntField

class Book(Document):
    title = StringField(max_length=255, required=True)
    author = StringField(max_length=255, required=True)
    published_date = DateField(required=True)
    isbn = StringField(max_length=13, required=True)
    description = StringField()
    price = IntField(required=True)

    def __str__(self):
        return self.title
