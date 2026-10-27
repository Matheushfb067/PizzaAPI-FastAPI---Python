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