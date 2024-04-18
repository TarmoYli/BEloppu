from fastapi import HTTPException
from .models import PlayerBase, PlayerDb, EventBase, EventDb
from sqlmodel import Session, select
from datetime import datetime
import json

def get_player(session:Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    return plr

def get_players(session:Session, plrname: str = ""):
    if plrname != "":
        result = session.exec(select(PlayerDb).where(PlayerDb.name == plrname)).all()
        if not result:
            raise HTTPException(status_code=404, detail=f"Player with name:{plrname} not found")

        plr = [{"id": player.id, "name": player.name, "events": session.exec(select(EventDb).where(EventDb.player_id == player.id)).all()} for player in result]
        return plr 
    result = session.exec(select(PlayerDb)).all()
    plrs = [{"id": player.id, "name": player.name, "events" : session.exec(select(EventDb).where(EventDb.player_id == player.id)).all()} for player in result]
    return plrs

def add_player(session:Session, plr_in: PlayerBase):
    plr = PlayerDb(name=plr_in.name)
    session.add(plr)
    session.commit()
    session.refresh(plr)
    return {"id": plr.id, "name": plr.name}

def make_new_event(session:Session, event_in: EventBase, plr_id:int):
    plr = session.get(PlayerDb, plr_id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{plr_id} not found")
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = EventDb(type=event_in.type, detail=event_in.detail, player_id=plr_id,timestamp=dt)
    event.player_id = plr.id
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

