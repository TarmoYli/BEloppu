from sqlmodel import SQLModel, Field, Column, ForeignKey, Integer
from enum import Enum
from typing import Any


class EventType(str, Enum):
    level_started = "level_started"
    level_solved = "level_solved"

class AddEventModel(SQLModel):
    type: EventType
    detail: str

class CreatePlr(SQLModel):
    name: str
        
class PlayerDb(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str

class EventDb(SQLModel, table= True):
    id: int = Field(default=None, primary_key=True)
    type: EventType
    detail: str
    timestamp: str
    player_id: int = Field(sa_column = Column(Integer, ForeignKey("playerdb.id")))

class GetPlrs(SQLModel):
    id:int
    name: str

class GetPlrWithId(SQLModel):
    id: int
    name: str
    events: Any

# "id": 1,
# "type": "level_started",
# "detail": "level_1212_001",
# "timestamp": "2023-01-13 12:01:22",
# "player_id": 1
