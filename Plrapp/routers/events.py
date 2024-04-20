from fastapi import APIRouter, status, Depends
from ..database.models import AddEventModel, EventDb
from ..database import event_crud
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/events")

@router.get("/", response_model=list[EventDb], status_code=200)
def get_events(*, session: Session = Depends(get_session), typename:str = ""):
    events = event_crud.get_events(session,typename)
    return events
