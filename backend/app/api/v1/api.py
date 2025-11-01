from fastapi import APIRouter

from app.api.v1.endpoints import categorias, rifas, tickets, users, webhooks

api_router = APIRouter()
api_router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
api_router.include_router(rifas.router, prefix="/rifas", tags=["rifas"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])