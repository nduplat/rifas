from sqlalchemy.orm import Session
from sqlalchemy import and_
import random
from typing import List, Dict, Any
from fastapi import HTTPException

from app.models.rifa import Rifa
from app.models.ticket import Ticket
from app.models.ganador import Ganador


class RifaService:
    def __init__(self, db: Session):
        self.db = db

    def close_rifa(self, rifa_id: str) -> Dict[str, Any]:
        rifa = self.db.query(Rifa).filter(Rifa.id == rifa_id).first()
        if rifa is None:
            raise HTTPException(status_code=404, detail="Rifa not found")

        if rifa.estado == "cerrada":
            raise HTTPException(status_code=400, detail="Rifa already closed")

        # Select winners
        sold_tickets = self.db.query(Ticket).filter(
            and_(Ticket.rifa_id == rifa_id, Ticket.estado == "vendido")
        ).all()

        if len(sold_tickets) < rifa.numero_ganadores:
            raise HTTPException(status_code=400, detail="Not enough tickets sold")

        winners = random.sample(sold_tickets, rifa.numero_ganadores)

        for i, ticket in enumerate(winners):
            ticket.estado = "ganador"
            ganador = Ganador(
                rifa_id=rifa_id,
                ticket_id=ticket.id,
                usuario_id=ticket.usuario_id,
                posicion=i + 1
            )
            self.db.add(ganador)

        rifa.estado = "cerrada"
        self.db.commit()
        return {"message": "Rifa closed successfully", "winners": [str(w.id) for w in winners]}

    def recalculate_rifa(self, rifa_id: str) -> Dict[str, Any]:
        rifa = self.db.query(Rifa).filter(Rifa.id == rifa_id).first()
        if rifa is None:
            raise HTTPException(status_code=404, detail="Rifa not found")

        if rifa.estado != "cerrada":
            raise HTTPException(status_code=400, detail="Rifa must be closed to recalculate")

        # Remove existing winners
        self.db.query(Ganador).filter(Ganador.rifa_id == rifa_id).delete()

        # Reset ticket states
        self.db.query(Ticket).filter(
            and_(Ticket.rifa_id == rifa_id, Ticket.estado == "ganador")
        ).update({"estado": "vendido"})

        # Re-select winners
        sold_tickets = self.db.query(Ticket).filter(
            and_(Ticket.rifa_id == rifa_id, Ticket.estado == "vendido")
        ).all()

        winners = random.sample(sold_tickets, min(rifa.numero_ganadores, len(sold_tickets)))

        for i, ticket in enumerate(winners):
            ticket.estado = "ganador"
            ganador = Ganador(
                rifa_id=rifa_id,
                ticket_id=ticket.id,
                usuario_id=ticket.usuario_id,
                posicion=i + 1
            )
            self.db.add(ganador)

        self.db.commit()
        return {"message": "Rifa recalculated successfully", "winners": [str(w.id) for w in winners]}