from fastapi import APIRouter, HTTPException
from app.models.schema import ISBNRequest, SaveRequest
from app.services.google_books import fetch_book_title
from app.services.sheet_handler import init_sheet, save_to_sheet

router = APIRouter()

@router.get("/")
def index():
    return {"message": "FastAPI root reached"}

@router.post("/receive_isbn")
def receive_isbn(data: ISBNRequest):
    title = fetch_book_title(data.isbn)
    if not title:
        print(f"Title not found for ISBN: {data.isbn}")
        return {"isbn": data.isbn, "error": "Title not found"}
    return {"isbn": data.isbn, "title": title}

@router.post("/save_title")
def save_title(data: SaveRequest):
    if not data.isbn or not data.b_title:
        raise HTTPException(status_code=400, detail="ISBN and title required")
    init_sheet()
    save_to_sheet(data.isbn, data.b_title, data.price, data.quantity)
    return {"message": "Saved successfully"}
