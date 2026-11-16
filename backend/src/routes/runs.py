from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controllers.dependencies import current_user,writers
from src.models import SegmentationRun,Segment
from src.schemas.run import RunInput
from src.services.runs import create_run
from src.utils.serialize import row
router=APIRouter()
@router.get('/runs')
def runs(db:Session=Depends(get_db),user=Depends(current_user)):return [row(x) for x in db.scalars(select(SegmentationRun).order_by(SegmentationRun.id.desc()))]
@router.get('/runs/{id}')
def one(id:int,db:Session=Depends(get_db),user=Depends(current_user)):
 run=db.get(SegmentationRun,id)
 if not run:raise HTTPException(404,'运行不存在')
 return row(run)
@router.post('/runs')
def create(data:RunInput,db:Session=Depends(get_db),user=Depends(writers)):return create_run(db,data,user.email)
@router.get('/segments')
def segments(db:Session=Depends(get_db),user=Depends(current_user)):return [row(x) for x in db.scalars(select(Segment).order_by(Segment.run_id,Segment.position))]
