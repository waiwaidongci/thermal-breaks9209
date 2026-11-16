from sqlalchemy import select
from fastapi import HTTPException
from src.models import InspectionNote
from src.utils.serialize import row
from .segments import selected_segments
from .audit import record

def create_note(db,data,actor):
 if db.scalar(select(InspectionNote).where(InspectionNote.name==data.name)):raise HTTPException(409,'说明名称已存在')
 snapshot=selected_segments(db,data.run_id,data.segment_ids)
 note=InspectionNote(**data.model_dump(),segment_snapshot=snapshot,created_by=actor);db.add(note);db.commit();record(db,actor,'note.created',{'note_id':note.id});return row(note)

def approve_note(db,id,data,actor):
 note=db.get(InspectionNote,id)
 if not note:raise HTTPException(404,'巡查说明不存在')
 note.status=data.status;note.review_note=data.review_note;db.commit();record(db,actor,'note.reviewed',{'note_id':id,'status':note.status});return row(note)
