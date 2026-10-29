#!/usr/bin/env python3
"""Arma un reel entero desde un guion JSON: tomas reales + textos + voz en off + drop de Sin City
+ portada con la estética de la grilla. Lo usa el agente diario; también sirve a mano.

    .venv/bin/python active/astronomy/contenido/reels_diarios/armar_reel.py GUION.json

Deja en la carpeta del guion: reel.mp4, portada.jpg, texto-reel.txt y qa.json.
Imprime REEL_OK <carpeta> si pasó todos los chequeos; si no, sale con error y dice cuál falló.

Guion (las claves con * son obligatorias):
{
 "slug"*: "swipe-falso",
 "formato"*: "swipe falso — de dónde salió la idea (link)",
 "tema"*: "go-back",                    # temas.json
 "drop"*: 6.0,                          # segundo del reel donde cae el drop
 "tomas"*: [{"archivo": "...", "desde": 12.0, "dur": 1.5, "x": 0.5, "zoom": 1.0, "efecto": "slam"}],
          # se pegan en orden; la suma de `dur` es el largo del reel. `x` = dónde centrar el recorte
          # 9:16 en un cuadro horizontal (0 izquierda … 1 derecha). efecto: slam | oscuro | null.
 "textos": [{"texto": "...", "desde": 0, "hasta": 2.5, "pos": "arriba|centro|abajo"}],
          # carteles a mano SÓLO donde no habla la voz (ej. el hook antes de que arranque):
          # mientras habla, los subtítulos salen SOLOS de los tiempos reales de la voz (Whisper).
 "carteles_beat": [{"texto": "DEJÁ EL CELULAR", "desde": 0.0, "cada": 1, "hasta": 3.0}],
          # texto GRANDE al centro que se arma palabra por palabra, una cada `cada` golpes del tema
          # (formato de las referencias de Facu del 29/10: «GIVE ME A SIGN», «PUT THAT PHONE DOWN…»).
          # Queda completo hasta `hasta`. Cuenta como cartel: no puede pisar la voz.
 "voz": {"texto": "...", "palabra_drop": "Astronomy"},   # la palabra cae justo en el drop
 "antes_del_drop": "filtro",           # filtro (build con pasa-bajos) | seco (silencio y golpe)
 "portada"*: {"titular": "LO QUE NADIE<br>TE MUESTRA", "ceja": "THE BUNKER", "toma": 0, "segundo": 1.0},
 "caption"*: "..."
}
"""
import difflib
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from comun import FF, OS, TEMAS, WHATSAPP, duracion, ff, info
import portada as portada_mod

FPS = 30
W, H = 1080, 1920
LOOK = "eq=contrast=1.08:saturation=1.05"
SLAM = (",fade=in:st=0:d=0.10:color=white,"
        "zoompan=z='max(1.0,1.15-0.8*on/30)':d=1:s=1080x1920:fps=30:"
        "x='iw/2-(iw/zoom/2)+30*sin(on*2.9)*exp(-on/5)':y='ih/2-(ih/zoom/2)+24*cos(on*3.3)*exp(-on/5)'")
# Modelos de voz por orden. El 2.5-flash es el que dio el acento rioplatense verificado (27/10);
# tiene cuota de 10 pedidos por día, por eso la voz se cachea por texto y los otros son respaldo.
MODELOS_VOZ = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts", "gemini-3.8-flash-tts"]
CACHE_VOZ = pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/Reels-diarios/_voces")
FUENTE = "/System/Library/Fonts/HelveticaNeue.ttc"
MAX_MB = 50     # límite del bucket temporal de publicar_reel.py


def falla(msg):
    sys.exit(f"REEL_FALLA: {msg}")


# ---------------------------------------------------------------- video

def recorte(t, w, h):
    """El filtro que lleva un cuadro de la fuente al 9:16 del reel (lo usan la toma y la portada)."""
    z = float(t.get("zoom", 1.0))
    if w > h:   # horizontal → recorte 9:16 centrado en x
        cw = int(h * 9 / 16 / z) // 2 * 2
        ch = int(h / z) // 2 * 2
        x0 = int(max(0, min(w - cw, float(t.get("x", 0.5)) * w - cw / 2)))
        y0 = (h - ch) // 2
        vf = f"crop={cw}:{ch}:{x0}:{y0},scale={W}:{H}:flags=lanczos"
    else:
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        if z != 1.0:
            vf += f",crop=iw/{z}:ih/{z},scale={W}:{H}:flags=lanczos"
    return vf


def toma(t, out, n_cuadros):
    src = pathlib.Path(t["archivo"])
    if not src.exists():
        falla(f"no existe la toma {src}")
    dur, w, h = info(src)
    if t["desde"] + t["dur"] > dur + 0.05:
        falla(f"la toma {src.name} pide hasta {t['desde'] + t['dur']:.1f}s y dura {dur:.1f}s")
    vf = f"fps={FPS},{recorte(t, w, h)},setsar=1,{LOOK}"
    if t.get("efecto") == "slam":
        vf += SLAM
    elif t.get("efecto") == "oscuro":
        vf += ",eq=brightness=-0.12"
    ff("-ss", t["desde"], "-i", src, "-frames:v", n_cuadros, "-vf", vf,
       "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", FPS, "-an", out)


def placa_texto(texto, pos, out, completo=None):
    """Texto en el lenguaje de la cuenta: mayúsculas, Helvetica Neue Medium, blanco, centrado,
    con sombra difusa. Respeta las zonas que tapa la interfaz de Reels (abajo y a la derecha)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    grande = pos == "grande"
    # Con `completo`, el tamaño y el corte de líneas se calculan sobre el texto ENTERO: al armarse
    # palabra por palabra las líneas no saltan de lugar.
    base = (completo or texto).upper()
    tam, alto_max, piso = (150, 900, 70) if grande else (74, 560, 46)
    while True:
        f = ImageFont.truetype(FUENTE, tam, index=1 if grande else 10)
        lineas = envolver(base, f, d, 860)
        alto = len(lineas) * int(tam * 1.12)
        ancho_max = max(d.textlength(l, font=f) for l in lineas)
        if (alto < alto_max and ancho_max <= 900) or tam <= piso:
            break
        tam -= 4
    if completo:
        quedan = len(texto.split())
        visibles = []
        for l in lineas:
            n = len(l.split())
            visibles.append(" ".join(l.split()[:max(0, quedan)]))
            quedan -= n
        lineas = visibles
    # «abajo» termina como mucho a 1500 px: más abajo lo tapan el caption y los botones de Reels.
    y = {"arriba": 300, "centro": (H - alto) // 2 - 80, "abajo": 1500 - alto, "sub": 1200,
         "grande": (H - alto) // 2 - 60}.get(pos, 300)
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    for i, l in enumerate(lineas):
        if not l:
            continue
        lw = d.textlength(l, font=f)
        xy = ((W - 60 - lw) / 2, y + i * int(tam * 1.12))   # corrido 30 px a la izquierda: botones de IG
        ds.text(xy, l, font=f, fill=(0, 0, 0, 200))
        d.text(xy, l, font=f, fill=(255, 255, 255, 255))
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    Image.alpha_composite(sombra, im).save(out)


def subtitulos(texto, pal, inicio):
    """Subtítulos de 1 a 4 palabras con los tiempos REALES de cada palabra (Whisper), corridos al
    lugar de la voz en el reel. Se escribe el texto del guion (bien escrito) si Whisper oyó la
    misma cantidad de palabras; si no, lo que oyó Whisper."""
    escritas = texto.split()
    palabras_ = escritas if len(escritas) == len(pal) else [p[2] for p in pal]
    grupos, actual = [], []
    for w, p in zip(palabras_, pal):
        actual.append((w, p[0], p[1]))
        largo = len(" ".join(x[0] for x in actual))
        if len(actual) == 4 or largo >= 16 or w[-1] in ".,?!:;":
            grupos.append(actual)
            actual = []
    if actual:
        grupos.append(actual)
    subs = []
    for i, gr in enumerate(grupos):
        a = inicio + gr[0][1]
        b = inicio + (grupos[i + 1][0][1] if i + 1 < len(grupos) else gr[-1][2] + 0.35)
        subs.append((" ".join(x[0] for x in gr), a, b))
    return subs


def envolver(texto, f, d, ancho):
    lineas = []
    for parrafo in texto.split("\n"):
        actual = ""
        for p in parrafo.split():
            prueba = f"{actual} {p}".strip()
            if d.textlength(prueba, font=f) <= ancho:
                actual = prueba
            else:
                lineas.append(actual)
                actual = p
        lineas.append(actual)
    return [l for l in lineas if l]


# ---------------------------------------------------------------- voz

def voz(texto, out):
    """Toma de voz Charon rioplatense. Cacheada por texto: un reintento no gasta cuota."""
    CACHE_VOZ.mkdir(parents=True, exist_ok=True)
    clave = hashlib.sha1(texto.encode()).hexdigest()[:16]
    cache = CACHE_VOZ / f"{clave}.wav"
    meta = CACHE_VOZ / f"{clave}.json"
    if cache.exists() and meta.exists():
        out.write_bytes(cache.read_bytes())
        return json.loads(meta.read_text())["modelo"]
    sys.path.insert(0, str(OS / "execution"))
    import gemini
    from google.genai import types
    errores = []
    for m in MODELOS_VOZ:
        try:
            r = gemini.cliente().models.generate_content(
                model=m,
                contents="Say in an Argentine Spanish (rioplatense) accent, curious confident narrator tone, natural pace: " + texto,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")))))
            pcm = r.candidates[0].content.parts[0].inline_data.data
            meta.write_text(json.dumps({"modelo": m, "texto": texto}, ensure_ascii=False))
            with wave.open(str(cache), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            out.write_bytes(cache.read_bytes())
            return m
        except Exception as e:  # cuota, 503: se prueba el siguiente
            errores.append(f"{m}: {str(e)[:100]}")
    falla("ningún modelo de voz respondió: " + " | ".join(errores))


def palabras(wav):
    from faster_whisper import WhisperModel
    import numpy as np
    # Se le pasa el audio ya decodificado: el `av` que trae el venv no acepta lo que
    # faster-whisper le pide al abrir archivos (metadata_errors).
    pcm = subprocess.run([FF, "-nostdin", "-v", "error", "-i", str(wav), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(np.frombuffer(pcm, dtype=np.float32), language="es", word_timestamps=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]


def refinar(pal, wav):
    """Whisper pone mal el inicio de la palabra que sigue a una pausa (hasta 0,5 s antes: el
    subtítulo aparecía antes que la voz). Si en el inicio que dio Whisper la voz está en silencio,
    se corre al primer cuadro de 10 ms donde la voz realmente suena."""
    import numpy as np
    pcm = subprocess.run([FF, "-nostdin", "-v", "error", "-i", str(wav), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, dtype=np.float32)
    env = np.array([np.sqrt((x[i:i + 160] ** 2).mean()) for i in range(0, len(x) - 160, 160)])
    umbral = max(env.max() * 0.06, 1e-4)
    nuevas = []
    for k, (a, b, w) in enumerate(pal):
        i = int(a * 100)
        if i < len(env) and env[i] < umbral:
            tope = min(len(env), int(min(b, a + 0.7) * 100))
            j = next((j for j in range(i, tope) if env[j] >= umbral), None)
            if j is not None:
                a = j / 100
        nuevas.append((a, max(b, a + 0.05), w))
    return nuevas


def normal(s):
    return re.sub(r"[^a-záéíóúñü]", "", s.lower())


# ---------------------------------------------------------------- armado

def armar(guion_path):
    guion_path = pathlib.Path(guion_path).resolve()
    g = json.loads(guion_path.read_text())
    for k in ("slug", "formato", "tema", "drop", "tomas", "portada", "caption"):
        if k not in g:
            falla(f"al guion le falta `{k}`")
    carpeta = guion_path.parent
    # Lo de una corrida anterior se borra ANTES de empezar: si esta corrida falla a la mitad, no
    # puede quedar un qa.json verde de antes al lado de un reel.mp4 nuevo.
    for f in ("qa.json", "reel.mp4", "portada.jpg", "texto-reel.txt", "revision.jpg"):
        (carpeta / f).unlink(missing_ok=True)
    temas = {t["tema"]: t for t in json.loads(TEMAS.read_text())}
    if g["tema"] not in temas:
        falla(f"tema `{g['tema']}` no está en temas.json ({sorted(temas)})")
    tema = temas[g["tema"]]
    total = round(sum(t["dur"] for t in g["tomas"]), 3)
    drop = float(g["drop"])
    if not (6 <= total <= 45):
        falla(f"el reel dura {total}s: tiene que estar entre 6 y 45")
    if not (1.0 <= drop <= total - 1.0):
        falla(f"el drop ({drop}s) tiene que caer adentro del reel ({total}s)")
    if duracion(tema["archivo"]) < tema["drop"] + (total - drop) + 0.2:
        falla(f"el tema {tema['titulo']} no alcanza: después del drop hacen falta {total - drop:.1f}s")
    qa = {"slug": g["slug"], "duracion_guion": total, "drop": drop, "tema": tema["titulo"]}

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        # --- video
        lista, t, cortes = [], 0.0, []
        for i, tm in enumerate(g["tomas"]):
            fin = t + tm["dur"]
            n = round(fin * FPS) - round(t * FPS)
            out = tmp / f"t{i:02d}.mp4"
            toma(tm, out, n)
            lista.append(f"file '{out}'")
            cortes.append(round(t, 3))
            t = fin
        (tmp / "lista.txt").write_text("\n".join(lista) + "\n")
        ff("-f", "concat", "-safe", 0, "-i", tmp / "lista.txt", "-c", "copy", tmp / "video.mp4")

        # --- voz
        inicio_voz = None
        if g.get("voz"):
            vwav = tmp / "voz.wav"
            qa["modelo_voz"] = voz(g["voz"]["texto"], vwav)
            pal = refinar(palabras(vwav), vwav)
            qa["voz_transcripta"] = " ".join(p[2] for p in pal)
            parecido = difflib.SequenceMatcher(None, normal(g["voz"]["texto"]), normal(qa["voz_transcripta"])).ratio()
            qa["voz_parecido"] = round(parecido, 2)
            if parecido < 0.85:
                falla(f"la voz no dice lo pedido (parecido {parecido:.2f}): oyó «{qa['voz_transcripta']}». "
                      "Cambiá apenas el texto (una coma, una palabra) para pedir otra toma")
            objetivo = normal(g["voz"].get("palabra_drop", "Astronomy"))
            if len(objetivo) < 4:
                falla("`palabra_drop` tiene que ser una palabra de verdad (ej. Astronomy)")
            hit = [p for p in pal if normal(p[2]).startswith(objetivo[:5])]
            if not hit:
                falla(f"Whisper no oyó «{g['voz'].get('palabra_drop')}» en la voz: «{qa['voz_transcripta']}»")
            # La última vez que aparece: si «Astronomy» también está en el hook, el drop va en la del final.
            inicio_voz = round(drop - hit[-1][0], 3)
            dur_voz = pal[-1][1]
            if inicio_voz < 0:
                falla(f"la voz llega a la palabra del drop a los {hit[-1][0]:.2f}s y el drop está a los {drop}s: "
                      "acortá el texto antes de la palabra o corré el drop más tarde")
            if inicio_voz + dur_voz > total - 0.1:
                falla(f"la voz termina a los {inicio_voz + dur_voz:.2f}s y el reel dura {total}s: alargá las tomas")
            qa["voz_inicio"] = inicio_voz
            qa["palabra_en_drop"] = round(inicio_voz + hit[-1][0], 3)

        # --- audio
        pre = drop
        dt = tema["drop"]
        if dt - pre < 0:
            falla(f"el tema tiene sólo {dt}s antes del drop y el reel pide {pre}s")
        filtros = []
        if g.get("antes_del_drop", "filtro") == "seco":
            filtros.append(f"[0:a]aresample=48000,volume=0.25,afade=in:d=0.3,afade=out:st={max(0, pre - 0.6):.3f}:d=0.5[build]")
        else:
            barrido = ";".join(f"{x * pre:.2f} lowpass f {hz}" for x, hz in
                               [(0, 300), (.3, 600), (.55, 1200), (.75, 2500), (.88, 5000), (.96, 12000)])
            filtros.append(f"[0:a]aresample=48000,asendcmd=c='{barrido}',lowpass=f=300,"
                           f"volume='0.45+0.55*t/{pre:.3f}':eval=frame,afade=in:d=0.4[build]")
        filtros.append(f"[1:a]aresample=48000,afade=in:d=0.004,afade=out:st={max(0.1, total - drop - 0.8):.2f}:d=0.8,"
                       f"adelay={int(drop * 1000)}:all=1[dropa]")
        # apad: sidechaincompress corta en el input MÁS CORTO; sin esto el audio terminaba con la voz
        # y los últimos segundos del reel quedaban mudos (los 10 del 28/10/2026).
        filtros.append(f"[build][dropa]amix=inputs=2:normalize=0,volume=0.6,apad=whole_dur={total:.3f}[musica]")
        entradas = ["-ss", dt - pre, "-t", pre, "-i", tema["archivo"],
                    "-ss", dt, "-t", total - drop, "-i", tema["archivo"]]
        if inicio_voz is not None:
            entradas += ["-i", tmp / "voz.wav"]
            filtros.append(f"[2:a]aresample=48000,aformat=channel_layouts=stereo,afade=in:d=0.02,"
                           f"adelay={int(inicio_voz * 1000)}:all=1,volume=1.5,apad=whole_dur={total:.3f},asplit[voz][sc]")
            filtros.append("[musica][sc]sidechaincompress=threshold=0.04:ratio=5:attack=8:release=280[md]")
            filtros.append(f"[voz][md]amix=inputs=2:normalize=0,alimiter=limit=0.7:level=disabled,atrim=0:{total:.3f}[a]")
        else:
            filtros.append(f"[musica]alimiter=limit=0.7:level=disabled,atrim=0:{total:.3f}[a]")
        ff(*entradas, "-filter_complex", ";".join(filtros), "-map", "[a]", "-ac", 2, "-ar", 48000, tmp / "audio.wav")

        # --- textos y mux
        textos = list(g.get("textos", []))
        golpe = 60 / tema["bpm"]
        for cb in g.get("carteles_beat", []):
            ws = cb["texto"].split()
            paso = golpe * float(cb.get("cada", 1))
            hasta = float(cb.get("hasta", cb["desde"] + paso * (len(ws) + 1)))
            for k in range(1, len(ws) + 1):
                a = cb["desde"] + paso * (k - 1)
                b = a + paso if k < len(ws) else hasta
                if b <= a:
                    falla(f"el cartel «{cb['texto']}» no entra: `hasta` ({hasta}s) es antes de la última palabra")
                textos.append({"texto": " ".join(ws[:k]), "completo": cb["texto"], "desde": round(a, 3),
                               "hasta": round(b, 3), "pos": "grande"})
        if inicio_voz is not None:
            fin_voz = inicio_voz + dur_voz
            for tx in textos:
                if tx["desde"] < fin_voz and tx["hasta"] > inicio_voz:
                    falla(f"el cartel «{tx['texto']}» ({tx['desde']}–{tx['hasta']}s) pisa la voz ({inicio_voz:.2f}–"
                          f"{fin_voz:.2f}s): mientras habla, los subtítulos salen solos. Sacalo o ponelo fuera de la voz")
            subs = subtitulos(g["voz"]["texto"], pal, inicio_voz)
            qa["subtitulos"] = [[t, round(a, 2), round(b, 2)] for t, a, b in subs]
            textos += [{"texto": t, "desde": a, "hasta": b, "pos": "sub"} for t, a, b in subs]
        ins, cad, prev = ["-i", tmp / "video.mp4", "-i", tmp / "audio.wav"], [], "[0:v]"
        for i, tx in enumerate(textos):
            png = tmp / f"tx{i}.png"
            placa_texto(tx["texto"], tx.get("pos", "arriba"), png, tx.get("completo"))
            ins += ["-i", png]
            cad.append(f"{prev}[{i + 2}:v]overlay=0:0:enable='between(t,{tx['desde']:.3f},{tx['hasta'] - 0.001:.3f})'[o{i}]")
            prev = f"[o{i}]"
        mp4 = carpeta / "reel.mp4"
        mapa = ["-filter_complex", ";".join(cad), "-map", prev] if cad else ["-map", "0:v"]
        ff(*ins, *mapa, "-map", "1:a", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "-t", f"{total:.3f}", mp4)

        # --- portada (de un cuadro de la toma pedida, sin textos encima)
        p = g["portada"]
        tp = g["tomas"][int(p.get("toma", 0))]
        seg = float(p.get("segundo", 0.5))
        if not 0 <= seg < tp["dur"]:
            falla(f"portada.segundo ({seg}) tiene que caer adentro de la toma ({tp['dur']}s)")
        _, sw, sh = info(tp["archivo"])
        cuadro = tmp / "cuadro-portada.jpg"
        ff("-ss", tp["desde"] + seg, "-i", tp["archivo"], "-frames:v", 1, "-q:v", 2,
           "-vf", recorte(tp, sw, sh), cuadro)
        portada_mod.armar(carpeta / "portada.jpg", p["titular"], p.get("ceja"), foto=cuadro)

    # --- caption: siempre con el WhatsApp
    cap = g["caption"].strip()
    if WHATSAPP not in cap:
        cap += f"\n\nEscribinos por WhatsApp: {WHATSAPP}"
    (carpeta / "texto-reel.txt").write_text(cap + "\n")

    # --- QA sobre el archivo final
    dur, w, h = info(mp4)
    vd = subprocess.run([FF, "-nostdin", "-i", str(mp4), "-af", "volumedetect", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    pico = float(re.search(r"max_volume: (-?[\d.]+)", vd).group(1))
    media = float(re.search(r"mean_volume: (-?[\d.]+)", vd).group(1))
    mb = mp4.stat().st_size / 1e6
    import numpy as np
    pcm = subprocess.run([FF, "-nostdin", "-v", "error", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, dtype=np.float32)
    dur_audio = len(x) / 8000
    db = [20 * np.log10(np.sqrt((x[i:i + 2000] ** 2).mean()) + 1e-9) for i in range(0, len(x) - 2000, 2000)]
    mudos = [round(i * 0.25, 2) for i, v in enumerate(db) if v < -45]
    qa.update({"duracion_audio": round(dur_audio, 2), "tramos_mudos": mudos})
    qa.update({"duracion_final": round(dur, 2), "tamano": f"{w}x{h}", "pico_db": pico, "media_db": media,
               "mb": round(mb, 1), "cortes": cortes})
    problemas = []
    if abs(dur - total) > 0.15:
        problemas.append(f"dura {dur:.2f}s y el guion dice {total}s")
    if (w, h) != (W, H):
        problemas.append(f"mide {w}x{h}")
    if pico > -0.5:
        problemas.append(f"el audio clipea (pico {pico} dB)")
    if media < -32:
        problemas.append(f"el audio casi no se oye (media {media} dB)")
    if abs(dur_audio - total) > 0.15:
        problemas.append(f"el audio dura {dur_audio:.2f}s y el reel {total}s")
    if mudos:
        problemas.append(f"hay audio mudo (< -45 dB) en {mudos[:6]}s")
    if mb > MAX_MB:
        problemas.append(f"pesa {mb:.0f} MB y el límite de subida es {MAX_MB}")
    qa["problemas"] = problemas
    if not problemas:
        hoja_revision(mp4, cortes, total, carpeta)
    # El qa.json va ÚLTIMO, con la huella del reel: publicar.py exige que coincidan.
    qa["ok"] = not problemas
    qa["sha_reel"] = hashlib.sha256(mp4.read_bytes()).hexdigest()[:20]
    (carpeta / "qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1))
    if problemas:
        falla("; ".join(problemas))
    print("REEL_OK", carpeta)


def hoja_revision(mp4, cortes, total, carpeta):
    """revision.jpg: un cuadro del medio de cada toma (con el segundo) + la portada. Es lo que
    el agente MIRA antes de publicar: el QA numérico no ve un recorte que deja al DJ afuera."""
    marcas = [round((a + b) / 2, 2) for a, b in zip(cortes, cortes[1:] + [total])]
    fuente = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 26)
    cuadros = []
    with tempfile.TemporaryDirectory() as tmp:
        for t in marcas:
            out = pathlib.Path(tmp) / f"{t}.jpg"
            ff("-ss", t, "-i", mp4, "-frames:v", 1, "-vf", "scale=270:480", out)
            im = Image.open(out).convert("RGB")
            ImageDraw.Draw(im).text((8, 6), f"{t}s", fill="yellow", font=fuente, stroke_width=2, stroke_fill="black")
            cuadros.append(im)
    cuadros.append(Image.open(carpeta / "portada.jpg").convert("RGB").resize((270, 480)))
    cols = min(6, len(cuadros))
    filas = (len(cuadros) + cols - 1) // cols
    lienzo = Image.new("RGB", (270 * cols, 480 * filas))
    for i, im in enumerate(cuadros):
        lienzo.paste(im, ((i % cols) * 270, (i // cols) * 480))
    lienzo.save(carpeta / "revision.jpg", quality=75)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    armar(sys.argv[1])
