# Em: src/login/repository.py

from sqlalchemy.orm import Session
from ..model.model import User # <-- Mudança aqui

class UserRepository: # <-- Mudança aqui
    @staticmethod
    def find_by_username(database: Session, username: str) -> User: # <-- Mudança aqui
        '''Função para fazer uma query por username de um objeto User na DB'''
        return database.query(User).filter(User.username == username).first() # <-- Mudança aqui