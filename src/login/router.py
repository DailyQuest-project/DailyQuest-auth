# Em: src/login/router.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db as get_database
from ..model.model import User # <-- Mudança aqui
from ..security import criar_token_jwt, verify_password, obter_usuario_logado
from .repository import UserRepository # <-- Mudança aqui

router = APIRouter(
  prefix='/login',
  tags=['login'],
  responses={404: {"description": "Not found"}},
)

@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_database)):
    # Busca o usuário pelo username fornecido no formulário de login
    user = UserRepository.find_by_username(database, username=form_data.username) # <-- Mudança aqui
    
    # Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.password_hash): # <-- Mudança aqui
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Nome de usuário ou senha incorretos",
          headers={"WWW-Authenticate": "Bearer"},
        )
        
    # O token é criado com base no username, que é único
    return {
      "access_token": criar_token_jwt(user.username), # <-- Mudança aqui
      "token_type": "bearer",
    }

@router.get("/me") # <-- Renomeado para "/me" por convenção
async def get_current_user_data(current_user: User = Depends(obter_usuario_logado)): # <-- Mudança aqui
  return current_user