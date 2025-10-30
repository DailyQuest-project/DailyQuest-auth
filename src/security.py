import os
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .database import get_db as get_database
from .login.repository import UserRepository 
from .model.model import User 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

authSchema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv('SECRET_KEY', 'dailyquestkey')
ALGORITHM="HS512"
ACCESS_TOKEN_EXPIRE_HOURS = 1

def criar_token_jwt(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_password(password: str, hashed_password: str) -> bool:
    # Truncar senha para 72 bytes se necessário (limite do bcrypt)
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password: str) -> str:
    # Truncar senha para 72 bytes se necessário (limite do bcrypt)
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def obter_usuario_logado(database: Session = Depends(get_database), token: str = Depends(authSchema)) -> User:
    try:
        subject = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub')
        if subject is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

    user = UserRepository.find_by_username(database, subject) 

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário do token não encontrado"
        )

    user.password_hash = None 
    return user