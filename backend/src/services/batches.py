from sqlalchemy import select
from fastapi import HTTPException
from src.models import ThermalBatch,TemperaturePoint
from src.utils.serialize import row
from .validation import validate_points
from .audit import record

def create_batch(db,data,actor):
 try:points=validate_points([x.model_dump() for x in data.points])
 except ValueError as e:raise HTTPException(422,str(e))
 if db.scalar(select(ThermalBatch).where(ThermalBatch.name==data.name)):raise HTTPException(409,'批次名称已存在')
 batch=ThermalBatch(name=data.name,filename=data.filename,description=data.description);db.add(batch);db.flush()
 for point in points:db.add(TemperaturePoint(batch_id=batch.id,**point))
 db.commit();record(db,actor,'batch.created',{'batch_id':batch.id,'points':len(points)});return row(batch)

def batch_data(db,id):
 batch=db.get(ThermalBatch,id)
 if not batch:raise HTTPException(404,'批次不存在')
 points=list(db.scalars(select(TemperaturePoint).where(TemperaturePoint.batch_id==id).order_by(TemperaturePoint.sequence)))
 return row(batch),[row(x) for x in points]

def edit_point(db,id,data,actor):
 point=db.get(TemperaturePoint,id)
 if not point:raise HTTPException(404,'温度点不存在')
 point.temperature=data.temperature;db.commit();record(db,actor,'point.updated',{'point_id':id});return row(point)
