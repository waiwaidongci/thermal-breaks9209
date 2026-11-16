import numpy as np

def build_frontier(costs,min_size,max_segments):
 n=len(costs.y);feasible=min(max_segments,n//min_size)
 if feasible<1:raise ValueError('最小段长大于样本数')
 dp=np.full((feasible+1,n+1),np.longdouble(np.inf));prev=np.full((feasible+1,n+1),-1,dtype=int);dp[0,0]=0
 for k in range(1,feasible+1):
  for end in range(k*min_size,n+1):
   starts=np.arange((k-1)*min_size,end-min_size+1);candidate=dp[k-1,starts]+costs.normalized(starts,end)
   # Relative longdouble roundoff ties prefer earliest prior cut, recursively.
   best=np.min(candidate);finite=np.isfinite(candidate)
   tolerance=np.finfo(np.longdouble).eps*64*np.maximum(np.abs(candidate[finite]),max(abs(best),np.finfo(np.longdouble).tiny))
   eligible=np.flatnonzero(finite)[candidate[finite]<=best+tolerance]
   index=int(eligible[0]);dp[k,end]=candidate[index];prev[k,end]=starts[index]
 return {'dp':dp,'previous':prev,'feasible_max_segments':feasible,'n':n}

def reconstruct(frontier,k):
 end=frontier['n'];segments=[]
 while k:
  start=int(frontier['previous'][k,end]);segments.append((start,end));end=start;k-=1
 if end!=0:raise ValueError('DP回溯失败')
 return list(reversed(segments))
