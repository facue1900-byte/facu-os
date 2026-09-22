import json,datetime,collections,re
SP='/private/tmp/claude-501/-Users-Facu-facu-os/04f9b729-3b85-4c7f-9d3f-4f536f4922ca/scratchpad/'
R={v['range'].split('!')[0].strip("'"):v['values'] for v in json.load(open(SP+'fin2.json'))['valueRanges']}
fecha=lambda t:(datetime.date(1899,12,30)+datetime.timedelta(days=int(t))).isoformat()
base=sorted([x+['']*(9-len(x)) for x in R['Base'][1:]],key=lambda x:x[0])
SOCIOS={'Facu','Jaime','Vlado'}
def c(x):
    ts,per,bu,tipo,sub,mon,usd,ars,desc=[v.strip() if isinstance(v,str) else v for v in x[:9]]; ds=str(desc).lower(); s=sub
    G=lambda cl,cat,why:(cl,cat,True,why)
    N=lambda cl,cat,why='':(cl,cat,False,why)
    # --- reglas de Facu 22/09 ---
    if s=='MIDI': return N('Inversión','Equipos','Facu 22/09: MIDI va adentro de Equipos')
    if 'mejoras' in ds and ('sistema' in ds or 'software' in ds): return N('Costo','Software y sistema','Facu 22/09: mejoras del sistema = gasto')
    if 'electricista' in ds and s=='Inversión': return N('Costo','Mantenimiento','Facu 22/09: electricista = mejoras = costo')
    if s=='Cables' or 'cables' in ds: return N('Inversión','Equipos','Facu 22/09: cables son inversión aunque sean chicos')
    if 'electricista' in ds: return G('Costo','Mantenimiento','Electricista del armado del container (2023). Aplico tu regla "electricista = costo", pero era parte de la obra: confirmar')
    # --- inversión clara ---
    if s=='Equipos': return N('Inversión','Equipos')
    if s=='Acondicionamiento Container': return N('Inversión','Obra del estudio')
    if s=='Muebles y Decoración':
        if 'arreglo' in ds or 'ruedas' in ds: return G('Costo','Mantenimiento','Arreglo/repuesto, no un mueble nuevo')
        return G('Inversión','Muebles','La planilla lo tenía como Gasto; un escritorio o cortinas duran años')
    if s=='Inversión':
        if 'xdj' in ds: return N('Inversión','Equipos','Envío de la consola: es parte del costo del equipo')
        if 'ventilador' in ds or 'dimmer' in ds: return G('Inversión','Equipos','Chico, pero queda en el estudio (mismo criterio que cables)')
        if 'laca' in ds or 'mural' in ds: return G('Inversión','Obra del estudio','Pintar el mural: ¿obra o mantenimiento?')
    # --- costos claros ---
    COST={'Sueldos Profesores':'Sueldos profes','Pago Profesor VN':'Sueldos profes','Sueldos':'Sueldos','Dj':'DJs de eventos',
          'Suscripciones':'Suscripciones y software','Subscripción Web':'Suscripciones y software','Google Suites':'Suscripciones y software',
          'Dominio':'Suscripciones y software','Pagina WEB':'Suscripciones y software','Pauta Publicitaria':'Pauta',
          'Diseño Audiovisual':'Diseño y contenido','Diseño de imagen':'Diseño y contenido','Contenido':'Diseño y contenido',
          'Contenido Audiovisual':'Diseño y contenido','Flyers':'Diseño y contenido','Flyer':'Diseño y contenido',
          'Seña para 250 flyers colegios':'Diseño y contenido','Theatre':'Costo de evento','Seña 50% evento Renzo':'Costo de evento',
          'Gastos Corrientes':'Insumos del estudio','Consumibles':'Insumos del estudio','Productos':'Costo de lo vendido (plug-ins)',
          'Costo Combo 1 Plug-ins':'Costo de lo vendido (plug-ins)','Servicios':'Servicios'}
    if s in COST:
        if s=='Diseño Audiovisual' and 'raw' in ds: return G('Costo','Diseño y contenido','RAW $245.161: el más grande del rubro. En Responses había otro "Raw falso" $380.000 que NO está en Base')
        if s=='Servicios' and 'alan' in ds: return G('Costo','Servicios','"El hdp de alan": ¿qué servicio fue?')
        if s=='Servicios': return G('Costo','Costo de evento','Vino + etiquetas + QR: parece de un evento')
        return N('Costo',COST[s])
    if s=='Otros' and tipo=='Egreso':
        if 'pilas' in ds or 'agua' in ds: return N('Costo','Insumos del estudio','Era "Otros"')
        if 'vino' in ds or 'medialunas' in ds: return G('Costo','Atenciones a alumnos (jam)','Era "Otros": vino y medialunas de la jam')
        if 'asado' in ds: return G('Costo','Atenciones al equipo','Era "Otros": asado de fin de año. ¿Costo de la empresa o retiro de socios?')
        if 'fee' in ds: return N('Costo','Fee de artistas (Talent)','Era "Otros": la parte del artista en la fecha')
    if s=='Astronomy Mansion': return G('Aporte de socios','Saldo de socio','"Balance de Facu/Jaime/Vlado" nov-2023: ¿qué era Astronomy Mansion? Lo leo como plata que cada uno puso')
    # --- ventas ---
    VENTA={'Venta de Curso':'Cursos y membresías','Venta':'Cursos y membresías','Subs DJ Delivery':'DJ Delivery','Dj Delivery Zorro':'DJ Delivery',
           'Dj Delivery':'DJ Delivery','DJ Delivery':'DJ Delivery','Venta de Plug In':'Plug-ins','Alquiler Studio':'Alquiler de estudio/cabina',
           'Alquiler Cabina':'Alquiler de estudio/cabina','Comisión fanz sunset':'Eventos','Evento Sunset':'Eventos','Evento Jet':'Eventos',
           'Eventos Plaza':'Eventos','Eventos Astronomy':'Eventos'}
    if s in VENTA:
        if s=='Venta' and bu=='Astronomy Dominé' and 'gin' not in ds: return G('Venta','Cursos y membresías','Son alumnos (Simon, Felipe, Zorro) pero cargados en la caja Dominé: ¿van a Academy?')
        if 'gin' in ds: return G('Venta','Eventos','London GIN $3.000: ¿barra de un evento?')
        return N('Venta',VENTA[s])
    if s=='Otros' and tipo=='Ingreso':
        if 'fecha dome' in ds: return N('Venta','Booking (Talent)','Era "Otros": la fecha de Dome + Fran Niell')
        if 'rendimiento' in ds: return N('Venta','Rendimiento financiero','Era "Otros"')
        if 'tipo de cambio' in ds: return G('Ajuste (no es plata)','Ajuste','Mismo día y mismo monto (u$s 96 ×2) que "Mejoras del sistema": parece un asiento que se compensa solo')
        if 'ajuste de caja' in ds: return G('Ajuste (no es plata)','Ajuste','Ajuste de caja $132.997: plata que apareció al contar. ¿Se sabe de qué era?')
    # --- socios ---
    if s in('Retiro de Socios','Retiro de Ganancias') and tipo=='Egreso': return N('Retiro de socios','Retiro')
    if s=='Retiro de Ganancias' and tipo=='Ingreso' and per in SOCIOS:
        if 'consola' in ds: return G('Retiro de socios','Retiro','La venta de una consola repartida entre los tres: es desinversión + retiro')
        return N('Retiro de socios','Retiro (lo que cobró cada socio)','Contracara del egreso de la caja: no sumar dos veces')
    if s=='Aporte de Capital' and per in SOCIOS: return N('Aporte de socios','Aporte')
    if s=='Aporte de Capital' and tipo=='Ingreso': return G('Pase entre cajas','Pase','Academy → General el mismo día por el mismo monto')
    if s=='Gastos Ficticios': return G('Ajuste (no es plata)','Reparto de gastos comunes','Gasto común (oficina, luz, estudio) repartido entre cajas. Cargado como INGRESO')
    # --- lo que Person=Astronomy anotó como Retiro de Ganancias (INGRESO) ---
    if s=='Retiro de Ganancias':
        if 'comision' in ds or 'comisión' in ds: return G('Venta','Comisión venta de equipos','Estaba como "Retiro de Ganancias" pero es una comisión cobrada')
        if 'ventas de cursos' in ds: return G('Venta','Cursos y membresías','Estaba como "Retiro de Ganancias"')
        if 'antibes' in ds: return G('Venta','Alquiler de estudio/cabina','Alquiler de Antibes: ¿alquiler a un tercero?')
        if bu=='Astronomy Talent' and any(k in ds for k in('creta','zegre','palma','after')): return G('Venta','Booking (Talent)','Estaba como "Retiro de Ganancias" pero es una fecha cobrada')
        if 'devolucion seña' in ds or 'devolución seña' in ds: return G('Ajuste (no es plata)','Devolución de seña','Devolución de la seña de los domos ($1.500.000): baja un costo, no es venta')
        if 'alquiler ficticio' in ds: return G('Pase entre cajas','Alquiler interno','"Alquiler ficticio": una caja le cobra alquiler a otra')
        return G('Pase entre cajas','Pase','Plata que pasa de una caja a otra (o a la caja de retiros)')
    if s=='Aporte de Capital':
        if 'gastos de fiesta' in ds: return G('Costo','Costo de evento','Estaba como "Aporte de capital" pero es el pago de la fiesta')
        if 'boat' in ds: return G('Costo','Costo de evento','Pago a Lanfran por Boat: ¿costo del evento o reparto a socio?')
        if 'devolucion facu' in ds: return G('Retiro de socios','Devolución a socio','Devolución a Facu por Dome')
        if 'sueldo' in ds: return G('Costo','Sueldos','Estaba como "Aporte" pero es un sueldo pagado (José / Nico)')
        if 'software' in ds: return N('Costo','Software y sistema','Facu 22/09: mejoras del sistema = gasto')
        if 'suscrip' in ds: return G('Costo','Suscripciones y software','Estaba como "Aporte" pero es pago de suscripciones')
        if 'pauta' in ds and 'aporte' not in ds: return G('Costo','Pauta','Estaba como "Aporte"')
        if 'facebook ads' in ds: return G('Costo','Pauta','Facebook Ads de Dominé, pagado con plata de Academy')
        if 'silla' in ds: return G('Costo','Mantenimiento','Arreglar la silla')
        if 'milo' in ds: return G('Costo','Diseño y contenido','Pago a Milo, fondeado por Academy')
        if 'alquiler office' in ds: return G('Ajuste (no es plata)','Reparto de gastos comunes','Se cancela con el "Gasto ficticio" del mismo día, mismo monto')
        return G('Pase entre cajas','Pase','Plata que pasa de una caja a otra')
    return G('???','???','Sin regla')
rows=[]
for x in base:
    cl,cat,gris,why=c(x)
    rows.append(dict(fecha=fecha(x[0]),ts=x[0],per=x[1].strip(),bu=x[2].strip(),tipo=x[3].strip(),sub=x[4].strip(),mon=x[5],usd=float(x[6] or 0),ars=float(x[7] or 0),desc=str(x[8]),cl=cl,cat=cat,gris=gris,why=why))
json.dump(rows,open(SP+'clasif.json','w'),ensure_ascii=False)
if __name__=='__main__':
    print(collections.Counter(r['cl'] for r in rows)); print('gris',sum(r['gris'] for r in rows))
    for r in rows:
        if r['cl']=='???': print(r)

# ===== v2: reglas de Facu 22/09 (segunda tanda) =====
# Aporte de Capital (EGRESO) = sale de esa caja hacia otra área.
# Retiro de Ganancias (INGRESO) = entra a esa caja desde otra área.
EXTERNO=('comision','comisión','ventas de cursos','antibes','creta','zegre','palma','after jose')
for i,x in enumerate(rows):
    d=x['desc'].lower()
    if x['per']!='Astronomy': continue
    if x['sub']=='Aporte de Capital' and x['tipo']=='Egreso' and 'alquiler office' not in d:
        if 'devolucion facu' in d:
            x.update(cl='Retiro de socios',cat='Devolución de aporte a Facu',gris=False,why='Facu 22/09: le devolvieron a Facu lo que puso de su bolsillo para la seña de los domos')
        else:
            x.update(cl='Pase entre cajas',cat='Aporte a otra caja (sale)',gris=True,why='Facu 22/09: Aporte de capital = sale de esta caja hacia otra área')
    elif x['sub']=='Aporte de Capital' and x['tipo']=='Ingreso':
        x.update(cl='Pase entre cajas',cat='Llega de otra caja',gris=True,why='Entra desde otra caja')
    elif x['sub']=='Retiro de Ganancias' and x['tipo']=='Ingreso' and not any(k in d for k in EXTERNO) and 'devolucion seña' not in d:
        x.update(cl='Pase entre cajas',cat='Llega de otra caja',gris=True,why='Facu 22/09: Retiro de ganancias (ingreso) = entra desde otra área')
    if 'devolucion seña' in d:
        x.update(cl='Ajuste (no es plata)',cat='Seña devuelta (evento cancelado)',gris=True,why='Facu 22/09: evento que no se hizo, devolvieron la seña a Dominé. La SALIDA de la seña ($1.500.000) no está cargada en ningún lado: sólo los $530.000 que Facu puso y se le devolvieron')
# emparejar pases: mismo día, mismo monto ARS, uno sale y otro entra, cajas distintas
pases=[x for x in rows if x['cl']=='Pase entre cajas']
usado=set()
for a in pases:
    if id(a) in usado or a['tipo']!='Egreso': continue
    for b in pases:
        if id(b) in usado or b is a or b['tipo']!='Ingreso' or b['bu']==a['bu']: continue
        if b['fecha']==a['fecha'] and abs(b['ars']-a['ars'])<1:
            usado|={id(a),id(b)}
            for p,o in((a,b),(b,a)):
                p.update(gris=False,why=f"Pase: {'sale hacia' if p['tipo']=='Egreso' else 'llega desde'} {o['bu'].replace('Astronomy ','')} el mismo día por el mismo monto")
            break
# Dominé 2023 → los ingresos son devoluciones que Academy le hace a Dominé
DEV={'devolucion de aportes de capital','devolucion fondeo milo'}
for x in rows:
    if x['desc'].lower().strip() in DEV:
        x.update(gris=False,why='Academy le devuelve a Dominé lo que Dominé le prestó entre 05/09 y 21/10/2024: los 11 aportes suman $1.458.366 = $1.188.366 + $270.000, exacto')
for x in rows:
    if x['cl']=='Pase entre cajas' and x['gris']:
        x['why']+=' — SIN CONTRAPARTE: no hay en otra caja un movimiento del mismo día y monto. ¿De qué/para qué caja fue? ¿O es un costo?'
# alumnos cargados en Dominé → Academy (Facu 22/09), y lo que se le pagó al profe por esas clases
for x in rows:
    if x['bu']=='Astronomy Dominé' and x['fecha']<'2023-08-01' and (x['sub'] in('Venta','Sueldos Profesores','Pago Profesor VN')) and 'gin' not in x['desc'].lower():
        x.update(bu='Astronomy Academy',gris=False,why='Facu 22/09: los alumnos cargados en Dominé van a Academy (y el pago al profe de esas clases también). Caja original: Dominé')
json.dump(rows,open(SP+'clasif.json','w'),ensure_ascii=False)
if __name__=='__main__':
    print('v2 gris',sum(r['gris'] for r in rows)); print(collections.Counter(r['cl'] for r in rows))
    for r in rows:
        if r['cl']=='Pase entre cajas' and r['gris']: print('  SIN PAR',r['fecha'],r['bu'],r['tipo'],r['ars'],r['desc'])
