from sqlmodel import SQLModel, Field

class PlayerBase(SQLModel):
    name: str
    events: list

class PlayerDb(PlayerBase, table = True):
    id: int = Field(default=None, primary_key=True)
