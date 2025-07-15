import gspread
from google.oauth2.service_account import Credentials
from app.core.config import SHEET_KEY, CREDENTIALS_PATH, ROWS_PER_SHEET

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_KEY)

sheet_index = 1
row_counter = 0
worksheet = None

def get_or_create_sheet(title):
    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        print(f"Creating new sheet: {title}")
        ws = spreadsheet.add_worksheet(title=title, rows="800", cols="10")
        ws.append_row([
            "ISBN\n*COMPULSORY FIELD",
            "Product ID",
            "Product Description",
            "Category",
            "Location ID",
            "Batch /Serial Number",
            "UOM",
            "Unit Cost",
            "Price",
            "Quantity"
        ])
        return ws

def init_sheet():
    global worksheet, row_counter, sheet_index
    while True:
        title = f"Sheet{sheet_index}"
        try:
            worksheet = spreadsheet.worksheet(title)
            values = worksheet.get_all_values()
            row_counter = len(values) - 1
            if row_counter < ROWS_PER_SHEET:
                break
            sheet_index += 1
        except gspread.WorksheetNotFound:
            worksheet = get_or_create_sheet(title)
            row_counter = 0
            break

def save_to_sheet(isbn, title, price="", quantity=""):
    global worksheet, sheet_index, row_counter
    if not isbn or not title:
        return

    isbn, title, price, quantity = isbn.strip(), title.strip(), str(price).strip(), str(quantity).strip()
    try:
        new_quantity = int(quantity)
    except (ValueError, TypeError):
        new_quantity = 1

    if row_counter >= ROWS_PER_SHEET:
        sheet_index += 1
        worksheet = get_or_create_sheet(f"Sheet{sheet_index}")
        row_counter = 0

    for sheet in spreadsheet.worksheets():
        rows = sheet.get_all_values()
        for idx, row in enumerate(rows):
            if len(row) >= 3 and row[0].strip() == isbn and row[2].strip().lower() == title.lower():
                try:
                    existing_quantity = int(row[9]) if len(row) > 9 and row[9].strip().isdigit() else 0
                except ValueError:
                    existing_quantity = 0
                updated_quantity = existing_quantity + new_quantity
                sheet.update_cell(idx + 1, 10, str(updated_quantity))
                print(f"Updated quantity for ISBN {isbn} in sheet {sheet.title}")
                if price and (len(row) <= 8 or row[8].strip() != price):
                    print(f"Updating price for ISBN {isbn} in sheet {sheet.title}")
                    sheet.update_cell(idx + 1, 9, price)
                return
    new_row = [
        isbn, "", title, "", "", "", "", "", price, str(new_quantity)
    ]
    print("Adding new row to sheet", new_row)
    worksheet.append_row(new_row)
    row_counter += 1
