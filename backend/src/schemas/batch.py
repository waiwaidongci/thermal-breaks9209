from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
class PointInput(BaseModel):
 model_config=ConfigDict(allow_inf_nan=False)
 sequence:int=Field(ge=1,le=600,strict=True)
 recorded_at:datetime
 temperature:float=Field(ge=-1e12,le=1e12)
class BatchInput(BaseModel):
 name:str=Field(min_length=2,max_length=150)
 filename:str=Field(min_length=2,max_length=180)
 description:str=Field(default='',max_length=3000)
 points:list[PointInput]=Field(min_length=1,max_length=600)
class PointPatch(BaseModel):
 model_config=ConfigDict(allow_inf_nan=False)
 temperature:float=Field(ge=-1e12,le=1e12)
