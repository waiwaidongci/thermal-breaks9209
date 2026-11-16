import hashlib,json
VERSION='centered-scaled-exact-dp-v1'
def fingerprint(batch,points,config):
 normalized=[{key:(p[key].isoformat() if hasattr(p[key],'isoformat') else p[key]) for key in ('id','sequence','recorded_at','temperature')} for p in sorted(points,key=lambda x:x['sequence'])]
 payload={'version':VERSION,'batch':batch,'points':normalized,'config':config}
 return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
