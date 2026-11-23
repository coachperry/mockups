"""Build a mockup page from a JSON config. Usage: python3 build.py config.json out/index.html"""
import json, sys, html as H

c = json.load(open(sys.argv[1]))
esc = H.escape
P = lambda u, w=1600: u.split('=')[0] + f'=w{w}' if 'googleusercontent' in u else u

name, town, phone = c['name'], c['town'], c['phone']
tel = '+1' + ''.join(ch for ch in phone if ch.isdigit())[-10:]
pal = c.get('palette', {'ink': '#14213d', 'accent': '#e07a1f', 'paper': '#f6f4ef'})
photos = c['photos']
svc = c['services']
reviews = c['reviews']
faqs = c['faqs']
trust = c.get('trust', [])

schema = {
    "@context": "https://schema.org", "@type": c.get('schema_type', 'LocalBusiness'),
    "name": name, "telephone": tel,
    "address": {"@type": "PostalAddress", "streetAddress": c.get('street', ''), "addressLocality": town, "addressRegion": "NJ", "addressCountry": "US"},
    "areaServed": c.get('areas', [town + ' NJ']),
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": c['rating'], "reviewCount": c['review_count']},
    "image": [P(p['url'], 1200) for p in photos[:3]],
}

tabs = ''.join(f'<button type="button" class="tab" data-i="{i}">{esc(s["name"])}</button>' for i, s in enumerate(svc))
cards = ''.join(f'<button type="button" class="gcard" data-i="{i}" aria-label="Open photo: {esc(p["cap"])}"><img loading="lazy" src="{P(p["url"], 900)}" alt="{esc(p["cap"])} by {esc(name)}, {esc(town)} NJ"><span class="gcap">{esc(p["cap"])}</span></button>' for i, p in enumerate(photos))
faq_html = ''.join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(faqs))
trust_html = ''.join(f'<div><b>{esc(a)}</b>{esc(b)}</div>' for a, b in trust)
opts = ''.join(f'<option>{esc(s["name"])}</option>' for s in svc)
hero = P(c.get('hero', photos[0]['url']), 1920)
stars = '&#9733;' * 5

S = [[s['name'], P(photos[s['photo']]['url'], 1200), s['text']] for s in svc]
G = [P(p['url'], 1920) for p in photos]
R = [[r['who'], r['text']] for r in reviews]

page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c['title'])}</title>
<meta name="description" content="{esc(c['meta'])}">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={c.get('font', 'Archivo:wght@600;800')}&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(schema)}</script>
<style>
:root{{--ink:{pal['ink']};--ac:{pal['accent']};--paper:{pal['paper']};--line:#e3e0d8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.55}}
h1,h2,h3,.logo{{font-family:'{c.get('font', 'Archivo').split(':')[0].replace('+', ' ')}',Georgia,serif;line-height:1.05}}
a{{color:inherit}}.wrap{{max-width:1120px;margin:0 auto;padding:0 20px}}
.bar{{background:var(--ink);color:#fff;font-size:14px}}.bar .wrap{{display:flex;justify-content:space-between;gap:12px;padding:9px 20px;flex-wrap:wrap}}
.bar a{{font-weight:600;text-decoration:none;color:#fff}}
nav{{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;align-items:center;justify-content:space-between;height:64px;gap:12px}}
.logo{{font-weight:800;font-size:20px;text-decoration:none}}.logo span{{color:var(--ac)}}
.links{{display:flex;gap:22px;align-items:center}}.links a{{text-decoration:none;font-weight:500;font-size:15px}}
.btn{{display:inline-block;background:var(--ac);color:#fff!important;padding:12px 20px;border-radius:999px;font-weight:600;text-decoration:none;border:0;cursor:pointer;font-size:15px}}
.btn.ghost{{background:transparent;border:2px solid #fff}}
@media(max-width:760px){{.links a:not(.btn){{display:none}}}}
.hero{{position:relative;color:#fff;min-height:600px;display:flex;align-items:flex-end;background:#222 url({hero}) center/cover}}
.hero:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15),rgba(0,0,0,.8))}}
.hero .wrap{{position:relative;padding-bottom:60px}}
.stars{{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.16);padding:7px 14px;border-radius:999px;font-weight:600;font-size:14px;margin-bottom:18px}}
.stars b{{color:#ffc94d;letter-spacing:2px}}
.hero h1{{font-size:clamp(40px,7vw,74px);max-width:820px}}
.hero p{{font-size:19px;max-width:580px;margin:16px 0 26px;opacity:.94}}
.cta{{display:flex;gap:12px;flex-wrap:wrap}}
.trust{{background:var(--paper);border-bottom:1px solid var(--line)}}
.trust .wrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:22px 20px;text-align:center;font-weight:600;font-size:15px}}
.trust b{{display:block;font-size:24px;color:var(--ac)}}
@media(max-width:700px){{.trust .wrap{{grid-template-columns:repeat(2,1fr)}}}}
section{{padding:80px 0}}
.kicker{{color:var(--ac);font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:13px;margin-bottom:10px}}
h2{{font-size:clamp(30px,4.5vw,46px);margin-bottom:14px}}
.lead{{font-size:18px;opacity:.8;max-width:640px}}
.tabs{{display:flex;gap:8px;flex-wrap:wrap;margin:26px 0 22px}}
.tab{{border:2px solid var(--ink);background:#fff;padding:10px 16px;border-radius:999px;font-weight:600;cursor:pointer;font-size:15px;color:var(--ink)}}
.tab.on{{background:var(--ink);color:#fff}}
.svc{{display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:center;background:var(--paper);border:2px solid var(--line);border-radius:18px;overflow:hidden}}
.svc img{{width:100%;height:360px;object-fit:cover;display:block}}.svc div{{padding:28px}}
.svc h3{{font-size:30px;margin-bottom:10px}}.svc p{{opacity:.8;font-size:17px;margin-bottom:18px}}
@media(max-width:760px){{.svc{{grid-template-columns:1fr}}.svc img{{height:240px}}}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px}}
.gcard{{position:relative;border:2px solid var(--ink);border-radius:14px;overflow:hidden;cursor:pointer;padding:0;background:#111;aspect-ratio:4/3}}
.gcard img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}}.gcard:hover img{{transform:scale(1.05)}}
.gcap{{position:absolute;left:0;right:0;bottom:0;padding:26px 12px 10px;background:linear-gradient(transparent,rgba(0,0,0,.75));color:#fff;font-size:14px;font-weight:600;text-align:left}}
@media(max-width:760px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
.lb{{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:50;padding:20px}}
.lb.on{{display:flex}}.lb img{{max-width:100%;max-height:86vh;border-radius:10px}}
.lb button{{position:absolute;background:#fff;border:0;width:46px;height:46px;border-radius:50%;font-size:22px;cursor:pointer}}
.lb .x{{top:18px;right:18px}}.lb .p{{left:18px}}.lb .n{{right:18px}}
.rev{{background:var(--ink);color:#fff}}
.rbox{{margin-top:28px;border:2px solid var(--ac);border-radius:18px;padding:34px;min-height:200px;background:rgba(255,255,255,.04)}}
.rbox q{{display:block;font-size:clamp(19px,2.4vw,24px);line-height:1.45;quotes:none}}
.rbox .who{{margin-top:18px;font-weight:700;color:var(--ac)}}
.dots{{display:flex;gap:8px;margin-top:18px}}.dots button{{width:11px;height:11px;border-radius:50%;border:0;background:rgba(255,255,255,.3);cursor:pointer}}.dots .on{{background:var(--ac)}}
details{{border:2px solid var(--line);border-radius:14px;padding:18px 20px;margin-top:12px;background:#fff}}
summary{{font-weight:700;font-size:17px;cursor:pointer}}details p{{margin-top:10px;opacity:.8}}
.quote{{background:var(--paper)}}.qgrid{{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:start}}
form{{background:#fff;border:2px solid var(--ink);border-radius:18px;padding:26px;display:grid;gap:12px}}
input,select,textarea{{width:100%;padding:13px 14px;border:2px solid var(--line);border-radius:10px;font:inherit}}
.ok{{display:none;background:#e3f5e9;border:2px solid #3aa35b;padding:14px;border-radius:10px;font-weight:600}}
.call{{font-size:34px;font-weight:800;color:var(--ac);text-decoration:none;display:block;margin:16px 0 6px}}
@media(max-width:760px){{.qgrid{{grid-template-columns:1fr}}}}
footer{{background:var(--ink);color:rgba(255,255,255,.75);padding:34px 0;font-size:14px}}
footer .wrap{{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}}
.fab{{position:fixed;right:16px;bottom:16px;z-index:30;box-shadow:0 8px 24px rgba(0,0,0,.25)}}
</style></head><body>
<div class="bar"><div class="wrap"><span>{esc(c['bar'])}</span><a href="tel:{tel}">Call {esc(phone)}</a></div></div>
<nav><div class="wrap"><a class="logo" href="#top">{c['logo']}</a>
<div class="links"><a href="#services">Services</a><a href="#work">Work</a><a href="#reviews">Reviews</a><a class="btn" href="#quote">{esc(c.get('cta', 'Free quote'))}</a></div></div></nav>
<header class="hero" id="top"><div class="wrap">
<div class="stars"><b>{stars}</b> {esc(c['rating'])} on Google, {esc(c['review_count'])} reviews</div>
<h1>{esc(c['h1'])}</h1><p>{esc(c['sub'])}</p>
<div class="cta"><a class="btn" href="#quote">{esc(c.get('cta', 'Get a free quote'))}</a><a class="btn ghost" href="tel:{tel}">{esc(phone)}</a></div>
</div></header>
<div class="trust"><div class="wrap">{trust_html}</div></div>
<section id="services"><div class="wrap"><div class="kicker">Services</div><h2>{esc(c['svc_h2'])}</h2>
<div class="tabs">{tabs}</div><div class="svc"><img id="simg" alt=""><div><h3 id="sh"></h3><p id="sp"></p><a class="btn" href="#quote">{esc(c.get('cta', 'Get a quote'))}</a></div></div></div></section>
<section id="work" style="padding-top:0"><div class="wrap"><div class="kicker">Recent work</div><h2>{esc(c['work_h2'])}</h2><p class="lead">Tap any photo to see it full size.</p><div class="grid">{cards}</div></div></section>
<section class="rev" id="reviews"><div class="wrap"><div class="kicker">Google reviews</div><h2>{esc(c['rating'])} stars on Google</h2>
<div class="rbox"><q id="rq"></q><div class="who" id="rw"></div></div><div class="dots" id="dots"></div></div></section>
<section><div class="wrap" style="max-width:820px"><div class="kicker">FAQ</div><h2>Common questions</h2>{faq_html}</div></section>
<section class="quote" id="quote"><div class="wrap qgrid">
<div><div class="kicker">{esc(c.get('cta', 'Free quote'))}</div><h2>{esc(c['quote_h2'])}</h2><p class="lead">{esc(c['quote_p'])}</p>
<a class="call" href="tel:{tel}">{esc(phone)}</a><p>{esc(c.get('address', town + ', NJ'))}</p></div>
<form id="qf"><input required placeholder="Name"><input required type="tel" placeholder="Phone"><input placeholder="Town"><select><option>What do you need?</option>{opts}</select><textarea rows="3" placeholder="Anything else we should know?"></textarea><button class="btn" type="submit">Send request</button><div class="ok" id="ok">Got it. We will reach out soon.</div></form>
</div></section>
<footer><div class="wrap"><span>&copy; {esc(name)}, {esc(town)}, NJ</span><span>{esc(c['footer'])}</span></div></footer>
<a class="btn fab" href="tel:{tel}">Call now</a>
<div class="lb" id="lb"><button class="x" aria-label="Close">&times;</button><button class="p" aria-label="Previous">&#8249;</button><img id="lbi" alt=""><button class="n" aria-label="Next">&#8250;</button></div>
<script>
const S={json.dumps(S)},G={json.dumps(G)},R={json.dumps(R)};
const tabs=[...document.querySelectorAll('.tab')];
function svc(i){{tabs.forEach((t,j)=>t.classList.toggle('on',i==j));simg.src=S[i][1];simg.alt=S[i][0];sh.textContent=S[i][0];sp.textContent=S[i][2];}}
tabs.forEach(t=>t.onclick=()=>svc(+t.dataset.i));svc(0);
let li=0;const L=document.getElementById('lb');function lb(i){{li=(i+G.length)%G.length;lbi.src=G[li];L.classList.add('on')}}
document.querySelectorAll('.gcard').forEach(c=>c.onclick=()=>lb(+c.dataset.i));
L.querySelector('.x').onclick=()=>L.classList.remove('on');L.querySelector('.p').onclick=()=>lb(li-1);L.querySelector('.n').onclick=()=>lb(li+1);
L.onclick=e=>{{if(e.target===L)L.classList.remove('on')}};
let ri=0,t;const dots=document.getElementById('dots');
R.forEach((_,i)=>{{const b=document.createElement('button');b.setAttribute('aria-label','Review '+(i+1));b.onclick=()=>{{rv(i);clearInterval(t)}};dots.appendChild(b)}});
function rv(i){{ri=i;rq.textContent='\\u201c'+R[i][1]+'\\u201d';rw.textContent=R[i][0]+'  \\u2605\\u2605\\u2605\\u2605\\u2605';[...dots.children].forEach((d,j)=>d.classList.toggle('on',i==j))}}
rv(0);if(R.length>1)t=setInterval(()=>rv((ri+1)%R.length),6000);
qf.onsubmit=e=>{{e.preventDefault();ok.style.display='block'}};
</script></body></html>"""
assert '—' not in page, 'em dash found'
import os; os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True)
open(sys.argv[2], 'w').write(page)
print(sys.argv[2], len(page) // 1024, 'KB')
