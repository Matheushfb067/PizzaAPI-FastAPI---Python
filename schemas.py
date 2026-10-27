from pydantic import BaseModel
from typing import Optional
''' 
    Aqui iremos praticamente copiar as classes dentro de models, porem tipando os
    dados que foram definidos
'''

# Os dados foram padronizados no endpoint por meio de um unico objeto, pois agora ao em vez da função receber multiplos parametros, ela recebe apenas user_schema que é nosso objeto
class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    # Criando subclasse que indica que os dados acima devem ser intepretados como um dicionario python padrão
    class config: 
        from_attributes = True


'''
    id é criado automaticamente, então o usuario não precisa passa-lo 
    status não é necessario pedir para o usuario informa-lo, uma vez que quando o pedido é criado o status será por default PENDENTE
    preco, só será calculado, quando o usuario finalizar o pedido, portanto não podemos informa-lo.
'''

class OrderSchema(BaseModel):
    # A unica informação de fato que será necessaria é o campo user, que é o usuario dono do pedido
    # Esse campo é uma foreign key do campo de id na tabela User, então é necessario passarmos esse id

    user: int

    class config: 
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class config:
        from_attributes = True