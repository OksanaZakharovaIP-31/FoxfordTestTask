from typing import List

import requests
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import session
from foxford_api.models import Tickets, Client
from foxford_api.schemas import TicketsModel, ClientModel

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[TicketsModel])
def get_tickets(db: session = Depends(get_db)):
    results = db.query(Tickets).all()
    return results


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
