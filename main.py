from fastapi import FastAPI
from passlib.context import CryptContext # Ferramenta para criar a criptografica das nossas senhas
from dotenv import load_dotenv # 

app = FastAPI()

# Tem que ser criado depois de app = FastAPI() para não dar erro de importação circular
from auth_routes import auth_router
from order_routes import order_router

# incluir no site todas as rotas do auth_router e order_router por meio do arquivo main.py
app.include_router(auth_router)
app.include_router(order_router)


