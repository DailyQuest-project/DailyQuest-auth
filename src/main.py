from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base 
from .login.router import router as login_router
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

@app.get('/')
async def hello_world():
    return {"status": "DailyQuest Auth Service is running"}