from fastapi import HTTPException
from .models import EventDb
from ..database.plr_crud import ordering_event
from sqlmodel import Session, select

def get_events(session:Session, typename: str = ""):
    if typename != "":
        result = session.exec(select(EventDb).where(EventDb.type == typename)).all()
        if not result:
            raise HTTPException(status_code=400, detail=f"Event with type:{typename} does not exist")
        return result
    result = session.exec(select(EventDb)).all()
    final= ordering_event(result)
    return final