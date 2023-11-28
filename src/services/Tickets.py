from database import session, get_db
from fastapi import Depends
from foxford_api.models import Tickets
from foxford_api.schemas import TicketsModel, TicketsFilter
from sqlalchemy import select


class TicketsService:
    def __init__(self, db: session = Depends(get_db)):
        self.session = session

    def get_tickets_filter(self, ticket_filter: TicketsFilter):
        query_filter = ticket_filter.filter(select(Tickets))

        return self.session.exec(query_filter).all()