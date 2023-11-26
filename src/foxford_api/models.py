"""
Модели БД
"""
from enum import Enum

from sqlalchemy.orm import relationship

from database import engine, Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String


class StatusType(str, Enum):
    """
    Возможные варианты статуса тикета
    """
    Open = 'Открыт'
    OnWork = 'В работе'
    Closed = 'Закрыт'


class Client(Base):
    """
    Таблица с клиентами
    """
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    ticket = relationship("Tickets", back_populates='client')
    message = relationship('Message', back_populates='client')


class Employee(Base):
    """
    Таблица с работниками
    """
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    ticket = relationship("Tickets", back_populates='employee')
    message = relationship('Message', back_populates='employee')


class Tickets(Base):
    """
    Таблица с тикетами
    """
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    status = StatusType.Open
    create_at = Column(DateTime)
    update_at = Column(DateTime)

    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    client = relationship('Client', back_populates='ticket')

    employee_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'), nullable=True)
    employee = relationship('Employee', back_populates='ticket')

    message = relationship('Message', back_populates='ticket')


class Message(Base):
    """
    Таблица с сообщениями
    """
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    ticket_id = Column(Integer, ForeignKey('ticker.id', ondelete='CASCADE'), nullable=False)
    ticket = relationship('Ticket', back_populates='message')

    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    client = relationship('Client', back_populates='message')

    employee_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'), nullable=True)
    employee = relationship('Employee', back_populates='message')


Base.metadata.create_all(bind=engine)
