from fastapi import FastAPI
from routes import copilot  # 👈 make sure __init__.py exists in routes/
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# ✅ Fix: add prefix so route matches frontend expectations
app.include_router(copilot.router, prefix="/copilot")

# ✅ Optional: CORS support for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)