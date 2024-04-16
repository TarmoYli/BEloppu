from sqlmodel import SQLModel, Field, JSON, Column
from enum import Enum
from typing import List
from datetime import datetime as dt

class EventType(str, Enum):
    level_started = "level_started"
    level_solved = "level_solved"

class EventBase(SQLModel):
    type: EventType
    detail: str
    player_id: int
    timestamp: dt

class EventDb(EventBase, table= True):
    id: int = Field(default=None, primary_key=True)

class PlayerBase(SQLModel):
    name: str
    
class PlayerDb(PlayerBase, table = True):
    id: int = Field(default=None, primary_key=True)
    event: List[EventBase] = Field(sa_column = Column(JSON))