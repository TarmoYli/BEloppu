from fastapi import HTTPException
from .models import PlayerBase, PlayerDb, EventBase, EventDb
from sqlmodel import Session, select

def get_player(session:Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    return plr

def get_players(session:Session, plrname: str = ""):
    if plrname != "":
        return session.exec(select(PlayerDb).where(PlayerDb.name == plrname)).all()
    return session.exec(select(PlayerDb)).all()

def add_player(session:Session, plr_in: PlayerBase):
    plr = PlayerDb.model_validate(plr_in)
    session.add(plr)
    session.commit()
    session.refresh(plr)
    return plr

def delete_plr(session: Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    session.delete(plr)
    session.commit()
    return {"Message": f"Player with id:{id} deleted."}
