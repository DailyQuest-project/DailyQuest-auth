from sqlalchemy.orm import Session
from ..model.model import User 

class UserRepository: 
    @staticmethod
    def find_by_username(database: Session, username: str) -> User:
        '''Função para fazer uma query por username de um objeto User na DB'''
        return database.query(User).filter(User.username == username).first() 