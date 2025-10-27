from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db as get_database
from ..model.model import User 
from ..security import criar_token_jwt, verify_password, obter_usuario_logado
from .repository import UserRepository 

router = APIRouter(
  prefix='/login',
  tags=['login'],
  responses={404: {"description": "Not found"}},
)

@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_database)):
    user = UserRepository.find_by_username(database, username=form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Nome de usuário ou senha incorretos",
          headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {
      "access_token": criar_token_jwt(user.username), 
      "token_type": "bearer",
    }

@router.get("/me") 
async def get_current_user_data(current_user: User = Depends(obter_usuario_logado)): 
  return current_user