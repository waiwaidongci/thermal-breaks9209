from sqlalchemy import select
from fastapi import HTTPException
from src.models import SegmentationRun
from src.utils.serialize import row
from .batches import batch_data
from .validation import validate_config
from .audit import record

def create_run(db,data,actor):
 _,points=batch_data(db,data.batch_id);config=data.model_dump(exclude={'batch_id','name'})
 try:validate_config(config,len(points))
 except ValueError as e:raise HTTPException(422,str(e))
 if db.scalar(select(SegmentationRun).where(SegmentationRun.name==data.name)):raise HTTPException(409,'运行名称已存在')
 run=SegmentationRun(batch_id=data.batch_id,name=data.name,config=config,created_by=actor,status='queued');db.add(run);db.commit()
 try:
  from src.worker import analyze_run
  analyze_run.delay(run.id)
 except Exception:
  run.status='failed';run.error='队列不可用，请稍后重试';db.commit();raise HTTPException(503,run.error)
 record(db,actor,'run.queued',{'run_id':run.id});return row(run)
