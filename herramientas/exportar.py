"""Exporta los manuales de GESPRO (docs/manual) a este sitio estático.

Uso: python herramientas/exportar.py [carpeta docs/manual de GESPRO]
"""
import re, shutil, pathlib, html, sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else r'C:\xampp\htdocs\gespro\docs\manual')
DST = pathlib.Path(__file__).resolve().parent.parent

ORDER = ['terreno', 'administracion-de-obra', 'jefe-administrativo', 'abastecimiento', 'bodega', 'control-de-gestion', 'gerencia']

COUNT = {5: 'Cinco', 6: 'Seis', 7: 'Siete', 8: 'Ocho', 9: 'Nueve', 10: 'Diez', 11: 'Once'}[len(ORDER)]

LOGO = ('<svg viewBox="0 0 20 20"><rect x="3" y="11" width="3.5" height="6" rx="0.6"/>'
        '<rect x="8.25" y="7" width="3.5" height="10" rx="0.6"/><rect x="13.5" y="3" width="3.5" height="14" rx="0.6"/></svg>')
FAVICON = ('data:image/svg+xml,' +
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect width='20' height='20' rx='4' fill='%232c50c4'/%3E"
           "%3Crect x='3' y='11' width='3.5' height='6' rx='0.6' fill='white'/%3E%3Crect x='8.25' y='7' width='3.5' height='10' rx='0.6' fill='white'/%3E"
           "%3Crect x='13.5' y='3' width='3.5' height='14' rx='0.6' fill='white'/%3E%3C/svg%3E")

# Lo mismo que el esqueleto con que el visor de artefactos envuelve la página.
RESET = (':root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}')

def page(head, body, description):
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{html.escape(description)}">\n'
            f'<link rel="icon" href="{FAVICON}">\n'
            f'<style>{RESET}</style>\n{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n')

if DST.exists():
    shutil.rmtree(DST / 'img', ignore_errors=True)
    for d in ORDER:
        shutil.rmtree(DST / d, ignore_errors=True)
DST.mkdir(exist_ok=True)

cards = []
names = []
for i, slug in enumerate(ORDER, 1):
    s = (SRC / slug / 'index.html').read_text(encoding='utf8')
    cut = s.index('</style>') + len('</style>')
    head, body = s[:cut], s[cut:]
    title = re.search(r'<title>(.*?)</title>', head).group(1)
    h1 = re.search(r'<h1>(.*?)</h1>', body).group(1)
    lede = re.sub(r'\s+', ' ', re.search(r'<p class="lede">(.*?)</p>', body, re.S).group(1))
    rol = re.search(r'<dt>Rol(?:es)? en GESPRO</dt><dd>(.*?)</dd>', body).group(1)
    screens = re.search(r'<dt>(?:Sus pantallas|Su pantalla principal)</dt><dd>(.*?)</dd>', body).group(1)
    names.append(h1.replace(' en GESPRO', '').removeprefix('Manual de ').removeprefix('Manual del '))
    first_img = re.search(r'src="(img/[^"]+)"', body).group(1)

    # Volver a la portada desde el índice de cada manual.
    head = head.replace('</style>', '.toc .back{display:inline-flex;gap:.35rem;margin-bottom:1rem;color:var(--brand);text-decoration:none;font-weight:600;font-size:.85rem}\n.toc a.back::before{content:none}\n.toc .back:hover{text-decoration:underline}\n</style>')
    body = body.replace('<nav class="toc" aria-label="Contenido del manual">',
                        '<nav class="toc" aria-label="Contenido del manual">\n        <a class="back" href="../">← Todos los manuales</a>', 1)
    (DST / slug).mkdir()
    (DST / slug / 'index.html').write_text(page(head, body, lede), encoding='utf8', newline='\n')
    shutil.copytree(SRC / slug / 'img', DST / slug / 'img')

    cards.append(f'''        <li>
            <a class="card" href="{slug}/">
                <span class="thumb"><img src="{slug}/{first_img}" alt="" width="1440" height="900" loading="lazy"></span>
                <span class="meta">
                    <span class="num">{i:02d}</span>
                    <span class="rol">{rol}</span>
                </span>
                <span class="name">{h1.replace(' en GESPRO', '')}</span>
                <span class="lede">{lede}</span>
                <span class="screens">{screens}</span>
            </a>
        </li>''')

portada_head = '''<title>Manuales de GESPRO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
    --bg: #f2f4f8; --surface: #ffffff; --line: #dde1e8; --ink: #131821; --ink-muted: #525d6d;
    --brand: #2c50c4; --accent-soft: #e7ecfb; --mark: #e8590c; --shadow: rgb(14 24 44 / 0.10);
    --font-body: "Public Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
    --font-mono: "IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
    color-scheme: light;
}
@media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
        --bg: #0d1118; --surface: #151a23; --line: #2a3242; --ink: #e6eaf1; --ink-muted: #a6afbe;
        --brand: #8ea5ff; --accent-soft: #1d2747; --mark: #ff8a4c; --shadow: rgb(0 0 0 / 0.4);
        color-scheme: dark;
    }
}
:root[data-theme="dark"] {
    --bg: #0d1118; --surface: #151a23; --line: #2a3242; --ink: #e6eaf1; --ink-muted: #a6afbe;
    --brand: #8ea5ff; --accent-soft: #1d2747; --mark: #ff8a4c; --shadow: rgb(0 0 0 / 0.4);
    color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 400 1rem/1.6 var(--font-body); padding-inline: 16px; padding-block: 0 4rem; }
.wrap { max-width: 76rem; margin-inline: auto; }
.top { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 1.75rem; }
.brand { display: flex; align-items: center; gap: 0.6rem; font-weight: 700; letter-spacing: 0.02em; }
.logo { width: 2rem; height: 2rem; border-radius: 0.5rem; background: var(--brand); display: grid; place-items: center; }
.logo svg { width: 1.1rem; height: 1.1rem; }
.logo rect { fill: var(--surface); }
.demo { color: var(--brand); font-weight: 600; text-decoration: none; font-size: 0.92rem; }
.demo:hover { text-decoration: underline; }
header.hero { max-width: 44rem; padding-block: 2rem 2.5rem; }
.eyebrow { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--brand); margin: 0; }
h1 { font-size: clamp(2rem, 4.5vw, 2.9rem); line-height: 1.12; font-weight: 700; margin: 0.4rem 0 0.9rem; text-wrap: balance; letter-spacing: -0.01em; }
.intro { font-size: 1.12rem; color: var(--ink-muted); margin: 0; }
ol.grid { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 21rem), 1fr)); }
.card {
    height: 100%; display: flex; flex-direction: column; gap: 0.5rem; padding: 0.75rem 0.75rem 1.25rem;
    background: var(--surface); border: 1px solid var(--line); border-radius: 0.8rem; color: inherit; text-decoration: none;
    transition: border-color .15s, box-shadow .15s, transform .15s;
}
.card:hover, .card:focus-visible { border-color: var(--brand); box-shadow: 0 10px 30px -14px var(--shadow); transform: translateY(-2px); outline: none; }
.thumb { display: block; aspect-ratio: 16 / 9; max-width: 100%; overflow: hidden; border-radius: 0.5rem; border: 1px solid var(--line); background: var(--bg); margin-bottom: 0.5rem; }
.thumb img { width: 100%; height: 100%; object-fit: cover; object-position: top left; display: block; }
.meta, .name, .lede, .screens { padding-inline: 0.5rem; }
.meta { display: flex; align-items: baseline; gap: 0.6rem; }
.num { font-family: var(--font-mono); font-size: 0.8rem; color: var(--mark); font-weight: 500; }
.rol { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-muted); }
.name { font-size: 1.3rem; font-weight: 700; line-height: 1.25; }
.card .lede { color: var(--ink-muted); font-size: 0.95rem; flex: 1; }
.screens { font-size: 0.8rem; color: var(--ink-muted); border-top: 1px solid var(--line); padding-top: 0.75rem; margin-inline: 0.5rem; padding-inline: 0; }
footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--line); color: var(--ink-muted); font-size: 0.88rem; }
footer p { margin: 0; max-width: 44rem; }
</style>'''

portada_body = f'''<div class="wrap">
    <div class="top">
        <div class="brand"><span class="logo" aria-hidden="true">{LOGO}</span>GESPRO</div>
        <a class="demo" href="https://gespro.enterweb.cl/">Entrar a la demostración →</a>
    </div>
    <header class="hero">
        <p class="eyebrow">Manuales de usuario</p>
        <h1>Cada rol de la obra, paso a paso</h1>
        <p class="intro">{COUNT} manuales con las pantallas reales de GESPRO: desde quien mide en terreno hasta la gerencia que cierra el mes. Los ejemplos usan los datos de demostración: el holding Altamira y su obra 1201 Edificio Mirador del Lago.</p>
    </header>
    <ol class="grid">
{chr(10).join(cards)}
    </ol>
    <footer>
        <p>Las capturas salen de la demostración en línea, con datos ficticios. Lo que muestra cada manual se puede recorrer en <a class="demo" href="https://gespro.enterweb.cl/">gespro.enterweb.cl</a>.</p>
    </footer>
</div>'''

(DST / 'index.html').write_text(
    page(portada_head, portada_body, 'Manuales de usuario de GESPRO por rol: ' + ', '.join(n.lower() for n in names[:-1]) + ' y ' + names[-1].lower() + '.'),
    encoding='utf8', newline='\n')
print('ok')
