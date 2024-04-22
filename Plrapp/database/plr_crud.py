from fastapi import HTTPException
from .models import PlayerDb, CreateEventModel, EventDb, EventType, CreatePlr
from sqlmodel import Session, select
from datetime import datetime

def get_player(session:Session, id:int):
    plr = session.get(PlayerDb, id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{id} not found")
    events = get_plr_event(session,id,"")
#    ordered = ordering_event(events)
    return {"id": plr.id, "name": plr.name, "events": events}

def get_players(session:Session):
    result = session.exec(select(PlayerDb)).all()
    plrs = [{"id": player.id, "name": player.name} for player in result]
    return plrs

def add_player(session: Session, plr_in: CreatePlr):
    plr = PlayerDb(name=plr_in.name)
    session.add(plr)
    session.commit()
    session.refresh(plr)
    return {"id": plr.id, "name": plr.name}

def make_new_event(session: Session, event_in: CreateEventModel, plr_id: int):
    plr = session.get(PlayerDb, plr_id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{plr_id} not found")
    if event_in.type not in[EventType.level_started, EventType.level_solved]:
        raise HTTPException(status_code=400, detail=f"Event type {event_in.type} does not exist")
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = EventDb(type = event_in.type, detail = event_in.detail, player_id = plr_id, timestamp = dt)
    event.player_id = plr.id
    session.add(event)
    session.commit()
    session.refresh(event)
    ordering_response = event.model_dump()
    ordered_response = {
            "id": ordering_response["id"],
            "type": ordering_response["type"],
            "detail": ordering_response["detail"],
            "timestamp": ordering_response["timestamp"],
            "player_id": ordering_response["player_id"],
        }
    return ordered_response

def get_plr_event(session: Session, plr_id: int, event_type: str = ""):
    plr = session.get(PlayerDb, plr_id)
    if not plr:
        raise HTTPException(status_code=404, detail=f"Player with id:{plr_id} not found")
    if event_type != "":
        if event_type != EventType.level_started and event_type != EventType.level_solved:
            raise HTTPException(status_code=400, detail=f"Event with type:{event_type} does not exist")
        events = session.exec(select(EventDb).where((EventDb.player_id == plr.id) & (EventDb.type == event_type))).all()
        events_ordered = ordering_event(events)
        return events_ordered    
    events = session.exec(select(EventDb).where(EventDb.player_id == plr.id)).all()
    events_ordered = ordering_event(events)
    return events_ordered

def ordering_event(events: EventDb):
    ordered_4lyfe = []
    for event in events:
        event_model = event.model_dump()
        ordered_event = {
            "id": event_model["id"],
            "type": event_model["type"],
            "detail": event_model["detail"],
            "timestamp": event_model["timestamp"],
            "player_id": event_model["player_id"],
        }
        ordered_4lyfe.append(ordered_event)
    return ordered_4lyfe
