from django.shortcuts import render
from book.models import Book

def home(request):
    books = Book.objects()

    return render(request, 'index.html', {"books": books})
