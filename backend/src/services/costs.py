import numpy as np
class StableCosts:
 def __init__(self,values):
  self.y=np.asarray(values,dtype=np.longdouble)
  if self.y.ndim!=1 or not 1<=len(self.y)<=600 or not np.isfinite(self.y).all() or (np.abs(self.y)>1e12).any():raise ValueError('序列须有限，一维，1..600点，温度绝对值≤1e12')
  self.origin=self.y[0];spread=np.max(np.abs(self.y-self.origin));self.scale=spread if spread else np.longdouble(1)
  z=(self.y-self.origin)/self.scale
  self.s=np.r_[np.longdouble(0),np.cumsum(z,dtype=np.longdouble)]
  self.q=np.r_[np.longdouble(0),np.cumsum(z*z,dtype=np.longdouble)]
 def normalized(self,starts,end):
  starts=np.asarray(starts,dtype=int);length=end-starts;v=(self.q[end]-self.q[starts])-(self.s[end]-self.s[starts])**2/length
  return np.maximum(v,np.longdouble(0))
 def segment(self,start,end):
  mean=self.origin+self.scale*(self.s[end]-self.s[start])/(end-start)
  return {'start':int(start),'end':int(end),'count':int(end-start),'mean':float(mean),'rss':float(self.normalized([start],end)[0]*self.scale*self.scale)}
