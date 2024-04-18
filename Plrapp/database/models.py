from sqlmodel import SQLModel, Field, JSON, Column, ForeignKey, Integer
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    level_started = "level_started"
    level_solved = "level_solved"

class PlayerBase(SQLModel):
    name: str
    
class PlayerDb(PlayerBase, table = True):
    id: int = Field(default=None, primary_key=True)

class EventBase(SQLModel):
    type: EventType
    detail: str

class EventDb(EventBase, table= True):
    id: int = Field(default=None, primary_key=True)
    player_id: int = Field(sa_column = Column(Integer, ForeignKey("playerdb.id")))
    timestamp: str