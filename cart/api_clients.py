import requests

BOOK_SERVICE_URL = "http://127.0.0.1:8000/book/"

def get_book_by_id(book_id):
    response = requests.get(BOOK_SERVICE_URL + f"{book_id}/")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"error": "Book not found"}
    elif response.status_code == 400:
        return {"error": "Invalid book ID format"}
    else:
        return {"error": "Unable to fetch book details"}