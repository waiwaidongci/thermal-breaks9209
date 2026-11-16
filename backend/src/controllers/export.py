from fastapi import HTTPException
from src.models import InspectionNote,SegmentationRun
from src.utils.csv_export import csv_response
from src.services.audit import record

def export_note(db,id,actor):
 note=db.get(InspectionNote,id)
 if not note:raise HTTPException(404,'说明不存在')
 if note.status!='approved':raise HTTPException(409,'仅已确认巡查说明可导出')
 run=db.get(SegmentationRun,note.run_id);rows=[[note.name,run.name,run.result['fingerprint'],s['position'],s['start']+1,s['end'],s['mean'],s['rss'],note.interpretation,note.next_step,note.review_note] for s in note.segment_snapshot]
 record(db,actor,'note.exported',{'note_id':id});return csv_response(f'thermal-inspection-{id}.csv',rows,['巡查说明','运行','输入指纹','段号','起始序号(含)','结束序号(含)','均温','RSS','人工解释','下一步','审核意见'])
