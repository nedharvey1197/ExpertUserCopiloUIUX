from fastapi import FastAPI
from routes import copilot  # 👈 make sure __init__.py exists in routes/

app = FastAPI()

app.include_router(copilot.router)