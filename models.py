# Onde criaremos as classes do nosso banco de dados, que serão as tabelas do mesmo.

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
# from sqlalchemy_utils.types import ChoiceType

# create_engine: permite criar o banco
# declarative_base: permite criar a base do bando
# Column: Permite criar as colunas do banco de dados

# Criando conxão do banco:
db = create_engine("sqlite:///banco.db")

# Criando a base do banco:
Base = declarative_base()

# Criando as classes/tabelas do banco:

# Usuarios
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    ''' Sempre quando eu for criar um usuário por meio de códigos Python,
        a função __init__ será executada automaticamente para
        inicializar o objeto e definir os valores de seus atributos,
        como nome, e-mail, senha, status de atividade e permissão
        de administrador.
    '''
    def __init__(self, name, email, password, active, admin):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

# Pedidos
class Order(Base): 
    __tablename__ = "orders"

    # Passando uma lista de Tuplas com os diferentes status de pedidos que eu posso ter
    '''
    STATUS_ORDERS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )
    '''
    
    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    status = Column("status", String) # pendente, cancelado, finalizado
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float) 
    # items =
     
    ''' Sempre quando eu for criar um usuário por meio de códigos Python,
        a função __init__ será executada automaticamente para
        inicializar o objeto e definir os valores de seus atributos,
        como nome, e-mail, senha, status de atividade e permissão
        de administrador.
    '''
    def __init__(self, user, status="Pendente", price=0):
        self.user = user
        self.status = status
        self.price = price

# Itens dos pedidos
class Itens(Base): 
    __tablename__ = "order_itens"

    id = Column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unitary_price = Column("unitary_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    ''' Sempre quando eu for criar um usuário por meio de códigos Python,
        a função __init__ será executada automaticamente para
        inicializar o objeto e definir os valores de seus atributos,
        como nome, e-mail, senha, status de atividade e permissão
        de administrador.
    '''
    def __init__(self, amount, flavor, size, unitary_price, order):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.unitary_price = unitary_price
        self.order = order

# Executa a criação dos metadados do banco:
