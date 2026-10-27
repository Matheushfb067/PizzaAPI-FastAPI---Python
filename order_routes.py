from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlalchemy.orm import Session
from schemas import OrderSchema
from models import Order

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/") # @ = decorator
async def orders():
    """Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação do usuário."""
    return {"mensagem": "Você acessou a rota de pedidos!"}

@order_router.post("/order")
async def crate_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user = order_schema.user)
    session.add(new_order)
    session.commit()
    return {"Mensagem": f"Pedido criado com sucesso. ID do pedido: {new_order.id}"}