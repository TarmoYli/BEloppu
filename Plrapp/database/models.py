from sqlmodel import SQLModel, Field, Column, ForeignKey, Integer
from enum import Enum

class EventType(str, Enum):
    level_started = "level_started"
    level_solved = "level_solved"

class EventBase(SQLModel):
    type: str
    detail: str

class PlayerBase(SQLModel):
    name:str

class GetPlrs(PlayerBase):
    id:int

class CreatePlr(PlayerBase):
    pass

class CreateEventModel(EventBase):
    pass
    
class PlayerDb(PlayerBase, table = True):
    id: int = Field(default=None, primary_key=True)

class EventDb(EventBase, table= True):
    id: int = Field(default=None, primary_key=True)
    type: EventType
    timestamp: str
    player_id: int = Field(sa_column = Column(Integer, ForeignKey("playerdb.id")))

class GetPlrWithId(PlayerBase):
    id: int
    events: list[EventDb]