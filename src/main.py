import requests
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import session
from foxford_api.models import Tickets
from foxford_api.schemas import TicketsModel

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[TicketsModel])
def get_quiz(db: Session = Depends(get_db)):
    """
    Get function
    Returns all objects from database (all quiz question)
    """
    results = db.query(Tickets).all()
    return results


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)