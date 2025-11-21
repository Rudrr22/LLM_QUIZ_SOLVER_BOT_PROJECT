# parsers.py

import re


# ---------------------------------------------------------------
# Helper: extract first URL from a string
# ---------------------------------------------------------------
def extract_pdf_url(text: str):
    pdf_match = re.search(r'https?://\S+\.pdf', text)
    if pdf_match:
        return pdf_match.group(0)
    return None


def extract_csv_url(text: str):
    csv_match = re.search(r'https?://\S+\.csv', text)
    if csv_match:
        return csv_match.group(0)
    return None


# ---------------------------------------------------------------
# Extract submit URL
# ---------------------------------------------------------------
def extract_submit_url(text: str):
    submit_match = re.search(r'https?://\S+/submit\S*', text)
    if submit_match:
        return submit_match.group(0)
    return None


# ---------------------------------------------------------------
# Detect the operation (sum / count / max / min)
# ---------------------------------------------------------------
def detect_operation(text: str):
    text_lower = text.lower()

    if "sum" in text_lower:
        return "sum"
    if "count" in text_lower:
        return "count"
    if "average" in text_lower or "mean" in text_lower:
        return "average"
    if "max" in text_lower:
        return "max"
    if "min" in text_lower:
        return "min"

    return None


# ---------------------------------------------------------------
# Extract page number from text e.g. "page 2"
# ---------------------------------------------------------------
def extract_page_number(text: str):
    match = re.search(r'page\s+(\d+)', text.lower())
    if match:
        return int(match.group(1))
    return None


# ---------------------------------------------------------------
# Extract column name inside quotes: "value"
# ---------------------------------------------------------------
def extract_column_name(text: str):
    match = re.search(r'"([^"]+)"', text)
    if match:
        return match.group(1)
    return None


# ---------------------------------------------------------------
# MAIN PARSER: Generates the task dictionary
# ---------------------------------------------------------------
def parse_quiz_text(text: str):
    # Try PDF
    pdf = extract_pdf_url(text)
    submit_url = extract_submit_url(text)
    operation = detect_operation(text)
    page_num = extract_page_number(text)
    column = extract_column_name(text)

    # If PDF case detected
    if pdf:
        return {
            "type": "pdf_task",
            "file_url": pdf,
            "submit_url": submit_url,
            "operation": operation,
            "page_number": page_num,
            "column_name": column
        }

    # Try CSV case
    csv_url = extract_csv_url(text)
    if csv_url:
        return {
            "type": "csv_task",
            "file_url": csv_url,
            "submit_url": submit_url,
            "operation": operation,
            "column_name": column
        }
    
        # Detect chart task
    if "chart" in text.lower() or "plot" in text.lower():
        csv_url = extract_csv_url(text)
        return {
            "type": "chart_task",
            "file_url": csv_url,
            "submit_url": submit_url,
            "x_column": "year",   # placeholder
            "y_column": "value",  # placeholder
            "chart_type": "bar"
        }


    # If no recognizable format
    return {
        "type": "unknown",
        "raw_text": text
    }
