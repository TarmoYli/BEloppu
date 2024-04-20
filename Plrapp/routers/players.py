from fastapi import APIRouter, Depends
from ..database.models import  GetPlrWithId, EventDb, AddEventModel, CreatePlr, GetPlrs
from ..database import plr_crud
from ..database.database import get_session
from sqlmodel import Session
from typing import List, Optional

router = APIRouter(prefix="/players")

@router.get("/", response_model=List[GetPlrs], status_code=200)
def get_players(*, session: Session = Depends(get_session)):
    plrs = plr_crud.get_players(session)
    return plrs

@router.post("/", status_code=201)
def add_player(*, session: Session = Depends(get_session), plr_in: CreatePlr):
    plr = plr_crud.add_player(session, plr_in)
    return plr

@router.get("/{id}", response_model=GetPlrWithId, status_code=200)
def get_player(*, session: Session = Depends(get_session), id:int):
    return plr_crud.get_player(session, id)

@router.post("/{id}/events", status_code=201)
def make_event(id:int, event_in: AddEventModel, session: Session = Depends(get_session)):
    return plr_crud.make_new_event(session, event_in, id)

@router.get("/{id}/events",response_model=List[EventDb], status_code=200)
def get_plr_event(id: int, type: Optional[str] = "", session: Session=Depends(get_session)):
    return plr_crud.get_plr_event(session, id, type)
