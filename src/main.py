from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base 
from .login.router import router as login_router
from .config import settings
from .model.model import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração de CORS para permitir requisições do frontend
import os
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Adicionar origem do Vercel em produção
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    allowed_origins.extend([
        f"https://{vercel_url}",
        "https://*.vercel.app",
    ])

# Adicionar domínio personalizado se existir
custom_domain = os.getenv("FRONTEND_URL")
if custom_domain:
    allowed_origins.append(custom_domain)

# Adicionar API backend
backend_url = os.getenv("BACKEND_URL")
if backend_url:
    allowed_origins.append(backend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("NODE_ENV") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

@app.get('/')
async def hello_world():
    return {"status": "DailyQuest Auth Service is running"}