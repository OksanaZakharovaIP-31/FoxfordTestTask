"""
Validation data
"""
from enum import Enum

from pydantic import BaseModel, ConfigDict

class StatusType(str, Enum):
    """
    Возможные варианты статуса тикета
    """
    Open = 'Открыт'
    OnWork = 'В работе'
    Closed = 'Закрыт'


class ClientModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int


class Employee(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int


class TicketsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    status: StatusType = StatusType.Open


class MessageModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
