import re, os, html
from urllib.parse import urljoin
from content import ROUTES
S = "site"
import base64
css = open(f"{S}/assets/styles.css").read()
for f in ("ArchivoExpanded-Variable.woff2","Archivo-Variable.woff2","Archivo-Italic-Variable.woff2"):
    css = css.replace(f'url("fonts/{f}")', 'url(data:font/woff2;base64,' + base64.b64encode(open(f"{S}/assets/fonts/{f}","rb").read()).decode() + ')')
css += """
.site-header{top:env(safe-area-inset-top,0px)}
:root{padding-bottom:env(safe-area-inset-bottom,0px)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--surface)}
.pv-page[hidden]{display:none}
.pv-toast{position:fixed;left:50%;bottom:1.5rem;transform:translateX(-50%);background:#000;color:#fff;font:500 15px Archivo,Arial,sans-serif;box-shadow:inset 0 0 0 1px #333;padding:.8rem 1.2rem;border-radius:4px;z-index:60;max-width:90vw}
"""
BASE = "http://x/"
pages = []
for key in ROUTES:
    for lang in ("es", "en"):
        route = ROUTES[key][lang]
        doc = open(f"{S}/{route}index.html", encoding="utf-8").read()
        title = re.search(r"<title>(.*?)</title>", doc).group(1)
        body = re.search(r"<body>(.*)</body>", doc, re.S).group(1)
        body = re.sub(r'<script src=.*?</script>', "", body)
        body = re.sub(r'<a class="skip".*?</a>', '', body)
        body = body.replace('id="main"', "").replace('id="site-nav"', "").replace('aria-controls="site-nav"', "")
        def fix(m):
            href = html.unescape(m.group(1))
            if href.startswith(("mailto:", "http", "#")):
                return m.group(0)
            r = urljoin(BASE + route, href)[len(BASE):]
            path, _, frag = r.partition("#")
            q = "?" + frag.replace("area-", "area=") if frag.startswith("area-") else ""
            return f'href="#/{path}{q}"'
        body = re.sub(r'href="([^"]*)"', fix, body)
        pages.append(f'<div class="pv-page" data-route="{route}" data-lang="{lang}" data-title="{title}" hidden>{body}</div>')

js = r"""
(function(){
 var pages=[].slice.call(document.querySelectorAll('.pv-page'));
 function filter(page,area){
  var chips=page.querySelectorAll('.catalog-filter .tag'); if(!chips.length) return;
  var panel=page.querySelector('.catalog-panel'), hint=page.querySelector('.catalog-hint');
  var items=page.querySelectorAll('.catalog li'), count=page.querySelector('.catalog-count'), n=0;
  page._area=area;
  chips.forEach(function(c){var on=c.dataset.area===area; c.setAttribute('aria-pressed',on?'true':'false'); c.setAttribute('aria-expanded',on?'true':'false');});
  if(!area){ panel.classList.remove('open'); if(hint) hint.hidden=false; return; }
  items.forEach(function(li){var on=area==='all'||li.dataset.area===area; li.hidden=!on; if(on)n++;});
  if(count) count.textContent=count.dataset.template.replace('{n}',n);
  if(hint) hint.hidden=true; panel.classList.add('open');
 }
 function go(){
  var h=location.hash.replace(/^#\/?/,''), area=null, m=h.match(/\?area=([a-z]+)$/);
  if(m){area=m[1]; h=h.replace(m[0],'');}
  var page=pages.filter(function(p){return p.dataset.route===h})[0]||pages[0];
  pages.forEach(function(p){p.hidden=p!==page});
  document.documentElement.lang=page.dataset.lang; document.title=page.dataset.title;
  var nav=page.querySelector('.nav'); if(nav) nav.classList.remove('open');
  filter(page, area && page.querySelector('.catalog-filter .tag[data-area="'+area+'"]') ? area : null);
  var cat=page.querySelector('#catalog');
  if(area&&cat) cat.scrollIntoView(); else window.scrollTo(0,0);
 }
 document.addEventListener('click',function(e){
  var b=e.target.closest('.menu-btn');
  if(b){var nav=b.parentNode.querySelector('.nav'); var o=nav.classList.toggle('open'); b.setAttribute('aria-expanded',o);return;}
  var c=e.target.closest('.catalog-filter .tag');
  if(c){var pg=c.closest('.pv-page'); filter(pg, pg._area===c.dataset.area?null:c.dataset.area); return;}
  var pv=e.target.closest('.pv-page');
  if(pv&&pv._area&&!e.target.closest('.catalog-filter')&&!e.target.closest('.catalog-panel')){filter(pv,null);}
  var x=e.target.closest('.catalog-close');
  if(x){var p2=x.closest('.pv-page'), was=p2._area; filter(p2,null); var b2=was&&p2.querySelector('.catalog-filter .tag[data-area="'+was+'"]'); if(b2) b2.focus();}
 });
 document.addEventListener('submit',function(e){
  e.preventDefault();
  var t=document.createElement('div'); t.className='pv-toast';
  t.textContent=document.documentElement.lang==='es'?'Vista previa: el formulario enviará los mensajes cuando configure Formspree.':'Preview: the form will send messages once Formspree is configured.';
  document.body.appendChild(t); setTimeout(function(){t.remove()},4000);
 });
 document.addEventListener('keydown',function(e){ if(e.key==='Escape'){var p=pages.filter(function(x){return !x.hidden})[0]; if(p&&p._area) filter(p,null);} });
 window.addEventListener('hashchange',go); go();
})();
"""
ICON = base64.b64encode(open("brand/app-icon.svg","rb").read()).decode()
out = f"""<!doctype html>
<html lang="es" class="js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>NextMind Learning</title>
<link rel="icon" href="data:image/svg+xml;base64,{ICON}">
<style>{css}</style></head><body>
{''.join(pages)}
<script>{js}</script></body></html>"""
os.makedirs("/mnt/user-data/outputs", exist_ok=True)
open("/mnt/user-data/outputs/nextmind-preview.html", "w", encoding="utf-8").write(out)
print(len(out)//1024, "KB")
