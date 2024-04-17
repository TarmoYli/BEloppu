from fastapi import HTTPException
from .models import PlayerBase, PlayerDb, EventBase, EventDb
from sqlmodel import Session, select

def get_events(session:Session, typename: str = ""):
    if typename != "":
        result = session.exec(select(EventDb).where(EventDb.type == typename)).all()
        if not result:
            raise HTTPException(status_code=400, detail=f"Event with type:{typename} does not exist")
        return result
    result = session.exec(select(EventDb)).all()
    return result