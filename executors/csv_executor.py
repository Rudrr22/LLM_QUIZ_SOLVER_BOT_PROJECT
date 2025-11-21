import pandas as pd
import io

def process_csv_task(csv_bytes: bytes, column_name: str, operation: str):

    df = pd.read_csv(io.BytesIO(csv_bytes))

    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")

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
