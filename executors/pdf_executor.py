# executors/pdf_executor.py
import io
import pdfplumber
import pandas as pd

def process_pdf_task(pdf_bytes: bytes, page_number: int, column_name: str, operation: str):
    
    # 1. Open the PDF
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page_index = page_number - 1  # pdfplumber pages are 0-indexed
        
        page = pdf.pages[page_index]
        table = page.extract_table()

    if not table:
        raise ValueError("No table found on this PDF page")

    df = pd.DataFrame(table[1:], columns=table[0])

    # 2. Clean numeric column
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")

    # 3. Perform operation
    if operation == "sum":
        return float(df[column_name].sum())
    if operation == "count":
        return int(df[column_name].count())
    if operation == "max":
        return float(df[column_name].max())
    if operation == "min":
        return float(df[column_name].min())
    if operation == "average":
        return float(df[column_name].mean())

    raise ValueError("Unsupported operation")
