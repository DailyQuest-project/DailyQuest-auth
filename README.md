# DailyQuest Auth

Serviço de autenticação FastAPI com JWT.

## Tecnologias

- FastAPI, JWT (PyJWT)
- PostgreSQL, SQLAlchemy
- Bcrypt para hashing

## Usuários de Teste

| Usuário | Email | Senha |
|---------|-------|-------|
| `testuser` | test@example.com | `testpass123` |
| `demo` | demo@dailyquest.com | `demo123` |

## Quick Start

```bash
docker compose up --build

# Auth disponível em: http://localhost:8001
# Docs: http://localhost:8001/docs
```

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/login` | Autenticação, retorna JWT |
| POST | `/register` | Criar nova conta |
| GET | `/me` | Dados do usuário autenticado |

## Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:pass@db:5432/dailyquest_db
JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Estrutura

```
src/
├── main.py        # App FastAPI
├── config.py      # Configurações
├── database.py    # Conexão DB
├── security.py    # JWT e hashing
├── login/         # Rotas de auth
└── model/         # Modelos SQLAlchemy
```
