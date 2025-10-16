from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base # Importar Base e engine
from .login.router import router as login_router
from .config import settings

# CENTRALIZADO: Ponto único para criação das tabelas na inicialização
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

# Routers
app.include_router(login_router)

@app.get('/')
async def hello_world():
    # CORREÇÃO: Removido o acesso a atributos inexistentes
    return {"status": "DailyQuest Auth Service is running"}