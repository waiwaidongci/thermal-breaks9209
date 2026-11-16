from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.config.database import get_db
from src.controllers.dependencies import current_user,writers
from src.models import ThermalBatch,TemperaturePoint
from src.schemas.batch import BatchInput,PointPatch
from src.services.batches import create_batch,edit_point
from src.utils.serialize import row
router=APIRouter()
@router.get('/batches')
def batches(db:Session=Depends(get_db),user=Depends(current_user)):return [row(x) for x in db.scalars(select(ThermalBatch).order_by(ThermalBatch.id))]
@router.post('/batches')
def create(data:BatchInput,db:Session=Depends(get_db),user=Depends(writers)):return create_batch(db,data,user.email)
@router.get('/points')
def points(db:Session=Depends(get_db),user=Depends(current_user)):return [row(x) for x in db.scalars(select(TemperaturePoint).order_by(TemperaturePoint.batch_id,TemperaturePoint.sequence))]
@router.patch('/points/{id}')
def patch(id:int,data:PointPatch,db:Session=Depends(get_db),user=Depends(writers)):return edit_point(db,id,data,user.email)
