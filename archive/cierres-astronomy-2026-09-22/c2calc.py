import json,collections
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
U=json.load(open(SP+'c2_unidades.json')); X=json.load(open(SP+'c2m.json')); mb=X['mb']; M=X['M']
def run(mon):
  cj={u:collections.defaultdict(float) for u in U}   # caja de cada unidad
  pl={u:collections.defaultdict(float) for u in U}   # resultado
  ma=collections.defaultdict(float)                  # caja maestra
  nota=[]
  ap={'Academy':33485 if mon=='ars' else 0}
  # apertura Academy en USD: neto pre-junio en USD
  for u,xs in U.items():
    for x in xs:
      v=x[mon]; c=x['cl']
      pass
      if c=='venta': cj[u]['ventas']+=v; pl[u]['ventas']+=v
      elif c=='costo': cj[u]['costos']-=v; pl[u]['costos']-=v
      elif c=='seña domos':
        s=v if x['tipo']=='Ingreso' else -v; cj[u]['seña domos (neto)']+=s; pl[u]['seña domos (neto)']+=s
      elif c=='devuelve aporte a Facu': cj[u]['devolución a Facu']-=v
      elif c=='a maestra': cj[u]['pases a la maestra']-=v
      elif c=='de maestra': cj[u]['pases desde la maestra']+=v
  # lado maestra: Base
  UNM={'Astronomy Academy':'Academy','Astronomy Dominé':'Dominé','Astronomy Talent':'Talent'}
  for x in mb:
    v=x[mon]
    if x['m_cl']=='unidad':
      u=x['u']
      if x['fila']==381: u='Dominé'                                            # Futura: es de Dominé
      if x.get('par') or x['fila'] in(289,381):
        ma['pases con '+u]+=x['dir']*v
      elif x['fila']==302:   # Dominé devuelve 270k (sólo en Base)
        nota.append('fila 302 fantasma')
      elif x['cl']=='Inversión':
        ma['equipos comprados para '+u]-=v; pl[u]['inversión (la pagó la maestra)']-=v
      elif x['cl'] in('Venta','Costo'):   # Talent cobrado/pagado directo por la maestra, software Academy
        s=x['dir']*v; ma['cobrado/pagado directo por '+u]+=s; pl[u]['ventas' if s>0 else 'costos']+=s
    elif x['m_cl']=='maestra propia':
      s=(1 if x['tipo']=='Ingreso' else -1)*v
      k='aportes de socios' if x['fila'] in(382,384) else 'ajustes' if x['cl'].startswith('Ajuste') else 'gastos propios (asado, sistema, oficina)'
      ma[k]+=s
  for x in M:
    if x.get('m_cl')=='retiro' and x['fila']!=311: ma['retiros de socios']-=x[mon]
    if x.get('m_cl')=='retiro' and x['fila']==311: ma['pases con Dominé']-=x[mon]   # 530k → Dominé → Facu
  # consola: Academy→maestra 376.500 y maestra→socios 3×124.000
  ac=[x for x in U['Academy'] if x['fila']==105][0]; ma['pases con Academy']+=ac[mon]
  cons=sum(x[mon] for x in M if x.get('m_cl')=='retiro consola (socio)'); ma['retiros de socios']-=cons
  # pases que sólo están en la planilla de Academy (expensas/alquiler que pagó la maestra)
  for f in(371,418,419):
    y=[x for x in U['Academy'] if x['fila']==f][0]; ma['pases con Academy (sólo en planilla Academy)']-=y[mon]
  return cj,pl,ma,nota
if __name__=='__main__':
  for mon in('ars','usd'):
    cj,pl,ma,n=run(mon); print('=========',mon)
    for u in cj:
      print(u,'CAJA',{k:round(v) for k,v in cj[u].items()},'→ cierre',round(sum(cj[u].values())))
      print('   RESULTADO',{k:round(v) for k,v in pl[u].items()},'→',round(sum(v for k,v in pl[u].items() if 'inversión' not in k)))
    print('MAESTRA',{k:round(v) for k,v in ma.items()},'→ cierre',round(sum(ma.values())))

def run2(mon):
  cj,pl,ma,n=run(mon)
  ap=33485 if mon=='ars' else None
  # apertura de Academy: neto de la planilla de Academy antes del 01/06/2024
  import sys; sys.path.insert(0,SP); from unid import load
  A=[x for x in load()['Academy'] if x['fecha']<'2024-06-01']
  cj['Academy']['saldo al 31/05/2024']=sum((1 if x['tipo']=='Ingreso' else -1)*x[mon] for x in A)
  # aportes "para costos ficticios" que la maestra mandó (sólo en planillas de unidad)
  for u in('Dominé','Talent'):
    for x in U[u]:
      if x['cl']=='de maestra' and 'ficticio' in x['desc'].lower(): ma['pases con '+u+' (sólo en planilla '+u+')']-=x[mon]
  return cj,pl,ma
if __name__=='__main__':
  out={}
  for mon in('ars','usd'):
    cj,pl,ma=run2(mon); out[mon]=dict(cj={u:dict(v) for u,v in cj.items()},pl={u:dict(v) for u,v in pl.items()},ma=dict(ma))
    print('=====',mon)
    for u in cj: print(u,'caja cierre',round(sum(cj[u].values())),'| resultado',round(sum(v for k,v in pl[u].items() if 'inversión' not in k)),'inversión',round(-pl[u].get('inversión (la pagó la maestra)',0)))
    print('MAESTRA',{k:round(v) for k,v in ma.items()},'→',round(sum(ma.values())))
  json.dump(out,open(SP+'c2res.json','w'),ensure_ascii=False)
