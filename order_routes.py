from fastapi import APIRouter 

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/") # @ = decorator
async def orders():
    """Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação do usuário."""
    return {"mensagem": "Você acessou a rota de pedidos!"}