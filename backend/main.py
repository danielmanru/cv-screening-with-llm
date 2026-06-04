from fastapi import FastAPI
from app.routes import screening, websocket
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="CV Evaluation API")
app.include_router(screening.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/ws", tags=["Websockets"])

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)