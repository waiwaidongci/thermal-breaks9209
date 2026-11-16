from sqlalchemy import select
from fastapi import HTTPException
from src.models import Segment,SegmentationRun
from src.utils.serialize import row

def selected_segments(db,run_id,ids):
 run=db.get(SegmentationRun,run_id)
 if not run or run.status!='succeeded':raise HTTPException(422,'只可为成功运行建立巡查说明')
 segments=list(db.scalars(select(Segment).where(Segment.run_id==run_id,Segment.id.in_(ids)).order_by(Segment.position)))
 if len(ids)!=len(set(ids)) or len(segments)!=len(ids):raise HTTPException(422,'所选分段不属于该运行或重复')
 return [row(s) for s in segments]
