import math
from datetime import datetime,timezone

def validate_points(points):
 if not 1<=len(points)<=600:raise ValueError('每批必须1..600点')
 ordered=sorted(points,key=lambda p:p['sequence'])
 if [p['sequence'] for p in ordered]!=list(range(1,len(ordered)+1)):raise ValueError('序号须从1连续且唯一')
 times=[]
 for p in ordered:
  if not math.isfinite(p['temperature']) or abs(p['temperature'])>1e12:raise ValueError('温度必须有限且绝对值不超1e12')
  t=p['recorded_at'];t=datetime.fromisoformat(t.replace('Z','+00:00')) if isinstance(t,str) else t
  if t.tzinfo is None or t.utcoffset() is None:raise ValueError('时间必须包含时区')
  times.append(t.astimezone(timezone.utc))
 if any(b<=a for a,b in zip(times,times[1:])):raise ValueError('时间必须按序号严格递增，不能重复或倒序')
 return ordered

def validate_config(config,n):
 m=config['min_size'];k=config['max_segments'];b=config['penalty'];path=config['penalties']
 if not isinstance(m,int) or isinstance(m,bool) or not 1<=m<=600 or m>n:raise ValueError('min_size超出样本数或合法范围')
 if not isinstance(k,int) or isinstance(k,bool) or not 1<=k<=12:raise ValueError('max_segments必须1..12')
 if not math.isfinite(b) or not 0<=b<=1e12 or not 2<=len(path)<=12 or any(not math.isfinite(x) or not 0<=x<=1e12 for x in path):raise ValueError('罚项需有限非负且路径2..12项')
 if len(set(path))<2:raise ValueError('罚项路径至少两个不同值')
 return min(k,n//m)
