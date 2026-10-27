from fastapi import APIRouter, Depends, HTTPException # Permite organizar as rotas da API em diferentes arquivos ou módulos
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session

# Sempre definir um prefixo para as rotas para organizar o código
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Função auxiliar de criação de token
def create_token(email):
    token = f"kjdashfkdjsakjash{email}"
    return token


@auth_router.get("/")
async def home():
    """Essa é a rota padrão de autenticação do nosso sistema"""
    return {"mensagem": "Você acessou a rota de autenticação!", "autenticado": False}

'''
    O modelo de criação de usuario a baixo tem alguns problemas: 
    - A sessão não é fechada em momento nenhum
    - Só uma mensagem é retornada dentro do if enquanto dentro do if deveria retornar um código de erro http e dentro do else um código de sucesso
    - Estamos pegando parametros de forma despadronizada
    - A senha não está sendo criptografada

    O objetivo de termos feito inicialmente dessa forma é demonstrar como é a estrutura 
    de criação de usuario de forma direta e simples.
'''
'''
@auth_router.post("/create_user")
async def create_account(email: str, password: str, name: str):
    # Pesquisando na tabela de usuario se existe um usuario com esse e-mail
    # Para isso trazemos a tabela de usuarios de models para cá por meio da importação 

    Session = sessionmaker(bind=db) # Criando nova sessão do banco
    session = Session() # Abrindo nova sessão no banco de dados

    # Agora eu podemos fazer requisições dentro da tabela user uma vez que a sessão já foi criada
    user = session.query(User).filter(User.email==email).first() # .first() pega o primeiero usuario com o email que queremos filtrar
    if user: 
        return {"mensagem":"Já existe um usuario com esse email!"}
    else:
        # Caso o usuario não exista devemos criar um novo usuario
        # Para isso precisamos passar o nome, email e senha que foram definidos em models
        # Depois armazemos no banco por meio da sessão

        new_user = User(name, email, password, True, False)
        session.add(new_user) # Armazenando novo usuario criado no banco
        session.commit() # Salva as alterações no banco
        return {"mensagem": "Usuario cadastrado com sucesso!"}
'''

# Fazendo o gerenciamento de sessão de forma mais robusta
# Todas as rotas dependem de uma sessão, portanto, para não criarmos elas em todos os endpoints criamos uma dependencia
# criado no arquivo dependencies.py que conterá a minha sessão e o fechamento dessa sessão

@auth_router.post("/create_user")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    # Pesquisando na tabela de usuario se existe um usuario com esse e-mail
    # Para isso trazemos a tabela de usuarios de models para cá por meio da importação 
    
    #    Agora ao em vez de criarmos a sessão aqui diretamente, passamos ela como parametro 
    #    direto para a função crate_acount sem precisar importar db e nem sqlalchemy.orm sessionmaker
    #    uma vez que isso está importado no arquivo de dependencies, então só importamos o proprio 
    #    dependencies.
    
    # Agora eu podemos fazer requisições dentro da tabela user uma vez que a sessão já foi criada
    user = session.query(User).filter(User.email==user_schema.email).first() # .first() pega o primeiero usuario com o email que queremos filtrar
    if user:    
        # Fazendo a padronizão de código de respostas
        # Usando HTTPExeption para gerar códigos de erro http para requisições incorretas. Nesse caso o código 400
        # return HTTPException(status_code = 400, detail="E-mail já cadastrado!")
        # é costume usar o raise ao em vez de return, já que estamos levantando um erro e não retornando um dado
        raise HTTPException(status_code = 400, detail="E-mail já cadastrado!")
    else:

        # Cria uma hash a partir da senha que o usuario digitou
        encrypted_password = bcrypt_context.hash(user_schema.password)

        # Caso o usuario não exista devemos criar um novo usuario
        # Para isso precisamos passar o nome, email e senha que foram definidos em models
        # Depois armazemos no banco por meio da sessão

        new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.active, user_schema.admin)
        session.add(new_user) # Armazenando novo usuario criado no banco
        session.commit() # Salva as alterações no banco

        return {"mensagem": f"Usuario cadastrado com sucesso! {user_schema.email}"}

# Proxima rota: login, faz sentido criarmos uma rota de login, uma vez que queremos apenas que usuarios logados possam fazer pedidos
# O processo de loging que se usa no fastAPI é o processo de uso de Tokens você loga apenas uma unica vez e esse token é usado em todas as rotas que estamos logados

# JWT

# login -> email e senha -> token JWT (Jsom Web token)

@auth_router.post("/login")
async def login(login_schema: LoginSchema , session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==login_schema.email).first()
    if not user: 
        raise HTTPException(status_code=400, detail = "Usuario não encontrado!")
    else:
        access_token = create_token(user.id)
        return {
            "access_token":access_token, 
            "token_type": "Bearer" # Padrão do token
            }
    