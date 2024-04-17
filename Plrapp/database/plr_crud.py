from fastapi import HTTPException
from .models import PlayerBase, PlayerDb, EventBase, EventDb
from sqlmodel import Session, select

def get_player(session:Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    plr_data = {"id": plr.id, "name": plr.name, "event" : plr.event or []}
    return plr_data

def get_players(session:Session, plrname: str = ""):
    if plrname != "":
        result = session.exec(select(PlayerDb).where(PlayerDb.name == plrname)).all()
        if not result:
            raise HTTPException(status_code=404, detail=f"Player with name:{plrname} not found")
        plr = [{"id": player.id, "name": player.name, "event": player.event or []} for player in result]
        return plr 
    result = session.exec(select(PlayerDb)).all()
    plrs = [{"id": player.id, "name": player.name, "event" : player.event or []} for player in result]
    return plrs

def add_player(session:Session, plr_in: PlayerBase):
    plr = PlayerDb(name=plr_in.name)
    session.add(plr)
    session.commit()
    session.refresh(plr)
    return {"id": plr.id, "name": plr.name}

