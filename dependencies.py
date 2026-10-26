from models import db 
from sqlalchemy.orm import sessionmaker

def get_session():
    try: 
        Session = sessionmaker(bind=db) # Criando nova sessão do banco
        session = Session() # Abrindo nova sessão no banco de dados
        yield session
    finally:
        session.close()