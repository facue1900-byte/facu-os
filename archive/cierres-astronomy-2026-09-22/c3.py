import sys,json,collections; sys.path.insert(0,'/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad')
from unid import load
A=[x for x in load()['Academy'] if '2025-04-11'<=x['fecha']<='2026-06-30']
def cl(x):
  f=x['fila']
  if f==597: return 'aporte socios'
  if f==877: return 'resultado Dominé (lo que mandó)'
  if f in(512,602): return 'venta Dominé'
  if f==612: return 'inversión Dominé'
  if x['tipo']=='Ingreso': return 'venta'
  return 'costo'
CUT='2025-12-18'
def run(mon):
  r=collections.defaultdict(float)
  for x in A:
    k=cl(x); per='hasta 18/12/25' if x['fecha']<=CUT else 'desde 19/12/25'
    r[(k,per)]+=x[mon]
  return r
if __name__=='__main__':
  st=[x for x in A if x['sub']=='Store']; print('STORE',[(x['fila'],x['fecha'],round(x['ars']),x['desc'][:40]) for x in st])
  for mon in('ars','usd'):
    r=run(mon); print('====',mon)
    for k,v in sorted(r.items()): print(' ',k,f"{v:,.0f}")
    for per in('hasta 18/12/25','desde 19/12/25'):
      res=r[('venta',per)]+r[('venta Dominé',per)]+r[('resultado Dominé (lo que mandó)',per)]-r[('costo',per)]
      print(' RESULTADO',per,f"{res:,.0f}")
  print('aporte fila 597 usd', [x['usd'] for x in A if x['fila']==597])
