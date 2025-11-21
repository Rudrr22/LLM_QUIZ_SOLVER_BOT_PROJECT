# app.py

import os
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EXPECTED_SECRET = os.getenv("QUIZ_SECRET")

# Import quiz solver (we will create this in Step 3)
from quiz_solver import process_quiz_flow


# ------------------- Request Body Model --------------------

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: HttpUrl   # Validates the format of the URL


# ------------------- Create FastAPI App --------------------

app = FastAPI()


# -------------------- POST /quiz Endpoint -------------------

@app.post("/quiz")
async def quiz_endpoint(payload: QuizRequest, background_tasks: BackgroundTasks):

    # 1. SECRET VALIDATION
    if payload.secret != EXPECTED_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # 2. Set a 3-minute deadline (180 seconds)
    deadline = time.time() + 180

    # 3. Start background quiz solver
    background_tasks.add_task(
        process_quiz_flow,
        email=payload.email,
        secret=payload.secret,
        start_url=str(payload.url),
        deadline_ts=deadline
    )

    # 4. Return response IMMEDIATELY (this is required)
    return {
        "status": "accepted",
        "message": "Quiz solving started in background."
    }
