from sqlmodel import SQLModel, Field
from enum import Enum
import datetime

class PlayerBase(SQLModel):
    name: str
    events: list

class PlayerDb(PlayerBase, table = True):
    id: int = Field(default=None, primary_key=True)

class EventType(str, Enum):
    level_started = "level_started"
    level_solved = "level_solved"

class EventBase(SQLModel):
    type: EventType
    detail: str
    player_id: int
    timestamp: datetime

class EventDb(EventBase):
    id: int = Field(default=None, primary_key=True)