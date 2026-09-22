import json,sys,collections
sys.path.insert(0,'/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad')
from unid import load
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
U=json.load(open(SP+'c2_unidades.json')); X=json.load(open(SP+'c2m.json')); mb=X['mb']; M=X['M']
FIC_COSTO={'Academy':{323,324,325,328,349,350,354,382,383},'Dominé':{91,92,101},'Talent':{13,17,32}}
FIC_APORTE={'Academy':{371,418,419},'Dominé':{90,103},'Talent':{12,39}}
BASE_FIC_PAR={330,332}          # aporte "Alquiler Office 33%" de la maestra, par del gasto ficticio del mismo día
def run(mon):
  cj={u:collections.defaultdict(float) for u in U}; pl={u:collections.defaultdict(float) for u in U}; ma=collections.defaultdict(float)
  A=[x for x in load()['Academy'] if x['fecha']<'2024-06-01']
  cj['Academy']['saldo al 31/05/2024']=sum((1 if x['tipo']=='Ingreso' else -1)*x[mon] for x in A)
  fic=collections.defaultdict(float)
  for u,xs in U.items():
    for x in xs:
      v=x[mon]; c=x['cl']
      if x['fila'] in FIC_COSTO[u]: fic[u]+=v; cj[u]['ficticios (no se pagaron)']-=v; continue
      if x['fila'] in FIC_APORTE[u]: fic[u]-=v; cj[u]['aportes para ficticios']+=v; continue
      if c=='venta': cj[u]['ventas']+=v; pl[u]['ventas']+=v
      elif c=='costo': cj[u]['costos']-=v; pl[u]['costos']-=v
      elif c=='seña domos': s=v if x['tipo']=='Ingreso' else -v; cj[u]['seña domos']+=s; pl[u]['seña domos (neto)']+=s
      elif c=='devuelve aporte a Facu': cj[u]['devolución a Facu']-=v
      elif c=='a maestra': cj[u]['pases a la maestra']-=v
      elif c=='de maestra': cj[u]['pases desde la maestra']+=v
  for x in mb:
    v=x[mon]
    if x['m_cl']=='unidad':
      if x['fila'] in BASE_FIC_PAR: continue
      u='Dominé' if x['fila']==381 else x['u']
      if x.get('par') or x['fila'] in(289,381): ma['pases con las unidades']+=x['dir']*v
      elif x['fila']==302: pass
      elif x['cl']=='Inversión': ma['equipos para Academy']-=v; pl[u]['inversión']-=v
      elif x['cl'] in('Venta','Costo'): s=x['dir']*v; ma['Talent cobrado/pagado directo']+=s; pl[u]['ventas' if s>0 else 'costos']+=s
    elif x['m_cl']=='maestra propia':
      s=(1 if x['tipo']=='Ingreso' else -1)*v
      if x['fila'] in(382,384): ma['aportes de socios']+=s
      elif x['cl']=='Inversión': ma['inversión propia (dimmer)']+=s
      elif x['cl'].startswith('Ajuste'): ma['ajustes']+=s
      else: ma['gastos propios']+=s
  for x in M:
    if x.get('m_cl')=='retiro':
      if x['fila']==311: ma['pases con las unidades']-=x[mon]
      else: ma['retiros de socios']-=x[mon]
  ac=[x for x in U['Academy'] if x['fila']==105][0]; ma['pases con las unidades']+=ac[mon]
  ma['retiros de socios']-=sum(x[mon] for x in M if x.get('m_cl')=='retiro consola (socio)')
  return cj,pl,ma,fic
if __name__=='__main__':
  out={}
  for mon in('ars','usd'):
    cj,pl,ma,fic=run(mon); out[mon]=dict(cj={k:dict(v) for k,v in cj.items()},pl={k:dict(v) for k,v in pl.items()},ma=dict(ma),fic=dict(fic))
    print('=====',mon)
    for u in cj: print(u,'caja',round(sum(cj[u].values())),{k:round(v) for k,v in cj[u].items()})
    print('   ficticios netos por unidad (costo ficticio − aporte ficticio):',{k:round(v) for k,v in fic.items()})
    print('MAESTRA',round(sum(ma.values())),{k:round(v) for k,v in ma.items()})
    tot=sum(sum(cj[u].values()) for u in cj)+sum(ma.values()); print('TOTAL CAJAS',round(tot))
  json.dump(out,open(SP+'c2v2.json','w'),ensure_ascii=False)
