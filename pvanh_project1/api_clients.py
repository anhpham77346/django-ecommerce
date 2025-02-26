import requests

BOOK_SERVICE_URL = "http://127.0.0.1:8000/book/"

def get_list_book():
    response = requests.get(BOOK_SERVICE_URL + "list/")

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch user profile"}