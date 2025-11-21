# quiz_solver.py

import time
import io
import pandas as pd
from playwright.sync_api import sync_playwright

# Import parser + executors + utils
from parsers import parse_quiz_text
from utils import download_file, submit_answer
from executors.pdf_executor import process_pdf_task
from executors.csv_executor import process_csv_task
from executors.chart_executor import generate_chart


# ---------------------------------------------------------------
# 1. RENDER QUIZ PAGE USING PLAYWRIGHT
# ---------------------------------------------------------------

def render_quiz_page(url: str) -> str:
    """
    Opens the quiz page using Playwright (JS-rendered)
    and extracts the text from #result or entire body.
    """
    print(f"\n[PLAYWRIGHT] Loading page: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Wait for JS to finish
        page.goto(url, wait_until="networkidle")

        # Try #result first (quiz usually uses this)
        try:
            content = page.inner_text("#result")
        except:
            content = page.inner_text("body")

        browser.close()

    print("\n[PLAYWRIGHT] Extracted text:")
    print(content)
    print("\n-----------------------------------------\n")

    return content



# ---------------------------------------------------------------
# 2. MAIN QUIZ SOLVER LOOP
# ---------------------------------------------------------------

def process_quiz_flow(email, secret, start_url, deadline_ts):

    print("\n==============================")
    print("      QUIZ SOLVER STARTED     ")
    print("==============================\n")

    current_url = start_url

    while time.time() < deadline_ts:

        print(f"\n=== Solving quiz at: {current_url} ===\n")

        # --- STEP 1: Load quiz page ---
        quiz_text = render_quiz_page(current_url)

        # --- STEP 2: Parse instructions ---
        task = parse_quiz_text(quiz_text)
        print("[PARSER OUTPUT]", task)

        task_type = task.get("type")

        # ===============================
        # PDF TASK
        # ===============================
        if task_type == "pdf_task":
            print("\n[EXECUTOR] Solving PDF task...\n")

            file_bytes = download_file(task["file_url"])

            answer = process_pdf_task(
                pdf_bytes=file_bytes,
                page_number=task["page_number"],
                column_name=task["column_name"],
                operation=task["operation"]
            )

        # ===============================
        # CSV TASK
        # ===============================
        elif task_type == "csv_task":
            print("\n[EXECUTOR] Solving CSV task...\n")

            file_bytes = download_file(task["file_url"])

            answer = process_csv_task(
                csv_bytes=file_bytes,
                column_name=task["column_name"],
                operation=task["operation"]
            )

        # ===============================
        # CHART TASK
        # ===============================
        elif task_type == "chart_task":
            print("\n[EXECUTOR] Generating CHART...\n")

            file_bytes = download_file(task["file_url"])

            df = pd.read_csv(io.BytesIO(file_bytes))

            chart_b64 = generate_chart(
                df,
                task["x_column"],
                task["y_column"],
                chart_type=task["chart_type"]
            )

            answer = chart_b64

        # ===============================
        # UNKNOWN TASK
        # ===============================
        else:
            print("\n[ERROR] Unknown task type. Cannot solve.")
            print(task)
            return


        print(f"\n[ANSWER GENERATED] --> {answer}\n")


        # --- STEP 3: SUBMIT ANSWER ---
        result = submit_answer(
            url=task["submit_url"],
            email=email,
            secret=secret,
            quiz_url=current_url,
            answer=answer
        )

        print("\n[SERVER RESPONSE]")
        print(result)

        # --- STEP 4: CHECK IF NEXT URL EXISTS ---
        next_url = result.get("url")

        if next_url:
            print("\n---- Moving to next quiz URL ----\n")
            current_url = next_url
            continue

        print("\n==============================")
        print("      QUIZ COMPLETED!         ")
        print("==============================\n")
        return

    # Deadline expired
    print("\n[TIMEOUT] Exceeded 3-minute limit. Solver stopped.\n")
