from pydantic import BaseModel,Field
class SegmentSelection(BaseModel):
 segment_ids:list[int]=Field(min_length=1,max_length=12)
