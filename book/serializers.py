from rest_framework import serializers
from .models import Book
from datetime import datetime

class BookSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    published_date = serializers.CharField()
    isbn = serializers.CharField(max_length=13)
    description = serializers.CharField(allow_blank=True, required=False)
    price = serializers.IntegerField()
    image_url = serializers.CharField(max_length=500, allow_blank=True, required=False)

    def to_representation(self, instance):
        """ Chuyển đổi từ MongoEngine Document sang dict """
        published_date = instance.published_date

        # Kiểm tra nếu published_date là chuỗi, thì cố gắng chuyển thành datetime
        if isinstance(published_date, str):
            try:
                published_date = datetime.strptime(published_date, "%Y-%m-%d").date()
            except ValueError:
                published_date = None  # Nếu lỗi thì giữ nguyên

        return {
            'id': str(instance.id),
            'title': instance.title,
            'author': instance.author,
            'published_date': published_date.isoformat() if published_date else None,
            'isbn': instance.isbn,
            'description': instance.description,
            'price': instance.price,
            'image_url': instance.image_url
        }
