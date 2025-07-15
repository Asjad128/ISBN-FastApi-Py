import requests

def fetch_book_title(isbn: str) -> str:
    try:
        google_resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
        return google_resp.json()['items'][0]['volumeInfo']['title']
    except Exception:
        try:
            openlib_resp = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
            return openlib_resp.json().get(f'ISBN:{isbn}', {}).get('title', '')
        except Exception:
            return ""
