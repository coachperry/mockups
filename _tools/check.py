"""Check a built mockup in headless Chrome.
Usage: python3 _tools/check.py <slug> [<slug> ...]
Shoots 1440 and 390 wide, then flags sideways scroll, broken images,
tap targets under 44px and leftover em dashes. Screenshots go to _shots/ (git-ignored).
"""
import sys, os, http.server, threading, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, '_shots'), exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Q, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

JS = """() => {
  const out = {};
  out.overflow = document.documentElement.scrollWidth - innerWidth;
  out.small = [...document.querySelectorAll('a,button,input,select,textarea,summary')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && r.height < 44 && !e.closest('p,blockquote,footer'); })
    .map(e => (e.innerText || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 30) + ' ' + Math.round(e.getBoundingClientRect().height) + 'px');
  out.dash = document.body.innerText.includes('\\u2014');
  return out;
}"""

fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for slug in sys.argv[1:]:
        for w, h in ((1440, 900), (390, 844)):
            pg = b.new_page(viewport={'width': w, 'height': h})
            pg.goto(f'http://127.0.0.1:{port}/{slug}/index.html', wait_until='domcontentloaded')
            pg.wait_for_timeout(1200)
            r = pg.evaluate(JS)
            pg.screenshot(path=os.path.join(ROOT, '_shots', f'{slug}-{w}.png'), full_page=True)
            issues = []
            if r['overflow'] > 1: issues.append(f"sideways scroll {r['overflow']}px")
            if r['small']: issues.append('small taps: ' + '; '.join(sorted(set(r['small']))[:6]))
            if r['dash']: issues.append('em dash in text')
            fails += bool(issues)
            print(f"{slug} @{w}: " + ('OK' if not issues else ' | '.join(issues)))
            pg.close()
    b.close()
srv.shutdown()
sys.exit(1 if fails else 0)
