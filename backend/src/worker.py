import json
from pathlib import Path
from celery import Celery
from src.config.database import SessionLocal
from src.config.settings import REDIS_URL,ARTIFACT_DIR
from src.models import SegmentationRun,Segment
from src.services.analysis import analyze
from src.services.batches import batch_data
from src.services.audit import record
app=Celery('thermal_breaks',broker=REDIS_URL,backend=REDIS_URL)
app.conf.update(task_track_started=True,worker_prefetch_multiplier=1,task_acks_late=True)
@app.task(name='thermal.analyze',soft_time_limit=120,time_limit=150)
def analyze_run(id):
 with SessionLocal() as db:
  run=db.get(SegmentationRun,id)
  if not run or run.status=='succeeded':return
  run.status='running';db.commit()
  try:
   batch,points=batch_data(db,run.batch_id);result=analyze(batch,points,run.config)
   Path(ARTIFACT_DIR).mkdir(parents=True,exist_ok=True);Path(ARTIFACT_DIR,f'thermal-{id}.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False))
   for segment in result['segments']:db.add(Segment(run_id=id,**{k:segment[k] for k in ('position','start','end','mean','rss')}))
   run.result=result;run.status='succeeded';run.error=None;db.commit();record(db,'worker','run.succeeded',{'run_id':id,'segments_count':result['segments_count']})
  except Exception as e:
   db.rollback();run=db.get(SegmentationRun,id);run.status='failed';run.error=str(e)[:1000];db.commit();record(db,'worker','run.failed',{'run_id':id,'error':run.error})
