from django.shortcuts import render
from .api_clients import get_list_book

def home(request):
    books = get_list_book()

    return render(request, 'index.html', {"books": books})
