"""
Validation data
"""
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


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

    class Config:
        orm_mode = True


class Employee(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int

    class Config:
        orm_mode = True


class TicketsModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    name: str
    status: StatusType = StatusType.Open
    create_at: datetime
    update_at: datetime
    client_id: int
    employee_id: Optional [int]

    class Config:
        orm_mode = True


class MessageModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int

    class Config:
        orm_mode = True
