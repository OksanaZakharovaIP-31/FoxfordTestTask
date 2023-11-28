from typing import List, Union

from fastapi_filter import FilterDepends
from sqlalchemy import select, and_, or_
# import requests
# import uvicorn
from fastapi import FastAPI, Depends, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, RedirectResponse

from database import session, engine, get_db
from foxford_api.models import Tickets, Client, Message, Employee
from foxford_api.schemas import TicketsModel, ClientModel, MessageModel, EmployeeModel, TicketsFilter
from services.Tickets import TicketsService

# import sql_engine_service

app = FastAPI()


# sql_engine = sql_engine_service.get_engine()
#
# service = TicketsService(Session(engine))
# service = ProductService(Session(sql_engine))


@app.get("/tickets")
def get_all_tickets(tickets_filter: TicketsFilter = FilterDepends(TicketsFilter), db: session = Depends(get_db)):
    """
    Получение списка всех тикетов с использование фильтров и сортировки
    :param tickets_filter:
    :param db:
    :return:
    """
    query = tickets_filter.filter(select(Tickets))
    results = db.execute(query)
    return results.all()


@app.post("/tickets")
def new_ticket(name: str, client_id: int, status: str = "Open", employee_id: int = None, db: session = Depends(get_db)):
    """
    Добавление нового тикеты в бд
    :param name:
    :param client_id:
    :param status:
    :param employee_id:
    :param db:
    :return:
    """
    # Провека на сущестование клиента
    client = db.query(Client).filter_by(id=client_id).first()
    if client is None:
        return JSONResponse(status_code=404, content={"message": "Клиет не существует"})
    # Проверка на закрытые тикеты от клиента
    # Если тикетов от клиента еще не было
    tickets = db.query(Tickets).filter(Tickets.client_id == client_id).first()
    if tickets is None:
        ticket = Tickets(name=name, status=status, client_id=client_id, employee_id=employee_id)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return RedirectResponse('/tickets')
    # Если есть еще открытые тикеты, или в работе
    tickets = db.query(Tickets).filter(Tickets.client_id == client_id).\
        filter(or_(Tickets.status == 'Open',Tickets.status == 'OnWork')).first()
    if tickets is None:
        ticket = Tickets(name=name, status=status, client_id=client_id, employee_id=employee_id)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return RedirectResponse('/tickets')
    return JSONResponse(status_code=404, content={"message": "Предыдущий тикет не закрыт"})


@app.put('/tickets/employee')
def change_employee(id: int, employee_id: int, db: session = Depends(get_db)):
    """
    Измнение работника у тикета
    :param id:
    :param employee_id:
    :param db:
    :return:
    """
    ticket = db.query(Tickets).filter(Tickets.id == id).first()
    if ticket is None:
        return JSONResponse(status_code=404, content={"message": "Тикет не найден"})
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        return JSONResponse(status_code=404, content={"message": "Работник не найден"})
    ticket.employee_id = employee_id
    db.commit()
    db.refresh(ticket)
    return RedirectResponse('/tickets')


@app.put('/tickets/status')
def change_status(id: int, status: str, db: session = Depends(get_db)):
    """
    Изменение статуса у тикеты
    :param id:
    :param status:
    :param db:
    :return:
    """
    ticket = db.query(Tickets).filter(Tickets.id == id).first()
    if ticket is None:
        return JSONResponse(status_code=404, content={"message": "Тикет не найден"})
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    # return JSONResponse(status_code=200, content={"message": "Ститус изменен"})
    return RedirectResponse('/tickets')


@app.get('/messages/{tickets_id}')
def get_message(tickets_id: int, db: session = Depends(get_db)):
    """
    Получение сообщение, относящихся к тикету
    :param tickets_id:
    :param db:
    :return:
    """
    result = select(Message).filter_by(ticket_id=tickets_id)
    message = db.scalars(result).first()
    try:
        message.text
        results = db.query(Message).filter(Message.ticket_id == tickets_id).all()
        return results
    except:
        return JSONResponse(status_code=404, content={"message": "Сообщения для данного тикета не найдены"})


@app.post('/message')
def send_message(ticket: int, employee: int, text: str, db: session = Depends(get_db)):
    client = db.query(Tickets).filter_by(id=ticket).first()
    id_client = client.client_id
    print(id_client)
    message = Message(ticket_id=ticket, text=text, client_id=id_client, employee_id=employee)
    db.add(message)
    db.commit()
    db.refresh(message)
    return RedirectResponse('/message')

    # results = db.query(Tickets.id, Tickets.create_at, Tickets.update_at, Tickets.status, Tickets.name, Client.name, Employee.login).\
    #     join(Client, Tickets.client_id == Client.id) \
    #     .join(Employee, Tickets.employee_id == Employee.id, isouter=True).all()
    # print(results)
    # for t, c, e in results:
    #     try:
    #         e.name
    #         print(f'{t.id}, {t.create_at}, {t.update_at}, {t.name}, {t.status}, {c.name}, {e.name}')
    #     except:
    #         print(f'{t.id}, {t.create_at}, {t.update_at}, {t.name}, {t.status}, {c.name}')
    # return results

# if __name__ == '__main__':
#     uvicorn.run(app, host='localhost', port=8000)
