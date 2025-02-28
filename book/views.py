from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from bson import ObjectId

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookDetailView(APIView):
    def get(self, request, book_id):
        try:
            # Kiểm tra xem book_id có phải là ObjectId hợp lệ không
            if not ObjectId.is_valid(book_id):
                return Response({"error": "Invalid book ID format"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Tìm sách theo ID
            book = Book.objects.get(id=ObjectId(book_id))
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
