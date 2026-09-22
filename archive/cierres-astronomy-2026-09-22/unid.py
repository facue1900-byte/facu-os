import json,datetime,collections
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
U=json.load(open(SP+'unidades.json'))
B=datetime.date(1899,12,30)
def todate(t): return B+datetime.timedelta(days=int(t)) if isinstance(t,(int,float)) and t>0 else None
def load():
  out={}
  for ID,u in U.items():
    name=u['title'].replace('Finanzas - Astronomy ','')
    h=u['values'][0]; rows=[r+['']*(len(h)-len(r)) for r in u['values'][1:]]
    ix={k:h.index(k) for k in h if k}
    L=[]
    for n,r in enumerate(rows,start=2):
      ts=todate(r[ix['Timestamp']]); rd=todate(r[ix['Real Date']])
      f=rd; fix=''
      if rd is None: f=ts; fix='sin Real Date: uso Timestamp'
      elif rd.day<=12:
        try: sw=rd.replace(day=rd.month,month=rd.day)
        except ValueError: sw=None
        if sw and ts and sw<=ts+datetime.timedelta(days=3) and abs((ts-sw).days)<abs((ts-rd).days): f=sw; fix=f'día/mes invertidos ({rd.isoformat()})'
      L.append(dict(unidad=name,fila=n,fecha=f.isoformat(),ts=ts.isoformat() if ts else '',fix=fix,tipo=str(r[ix['Category']]).strip(),sub=str(r[ix['Sub Category']]).strip(),
        ars=float(r[ix['ARS_Ammount']] or 0),usd=float(r[ix['USD_Ammount']] or 0),desc=str(r[ix['Descripción']]).strip(),evento=str(r[ix['Event']]).strip() if 'Event' in ix else ''))
    out[name]=L
  return out
