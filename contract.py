"""Public data contract. Contains no IGNISPYRO calculation engines."""
import datetime, hashlib, json, math, re
SOURCE='https://api.ipma.pt/open-data/observation/meteorology/stations/stations.json'
def encode(value): return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
def validate_stations(data):
 if set(data)!={'type','source','features'} or data['type']!='FeatureCollection' or data['source']!=SOURCE: raise ValueError('Invalid public dataset')
 if not isinstance(data['features'],list) or not 1<=len(data['features'])<=5000: raise ValueError('Invalid feature count')
 seen=set()
 for f in data['features']:
  if not isinstance(f,dict) or set(f)!={'type','geometry','properties'} or f['type']!='Feature':raise ValueError('Invalid feature')
  g=f['geometry'];p=f['properties']
  if not isinstance(g,dict) or set(g)!={'type','coordinates'} or g['type']!='Point':raise ValueError('Invalid geometry')
  c=g['coordinates']
  if not isinstance(c,list) or len(c)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in c) or not -180<=c[0]<=180 or not -90<=c[1]<=90:raise ValueError('Invalid coordinates')
  if not isinstance(p,dict) or set(p)!={'station_id','name','source'} or p['source']!='IPMA':raise ValueError('Non-public property')
  if type(p['station_id']) is not int or not 0<p['station_id']<10**10 or p['station_id'] in seen:raise ValueError('Invalid station id')
  seen.add(p['station_id'])
  name=p['name']
  if not isinstance(name,str) or not 1<=len(name)<=120 or any(ord(c)<32 for c in name) or re.search(r'password|secret|token|https?://|-----BEGIN|[A-Za-z0-9_=-]{48,}',name,re.I):raise ValueError('Unsafe station name')
 return data
def validate_package(root):
 root=__import__('pathlib').Path(root)
 m=json.loads((root/'manifest.json').read_text('utf-8'))
 if set(m)!={'schema','published_at','products'} or m['schema']!='ignispyro-public-products/1' or len(m['products'])!=1:raise ValueError('Invalid manifest')
 dt=datetime.datetime.fromisoformat(m['published_at'].replace('Z','+00:00'))
 if dt.utcoffset()!=datetime.timedelta(0):raise ValueError('UTC required')
 p=m['products'][0]
 if set(p)!={'id','title','path','sha256','bytes','source','kind'} or p['id']!='ipma-stations' or p['kind']!='station-catalogue' or p['title']!='Estações IPMA (catálogo)' or p['source']!=SOURCE:raise ValueError('Invalid product')
 if not re.fullmatch(r'products/ipma-stations-[a-f0-9]{64}\.geojson',p['path']) or p['path']!='products/ipma-stations-'+p['sha256']+'.geojson':raise ValueError('Invalid product path')
 path=root/p['path']
 if path.is_symlink() or path.resolve().parent!=(root/'products').resolve():raise ValueError('Unsafe product path')
 payload=path.read_bytes()
 if len(payload)>2_000_000 or type(p['bytes']) is not int or len(payload)!=p['bytes'] or hashlib.sha256(payload).hexdigest()!=p['sha256']:raise ValueError('Product digest mismatch')
 validate_stations(json.loads(payload))
 return m
