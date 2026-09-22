import json,datetime,collections
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
U=json.load(open(SP+'c2_unidades.json'))
R=json.load(open(SP+'clasif_v5.json'))
M=[dict(x,fila=i+2) for i,x in enumerate(R) if i>=253]   # filas 255 en adelante
assert M[0]['fila']==255
D=lambda s:datetime.date.fromisoformat(s)
UN={'Astronomy Academy':'Academy','Astronomy Dominé':'Dominé','Astronomy Talent':'Talent'}
pases_u=[dict(x,u=u,dir=(+1 if x['cl']=='a maestra' else -1),m=None) for u,xs in U.items() for x in xs if x['cl'] in('a maestra','de maestra')]
mb=[]
for x in M:
  if x['cl']=='No existió (ficticio)': x['m_cl']='ficticio'; continue
  if x['bu'].startswith('Socios'): x['m_cl']='espejo socio'; continue
  if x['per']!='Astronomy' and x['sub']=='Aporte de Capital': x['m_cl']='espejo aporte socio'; continue
  if x['per']!='Astronomy' and 'consola' in x['desc'].lower(): x['m_cl']='retiro consola (socio)'; continue
  if x['cl']=='Retiro de socios': x['m_cl']='retiro'; continue
  if x['bu'] in UN:
    x['m_cl']='unidad'; x['u']=UN[x['bu']]; x['dir']=(+1 if x['tipo']=='Ingreso' else -1)
  else: x['m_cl']='maestra propia'
  mb.append(x)
# emparejar
for x in [y for y in mb if y['m_cl']=='unidad']:
  best=None
  for p in pases_u:
    if p['m'] is not None or p['u']!=x['u'] or p['dir']!=x['dir']: continue
    dd=abs((D(p['fecha'])-D(x['fecha'])).days)
    if abs(p['ars']-x['ars'])<=max(2,0.035*x['ars']) and dd<=25:
      if best is None or dd<best[1]: best=(p,dd)
  if best: best[0]['m']=x['fila']; x['par']=best[0]['fila']
if __name__=='__main__':
  un=[x for x in mb if x['m_cl']=='unidad']
  print('Base filas unidad',len(un),'emparejadas',sum(1 for x in un if x.get('par')))
  print('\nBASE, tagueadas a una unidad y SIN par en la planilla de la unidad:')
  for x in un:
    if not x.get('par'): print(f"  fila {x['fila']} {x['fecha']} {x['u']:8} {'→maestra' if x['dir']>0 else 'maestra→'} {x['ars']:>11,.0f} {x['cl'][:14]:14} {x['desc'][:40]}")
  print('\nPLANILLAS DE UNIDAD, pases SIN par en Base:')
  for p in pases_u:
    if p['m'] is None: print(f"  {p['u']:8} fila {p['fila']} {p['fecha']} {'→maestra' if p['dir']>0 else 'maestra→'} {p['ars']:>11,.0f} {p['desc'][:45]}")
  print('\nmaestra propia:',[(x['fila'],x['fecha'],x['tipo'][:3],round(x['ars']),x['desc'][:25],x['cl']) for x in mb if x['m_cl']=='maestra propia'])
  print('retiros:',[(x['fila'],x['fecha'],round(x['ars']),x['desc']) for x in M if x.get('m_cl')=='retiro'])
  json.dump(dict(mb=mb,pases_u=pases_u,M=M),open(SP+'c2m.json','w'),ensure_ascii=False)
