from fastapi import FastAPI
from routes import copilot  # 👈 make sure __init__.py exists in routes/
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(copilot.router)

# ✅ Optional: CORS support for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)