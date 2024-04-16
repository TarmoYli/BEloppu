from fastapi import HTTPException
from .models import PlayerBase, PlayerDb, EventBase, EventDb
from sqlmodel import Session, select

def get_player(session:Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    plr_data = {"id": plr.id, "name": plr.name}
    if plr.event is None:
        plr_data["event"] = []
    else:
        plr_data["event"] = plr.event
    return plr_data

def get_players(session:Session, plrname: str = ""):
    query = select(PlayerDb.id, PlayerDb.name)
    if plrname:
        query = query.where(PlayerDb.name == plrname)
    result = session.exec(query).all()
    players_data = [{"id": player.id, "name": player.name} for player in result]
    return players_data

def add_player(session:Session, plr_in: PlayerBase):
    plr = PlayerDb(name=plr_in.name)
    session.add(plr)
    session.commit()
    session.refresh(plr)
    return {"id": plr.id, "name": plr.name}

