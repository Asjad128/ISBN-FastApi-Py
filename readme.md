# 📚 FastAPI ISBN Book Entry Service

This project is a FastAPI-based backend service that:
- Accepts ISBN codes from clients
- Fetches the book title using Google Books and Open Library APIs
- Saves the book details into Google Sheets with proper formatting and deduplication logic

---

## Features

- ISBN to Book Title lookup (Google Books API, fallback to Open Library)
- Duplicate check before inserting to Google Sheet
- Auto-add quantity if the book already exists
- Sheet auto-rotation after 800 rows per sheet
- Google Sheets API integration via service account
- Fully modular FastAPI code structure
- Docker-compatible and production-ready

---

## Project Structure

```
fastapi_isbn_service/
├── app/
│   ├── api/              # Routes
│   ├── core/             # App configs
│   ├── models/           # Pydantic schemas
│   ├── services/         # Business logic (Google Books + Sheets)
│   └── main.py           # FastAPI app entry
├── gunicorn_conf.py      # Gunicorn prod config
├── requirements.txt
├── run.sh                # Start server script
└── README.md
```

---

## Setup Instructions

### Clone & Install Dependencies
```bash
git clone <your-repo-url>
cd fastapi_isbn_service
pip install -r requirements.txt
```

### Add Google Credentials
- Create a Google Service Account and enable **Google Sheets + Drive API**
- Download the JSON credentials file and save it as:
  ```
  path/to/your/config/file/databooks.json
  ```

###  Update Config
Edit `app/core/config.py`:
```python
SHEET_KEY = "your-google-sheet-key"
CREDENTIALS_PATH = "/absolute/path/to/databooks.json"
ROWS_PER_SHEET = 800
```

---

## Run in Development

```bash
bash run.sh
```
Then access:  
 `http://localhost:8000/`

---

##  Run with Docker

###  Build Docker Image
```bash
docker build -t fastapi-isbn-app .
```

###  Run Container
```bash
docker run -d -p 8000:8000 fastapi-isbn-app
```

---

##  Run in Production with Gunicorn

```bash
gunicorn app.main:app -c gunicorn_conf.py
```

---

## API Endpoints

### `GET /`
Check if server is running  
**Response:**
```json
{ "message": "FastAPI root reached" }
```

---

### `POST /receive_isbn`
Fetch title for an ISBN

**Request:**
```json
{ "isbn": "9780132350884" }
```

**Response:**
```json
{ "isbn": "9780132350884", "title": "Clean Code" }
```

---

### `POST /save_title`
Save book entry to Google Sheets

**Request:**
```json
{
  "isbn": "9780132350884",
  "b_title": "Clean Code",
  "price": "500",
  "quantity": "2"
}
```

**Response:**
```json
{ "message": "Saved successfully" }
```

---

##  Dependencies

- FastAPI
- Uvicorn
- gspread
- google-auth
- requests

Install all via:
```bash
pip install -r requirements.txt
```

  
---

##  Need Help?

Feel free to open an issue or reach out.
