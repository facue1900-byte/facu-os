import sys,json,datetime,collections
sys.path.insert(0,'/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad')
from unid import load
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
D=load(); I,F='2024-06-01','2025-04-10'
def clase(x):
  s=x['sub'].lower(); d=x['desc'].lower()
  if x['tipo']=='Egreso' and s.startswith('retiro de ganancia'): return 'a maestra'
  if x['tipo']=='Ingreso' and s=='aporte de capital': return 'de maestra'
  if x['tipo']=='Ingreso' and 'aporte de capital' in d: return 'de maestra'
  if 'devolucion facu' in d: return 'devuelve aporte a Facu'
  if 'seña domos' in d or 'seña domos' in d.replace('ñ','ñ') or ('seña' in d and 'domos' in d): return 'seña domos'
  if x['tipo']=='Ingreso': return 'venta'
  return 'costo'
U={}
for u,L in D.items():
  xs=[dict(x,cl=clase(x)) for x in L if I<=x['fecha']<=F]
  U[u]=xs
json.dump(U,open(SP+'c2_unidades.json','w'),ensure_ascii=False)
if __name__=='__main__':
  for u,xs in U.items():
    a=collections.defaultdict(float)
    for x in xs: a[x['cl']]+=x['ars']
    print(u,len(xs),{k:round(v) for k,v in a.items()})
    for x in xs:
      if x['cl'] in('seña domos','devuelve aporte a Facu') or ('ficticio' in x['desc'].lower()): print('   ',x['fecha'],x['tipo'],x['sub'],x['ars'],x['desc'],x['cl'])
