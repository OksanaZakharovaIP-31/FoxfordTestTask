"""
Validation data
"""
from pydantic import BaseModel, ConfigDict


class ClientModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int


class Employee(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int


class TicketsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int


class MessageModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
