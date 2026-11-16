import numpy as np
from .dynamic_program import reconstruct

def select_partition(frontier,costs,penalty):
 ks=np.arange(1,frontier['feasible_max_segments']+1)
 rss=frontier['dp'][1:,frontier['n']]*costs.scale*costs.scale
 objectives=rss+np.longdouble(penalty)*(ks-1)
 best=np.min(objectives)
 # Relative machine-precision tie only; ascending K selects fewer segments.
 tolerance=np.finfo(np.longdouble).eps*64*np.maximum(np.abs(objectives),max(abs(best),np.finfo(np.longdouble).tiny))
 index=int(np.flatnonzero(objectives<=best+tolerance)[0]);k=int(ks[index]);parts=reconstruct(frontier,k)
 segments=[dict(position=i+1,**costs.segment(start,end)) for i,(start,end) in enumerate(parts)]
 return {'penalty':float(penalty),'segments_count':k,'breakpoints':[end for _,end in parts[:-1]],'rss':float(rss[index]),'objective':float(objectives[index]),'segments':segments,'adjacent_mean_differences':[{'breakpoint':left['end'],'left_mean':left['mean'],'right_mean':right['mean'],'difference':right['mean']-left['mean']} for left,right in zip(segments,segments[1:])]}

def evaluate_path(frontier,costs,penalties):
 return [select_partition(frontier,costs,b) for b in sorted(set(penalties))]
