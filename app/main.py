from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schema.engine import *
import app.schema.model as model
import app.routes.user_routes as user_router
import app.routes.auth_routes as auth_router
import app.routes.task_routes as task_router


origins = [
    "http://192.168.31.35:8080",
    "http://192.168.31.36:8080",
    "http://192.168.31.37:8080",
    "http://192.168.*.*:8080",
    "http://192.168.31.68:8080",
    # "http://192.168.31.68:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


app = FastAPI()
app.include_router(router=user_router.router)
app.include_router(router=task_router.router)
app.include_router(router=auth_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model.Base.metadata.create_all(bind=engine)


@app.get("/")
async def start():
    return "Welcome to GosuDesk"