import json
from datetime import datetime,timedelta,timezone
import numpy as np
from sqlalchemy import select,func
from src.config.database import Base,engine,SessionLocal
from src.models import User,ThermalBatch,TemperaturePoint,SegmentationRun,Segment,InspectionNote
from src.utils.security import hash_password
from src.utils.serialize import row
from src.services.analysis import analyze

def seed():
 Base.metadata.create_all(engine)
 with SessionLocal() as db:
  for role,name in [('admin','赵砚 · 工艺负责人'),('analyst','陈禾 · 热程分析员'),('viewer','吴川 · 巡查观察员')]:
   if not db.scalar(select(User).where(User.email==f'{role}@yangu.demo')):db.add(User(email=f'{role}@yangu.demo',name=name,role=role,password_hash=hash_password('Yangu2026!')))
  db.commit();rng=np.random.default_rng(224);n=300;t=np.arange(n)
  arrays=[np.r_[np.full(90,165.),np.full(110,181.),np.full(100,173.)]+rng.normal(0,1.2,n),165+t*.065+rng.normal(0,.8,n),172+rng.normal(0,1.8,n),np.full(n,170.)]
  names=['YG-2411-A 阶跃焙程','YG-2411-B 平滑升温','YG-2411-C 噪声对照','YG-2411-D 恒温对照']
  for index,(name,values) in enumerate(zip(names,arrays)):
   batch=db.scalar(select(ThermalBatch).where(ThermalBatch.name==name))
   if batch:continue
   batch=ThermalBatch(name=name,filename=f'yg-thermal-{index+1}-202611.csv',description=['均值阶跃，离线拟合后仍需巡查','平滑漂移可能被拟合为阶跃','纯噪声，不代表没有设备误差','零方差合法样本'][index]);db.add(batch);db.flush()
   start=datetime(2026,11,10+index,9,0,tzinfo=timezone.utc)
   for j,v in enumerate(values):db.add(TemperaturePoint(batch_id=batch.id,sequence=j+1,recorded_at=start+timedelta(seconds=30*j),temperature=float(v)))
   db.commit()
  run=db.scalar(select(SegmentationRun).where(SegmentationRun.name=='A批离线热程校对'))
  if not run:
   batch=db.scalar(select(ThermalBatch).where(ThermalBatch.name==names[0]));points=[row(x) for x in db.scalars(select(TemperaturePoint).where(TemperaturePoint.batch_id==batch.id).order_by(TemperaturePoint.sequence))];config={'min_size':12,'max_segments':8,'penalty':80.,'penalties':[0.,20.,80.,320.,1280.]};result=analyze(row(batch),points,config)
   run=SegmentationRun(batch_id=batch.id,name='A批离线热程校对',config=config,created_by='analyst@yangu.demo',status='succeeded',result=result);db.add(run);db.flush()
   for s in result['segments']:db.add(Segment(run_id=run.id,**{k:s[k] for k in ('position','start','end','mean','rss')}))
   db.commit()
  if not db.scalar(select(InspectionNote).where(InspectionNote.name=='A批巡查假设初稿')):
   segments=list(db.scalars(select(Segment).where(Segment.run_id==run.id).order_by(Segment.position)));db.add(InspectionNote(run_id=run.id,name='A批巡查假设初稿',segment_ids=[s.id for s in segments],segment_snapshot=[row(s) for s in segments],interpretation='分段均值变化提供离线巡查线索，不能据此认定工艺切换原因。',next_step='回查时间对应的炉温记录及校准记录，核对平滑变化或测量偏差。',created_by='analyst@yangu.demo'));db.commit()
  counts={m.__tablename__:db.scalar(select(func.count()).select_from(m)) for m in [User,ThermalBatch,TemperaturePoint,SegmentationRun,Segment,InspectionNote]};print(json.dumps(counts));return counts
if __name__=='__main__':seed()
