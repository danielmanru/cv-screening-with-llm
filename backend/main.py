from fastapi import FastAPI
from app.routes.screening import router

app = FastAPI(title="CV Evaluation API")
app.include_router(router, prefix="/api/v1")