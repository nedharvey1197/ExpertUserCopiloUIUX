import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI
from routes import copilot
from routes import enriched_trials
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# ✅ Fix: add prefix so route matches frontend expectations
app.include_router(copilot.router, prefix="/copilot")
app.include_router(enriched_trials.router, prefix="/copilot")  # ✅ shared base path

# ✅ Optional: CORS support for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
