# executors/chart_executor.py

import io
import base64
import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(data: pd.DataFrame, x_col: str, y_col: str, chart_type="bar"):
    """
    Creates a chart from a DataFrame and returns a base64-encoded PNG image.
    """

    plt.figure(figsize=(8, 5))

    if chart_type == "bar":
        plt.bar(data[x_col], data[y_col])
    elif chart_type == "line":
        plt.plot(data[x_col], data[y_col])
    elif chart_type == "scatter":
        plt.scatter(data[x_col], data[y_col])
    else:
        raise ValueError("Unsupported chart type")

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type.capitalize()} Chart of {y_col} vs {x_col}")

    # Save plot to bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode to base64
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")

    plt.close()  # free memory

    return encoded_image
