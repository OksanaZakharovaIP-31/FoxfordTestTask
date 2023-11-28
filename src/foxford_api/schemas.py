"""
Validation data
"""
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from foxford_api.models import Client, Employee, Tickets


class StatusType(str, Enum):
    """
    Возможные варианты статуса тикета
    """
    Open = 'Open'
    OnWork = 'OnWork'
    Close = 'Close'


class ClientModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    name: str

    # class Config:
    #     orm_mode = True


class EmployeeModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    name: str
    email: str
    login: str
    password: str
    #
    # class Config:
    #     orm_mode = True


class TicketsModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    name: str
    status: StatusType
    create_at: datetime
    update_at: datetime
    client_id: int
    employee_id: Optional[int] = None
    #

    class Config:
        from_attributes = True


class MessageModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    ticket_id: int
    client_id: int
    employee_id: int
    text: str
    ticket_id: int

    class Config:
        from_attributes = True


class TicketsFilter(Filter):
    """
    Фильтрация
    """
    status__in: Optional[list[StatusType]] = None
    employee_id__isnull: Optional[list[int]] = None
    # order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Tickets

    class Config:
        populate_by_field_name = True

