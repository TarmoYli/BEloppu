from fastapi import APIRouter, status, Depends
from ..database.models import PlayerBase, PlayerDb, EventDb, EventBase
from ..database import plr_crud
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/players")

@router.get("/", response_model=list[PlayerDb], status_code=200)
def get_players(*, session: Session = Depends(get_session), plr:str = ""):
    plrs = plr_crud.get_players(session,plr)
    return plrs

@router.post("/", status_code=201)
def add_player(*, session: Session = Depends(get_session), plr_in: PlayerBase):
    plr = plr_crud.add_player(session, plr_in)
    return plr

@router.get("/{id}", response_model=PlayerDb, status_code=200)
def get_player(*, session: Session = Depends(get_session), id:int):
    return plr_crud.get_player(session, id)

@router.post("/{id}/events", status_code=201)
def make_event(*, session: Session = Depends(get_session),id:int,eventtype:str,details:str):
    return plr_crud.make_new_event(session,eventtype,details,id)

#@router.get("/{id}/events", status_code=200, response_model=list)
#def get_player_events(*, session: Session = Depends(get_session), type: str = ""):
#    pass
