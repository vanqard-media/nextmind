# -*- coding: utf-8 -*-
"""Builds the NextMind Learning static site into ./site  (python3 build.py)"""
import json, os, re, shutil, datetime
from html import escape as e
from legal_texts import LEGAL, PRIVACY, UPDATED
from content import (MEDIA, MEDIA_SOURCES, HERO_VIDEO_SOURCE, CONFIG, ROUTES, NAV, UI, FORMATS, PROCESS, AUDIENCE, OUTCOMES,
                     FAQ_HOME, FAQ_COURSES_EXTRA, AREAS, TOPICS, FREQUENT_THEMES)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
SITE = CONFIG["site_url"].rstrip("/")
BRAND = CONFIG["brand"]
TODAY = datetime.date.today().isoformat()
ORG_ID = SITE + "/#organization"

def _logo():
    svg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand", "logo-black.svg"), encoding="utf-8").read()
    svg = svg.replace("#000000", "currentColor")
    svg = re.sub(r'<title>.*?</title>', '', svg)
    svg = re.sub(r' width="\d+" height="\d+" role="img" aria-label="[^"]*"', ' aria-hidden="true" focusable="false"', svg)
    return svg
LOGO_SVG = _logo()
MARK_SVG = re.sub(r'<title>.*?</title>', '', open(os.path.join(ROOT, "brand", "mark-black.svg"), encoding="utf-8").read()).replace(' role="img" aria-label="NextMind Learning"', ' aria-hidden="true"').replace('#000000', 'currentColor')


def url(key, lang):
    return SITE + "/" + ROUTES[key][lang]


def rel(from_key, from_lang, to_path):
    depth = ROUTES[from_key][from_lang].count("/")
    return "../" * depth + to_path


# ------------------------------------------------------------------ fragments
def faq_html(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>')
    out.append("</div>")
    return "".join(out)


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def rows(items):
    return '<ul class="rows">' + "".join(
        f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in items) + "</ul>"


def steps(lang):
    return '<ol class="steps">' + "".join(
        f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in PROCESS[lang]) + "</ol>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def cta_band(key, lang, title, text):
    return (f'<section class="cta-band on-black"><div class="wrap cta-inner"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>'
            f'<a class="btn btn-primary" href="{rel(key, lang, ROUTES["contact"][lang])}">{e(UI[lang]["cta"])}</a></div></section>')


def page_hero(key, lang, h1, lead, img=None):
    home = rel(key, lang, ROUTES["home"][lang]) or "./"
    pic = media(key, lang, img, eager=True) if img else ""
    return (f'<section class="page-hero"><div class="wrap{" page-hero-grid" if img else ""}"><div>'
            f'<nav class="crumbs" aria-label="breadcrumb"><a href="{home}">{e(UI[lang]["nav"]["home"])}</a> / {e(UI[lang]["nav"][key])}</nav>'
            f'<h1>{e(h1)}</h1><div class="stem"><div><p class="lead">{e(lead)}</p></div></div></div>{pic}</div></section>')


MEDIA_IN = os.path.join(ROOT, "media")
MEDIA_WIDTHS = (640, 1024, 1600, 2200)
_media_cache = {}


def _find(name, exts):
    for ext in exts:
        p = os.path.join(MEDIA_IN, name + ext)
        if os.path.exists(p):
            return p
    return None


def _variants(name):
    """Creates responsive WebP versions of media/<name>.* once; returns [(file, width)], (w, h)."""
    if name in _media_cache:
        return _media_cache[name]
    src = _find(name, (".jpg", ".jpeg", ".png", ".webp"))
    if not src:
        _media_cache[name] = None
        return None
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    out_dir = os.path.join(OUT, "assets", "media")
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for w in MEDIA_WIDTHS:
        if w > im.width and files:
            break
        ww = min(w, im.width)
        hh = round(im.height * ww / im.width)
        fn = f"{name}-{ww}.webp"
        im.resize((ww, hh), Image.LANCZOS).save(os.path.join(out_dir, fn), "WEBP", quality=78, method=6)
        files.append((fn, ww))
    _media_cache[name] = (files, (im.width, im.height))
    return _media_cache[name]


def media(key, lang, name, facet=False, wide=False, eager=False):
    ratio, alt_es, alt_en = MEDIA[name]
    alt = alt_es if lang == "es" else alt_en
    cls = "media" + (" facet" if facet else "") + (" media-wide" if wide else "")
    v = _variants(name)
    if not v and name in MEDIA_SOURCES:
        base = MEDIA_SOURCES[name][0]
        srcset = ", ".join(f"{base}?auto=format&fit=crop&q=70&w={w} {w}w" for w in MEDIA_WIDTHS)
        sizes = "100vw" if wide else "(max-width: 720px) 100vw, 50vw"
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return (f'<figure class="{cls}" style="aspect-ratio:{ratio}"><img src="{base}?auto=format&fit=crop&q=70&w=1600" '
                f'srcset="{srcset}" sizes="{sizes}" alt="{e(alt)}" {load} decoding="async"></figure>')
    if not v:
        mark = MARK_SVG
        return (f'<figure class="{cls} media-empty" style="aspect-ratio:{ratio}" aria-hidden="true" data-media="{name}">'
                f'<span class="media-mark">{mark}</span></figure>')
    files, (w, h) = v
    pre = rel(key, lang, "assets/media/")
    srcset = ", ".join(f"{pre}{fn} {ww}w" for fn, ww in files)
    sizes = "100vw" if wide else "(max-width: 720px) 100vw, 50vw"
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="{cls}" style="aspect-ratio:{ratio}"><img src="{pre}{files[-1][0]}" srcset="{srcset}" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"></figure>')


def optimize_video():
    """If media/hero-source.(mp4|mov|m4v|webm) exists, creates web-ready hero files with ffmpeg:
    hero.mp4 (H.264, 1920px, no audio, fast start), hero.webm (VP9), hero-mobile.mp4 (vertical 720x1280)
    and hero-poster.jpg (first second). Skips files that are already newer than the source."""
    src = _find("hero-source", (".mp4", ".mov", ".m4v", ".webm"))
    if not src:
        return
    if not shutil.which("ffmpeg"):
        if src.endswith(".mp4") and not os.path.exists(os.path.join(MEDIA_IN, "hero.mp4")):
            shutil.copy(src, os.path.join(MEDIA_IN, "hero.mp4"))  # unoptimized but works
        return
    import subprocess
    def stale(name):
        p = os.path.join(MEDIA_IN, name)
        return not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(src)
    trim = ["-t", "20"]  # backgrounds loop: 20 s max keeps files small
    jobs = [
        ("hero.mp4", ["-vf", "scale='min(1920,iw)':-2,fps=25", "-c:v", "libx264", "-preset", "slow", "-crf", "27",
                      "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]),
        ("hero.webm", ["-vf", "scale='min(1920,iw)':-2,fps=25", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "38",
                       "-row-mt", "1", "-deadline", "good", "-cpu-used", "4", "-an"]),
        ("hero-mobile.mp4", ["-vf", "crop='min(iw,ih*9/16)':ih,scale=720:1280,fps=25", "-c:v", "libx264", "-preset", "slow",
                             "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]),
    ]
    for name, args in jobs:
        if stale(name):
            print("  encoding", name)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src] + trim + args + [os.path.join(MEDIA_IN, name)], check=True)
    if not _find("hero-poster", (".jpg", ".jpeg", ".png", ".webp")) or stale("hero-poster.jpg"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", src, "-frames:v", "1", "-q:v", "3",
                        os.path.join(MEDIA_IN, "hero-poster.jpg")], check=True)


def hero_video(key, lang):
    """Full-screen background video: loaded by JS only when motion and data allow it."""
    mp4 = _find("hero", (".mp4",))
    poster_src = _find("hero-poster", (".jpg", ".jpeg", ".png", ".webp"))
    pre = rel(key, lang, "assets/media/")
    poster = ""
    if poster_src:
        from PIL import Image, ImageOps
        os.makedirs(os.path.join(OUT, "assets", "media"), exist_ok=True)
        im = ImageOps.exif_transpose(Image.open(poster_src)).convert("RGB")
        if im.width > 1920:
            im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, "assets", "media", "hero-poster.webp"), "WEBP", quality=72, method=6)
        poster = f"{pre}hero-poster.webp"
    if not mp4 and HERO_VIDEO_SOURCE.get("mp4"):
        data = {"mp4": HERO_VIDEO_SOURCE["mp4"]}
        poster = poster or HERO_VIDEO_SOURCE.get("poster", "")
        attrs = f'data-mp4="{data["mp4"]}"'
        label = {"es": ("Pausar vídeo", "Reproducir vídeo"), "en": ("Pause video", "Play video")}[lang]
        poster_attr = f' poster="{poster}"' if poster else ""
        bg = f' style="background-image:url({poster})"' if poster else ""
        return (f'<div class="hero-media"{bg} aria-hidden="true"><video class="hero-video" muted loop playsinline preload="none"{poster_attr} {attrs}></video></div>'
                f'<div class="hero-scrim" aria-hidden="true"></div>'
                f'<button class="hero-toggle" type="button" hidden data-pause="{label[0]}" data-play="{label[1]}" aria-label="{label[0]}">'
                f'<span aria-hidden="true">II</span></button>')
    if not mp4:
        style = f' style="background-image:url({poster})"' if poster else ""
        return f'<div class="hero-media"{style} aria-hidden="true"></div><div class="hero-scrim" aria-hidden="true"></div>'
    data = {"mp4": "hero.mp4"}
    for n, ext in (("webm", ".webm"), ("mobile", ".mp4")):
        f = _find("hero" + ("-mobile" if n == "mobile" else ""), (ext,))
        if f:
            data[n] = os.path.basename(f)
    for f in data.values():
        shutil.copy(os.path.join(MEDIA_IN, f), os.path.join(OUT, "assets", "media", f))
    attrs = " ".join(f'data-{n}="{pre}{f}"' for n, f in data.items())
    label = {"es": ("Pausar vídeo", "Reproducir vídeo"), "en": ("Pause video", "Play video")}[lang]
    poster_attr = f' poster="{poster}"' if poster else ""
    bg = f' style="background-image:url({poster})"' if poster else ""
    return (f'<div class="hero-media"{bg} aria-hidden="true"><video class="hero-video" muted loop playsinline preload="none"{poster_attr} {attrs}></video></div>'
            f'<div class="hero-scrim" aria-hidden="true"></div>'
            f'<button class="hero-toggle" type="button" hidden data-pause="{label[0]}" data-play="{label[1]}" aria-label="{label[0]}">'
            f'<span aria-hidden="true">II</span></button>')


def area_name(code, lang):
    for c, es, en in AREAS:
        if c == code:
            return es if lang == "es" else en


# ------------------------------------------------------------------ pages
def home(lang):
    k = "home"
    T = {
        "es": dict(
            title="Cursos de IA para empresas y directivos | NextMind Learning",
            desc="Formación ejecutiva a medida en IA, ciberseguridad, transformación digital y liderazgo para grandes empresas, con profesorado universitario de referencia.",
            h1="Cursos para empresas con profesorado de universidades de referencia mundial",
            lead="En NextMind Learning diseñamos programas de formación ejecutiva en inteligencia artificial, ciberseguridad, transformación digital, ingeniería y liderazgo para grandes empresas, junto a universidades de referencia mundial de Estados Unidos.",
            b1="Ver cursos para empresas", b2="Contáctanos", kicker="Formación ejecutiva para grandes empresas", panel="Qué enseñamos",
            board=["Inteligencia artificial", "IA agéntica", "Ciberseguridad", "Computación cuántica",
                   "Internet de las cosas", "Transformación digital", "Liderazgo e innovación", "Sostenibilidad y ESG"],
            intro_h="Formación diseñada a partir de su estrategia",
            intro=["La tecnología está cambiando todos los sectores, pero la transformación depende de las personas. Trabajamos con grandes organizaciones para formar a su comité de dirección, a sus mandos y a sus equipos técnicos con programas que parten de sus objetivos de negocio, no de un temario estándar.",
                   "Combinamos cursos online de universidades de primer nivel, sesiones en directo con su profesorado, talleres presenciales y programas desarrollados desde cero para su empresa."],
            fmt_h="Cinco formas de trabajar con nosotros", fmt_link="Ver formatos, temas y certificaciones", cons_link="Conocer la consultoría ejecutiva",
            areas_h="Áreas de formación", areas_p="Cada área reúne temas que combinamos en programas a medida. Seleccione una para ver el catálogo.",
            who_h="Para quién", who_p="Grandes empresas, multinacionales, administraciones públicas e instituciones que necesitan preparar a sus líderes y equipos para las tecnologías emergentes.",
            out_h="Qué consiguen las organizaciones",
            proc_h="Cómo trabajamos",
            faq_h="Preguntas frecuentes",
            beyond_h="Más allá de la empresa",
            p_h="Alianzas universitarias", p_p="Co-desarrollamos programas de formación ejecutiva y tecnológica con universidades e instituciones de educación superior.", p_a="Conocer las alianzas",
            c_h="Campamentos", c_p="Programas inmersivos de verano e invierno para estudiantes preuniversitarios a partir de 16 años.", c_a="Conocer los campamentos",
            cta_h="¿Hablamos de su próximo programa?", cta_p="Cuéntenos qué quiere conseguir y le propondremos un programa a la medida de su organización."),
        "en": dict(
            title="Corporate AI courses for executives | NextMind Learning",
            desc="Custom executive education in AI, cybersecurity, digital transformation and leadership for large companies, with faculty from world-leading universities.",
            h1="Corporate courses with faculty from world-leading universities",
            lead="NextMind Learning designs executive education programs in artificial intelligence, cybersecurity, digital transformation, engineering and leadership for large companies, together with world-leading universities in the United States.",
            b1="See corporate courses", b2="Contact us", kicker="Executive education for large companies", panel="What we teach",
            board=["Artificial intelligence", "Agentic AI", "Cybersecurity", "Quantum computing",
                   "Internet of Things", "Digital transformation", "Leadership and innovation", "Sustainability and ESG"],
            intro_h="Learning built around your strategy",
            intro=["Technology is reshaping every industry, but transformation depends on people. We work with large organizations to develop their executive committees, managers and technical teams through programs that start from their business objectives, not from a standard syllabus.",
                   "We combine online courses from top universities, live sessions with their faculty, in-person workshops and programs built from scratch for your company."],
            fmt_h="Five ways to work with us", fmt_link="See formats, topics and certificates", cons_link="About executive consulting",
            areas_h="Learning areas", areas_p="Each area brings together topics we combine into tailored programs. Choose one to open the catalog.",
            who_h="Who it's for", who_p="Large companies, multinationals, government bodies and institutions that need to prepare their leaders and teams for emerging technologies.",
            out_h="What organizations achieve",
            proc_h="How we work",
            faq_h="Frequently asked questions",
            beyond_h="Beyond the enterprise",
            p_h="University partnerships", p_p="We co-develop executive education and technology programs with universities and higher education institutions.", p_a="About our partnerships",
            c_h="Camps", c_p="Immersive summer and winter programs for pre-university students aged 16 and over.", c_a="About our camps",
            cta_h="Shall we talk about your next program?", cta_p="Tell us what you want to achieve and we will propose a program built for your organization."),
    }[lang]
    courses = rel(k, lang, ROUTES["courses"][lang])
    board = "".join(f"<li>{e(x)}</li>" for x in T["board"])
    areas = "".join(f'<li><a href="{courses}#area-{c}">{e(es if lang == "es" else en)}</a></li>' for c, es, en in AREAS)
    body = f"""
<section class="hero on-black">
  {hero_video(k, lang)}
  <div class="wrap hero-content">
    <p class="kicker">{e(T['kicker'])}</p>
    <h1>{e(T['h1'])}</h1>
    <div class="stem"><div><p class="lead">{e(T['lead'])}</p></div></div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{rel(k, lang, ROUTES['contact'][lang])}">{e(T['b2'])}</a>
      <a class="hero-link" href="{courses}">{e(T['b1'])}</a>
    </div>
  </div>
</section>

<section class="section"><div class="wrap split split-media">
  <div><h2>{e(T['intro_h'])}</h2>
  {''.join(f'<p class="lead">{e(p)}</p>' if i == 0 else f'<p>{e(p)}</p>' for i, p in enumerate(T['intro']))}</div>
  {media(k, lang, 'home-intro', facet=True)}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['fmt_h'])}</h2></div>
  {rows(FORMATS[lang])}
  <p style="margin-top:1.5rem"><a href="{courses}">{e(T['fmt_link'])}</a> &nbsp;·&nbsp; <a href="{rel(k, lang, ROUTES['consulting'][lang])}">{e(T['cons_link'])}</a></p>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="section-head"><h2>{e(T['areas_h'])}</h2><p>{e(T['areas_p'])}</p></div>
  <ul class="tags area-tags">{areas}</ul>
</div></section>

<section class="section"><div class="wrap split">
  <div><h2>{e(T['who_h'])}</h2><p>{e(T['who_p'])}</p>{ticks(AUDIENCE[lang])}</div>
  <div><h2>{e(T['out_h'])}</h2>{ticks(OUTCOMES[lang])}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['proc_h'])}</h2></div>
  {steps(lang)}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['faq_h'])}</h2></div>
  {faq_html(FAQ_HOME[lang])}
</div></section>

<section class="section section-alt"><div class="wrap">
  <h2 class="h-small">{e(T['beyond_h'])}</h2>
  <div class="beyond">
    <div>{media(k, lang, 'home-partnerships')}<h3>{e(T['p_h'])}</h3><p>{e(T['p_p'])}</p><a href="{rel(k, lang, ROUTES['partners'][lang])}">{e(T['p_a'])}</a></div>
    <div>{media(k, lang, 'home-camps')}<h3>{e(T['c_h'])}</h3><p>{e(T['c_p'])}</p><a href="{rel(k, lang, ROUTES['camps'][lang])}">{e(T['c_a'])}</a></div>
  </div>
</div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    ld = [faq_ld(FAQ_HOME[lang])]
    return T["title"], T["desc"], body, ld


def courses(lang):
    k = "courses"
    T = {
        "es": dict(
            title="Cursos de IA y tecnología para empresas | NextMind Learning",
            desc="Programas in company de IA, ciberseguridad, transformación digital y liderazgo para directivos y equipos. Online, presencial o en campus universitario.",
            h1="Cursos de IA y tecnología para empresas",
            lead="Formación ejecutiva y capacitación tecnológica para grandes empresas, sus comités de dirección, sus mandos y su talento de alto potencial, con profesorado de universidades de referencia mundial de Estados Unidos.",
            fmt_h="Formatos", fmt_p="Todos los formatos se pueden combinar entre sí.",
            del_h="Cómo y dónde se imparte",
            delivery=[("En remoto", "El profesorado imparte las sesiones en directo desde su universidad."),
                      ("En su país", "El profesorado viaja para impartir sesiones presenciales en sus instalaciones."),
                      ("En el campus", "Grupos seleccionados viven una inmersión en el campus de la universidad."),
                      ("Duración flexible", "Desde una sesión ejecutiva de dos horas hasta iniciativas de varios meses o años.")],
            lvl_h="Un programa para cada nivel",
            levels=[("Comité de dirección", "Grupos reducidos centrados en el criterio estratégico: dónde aplicar la IA y dónde no, cómo priorizar inversiones y cómo gobernar la innovación."),
                    ("Mandos y equipos técnicos", "Programas aplicados para grupos grandes, centrados en identificar, diseñar y desplegar casos de uso de forma responsable.")],
            lvl_p="Formar a ambos niveles a la vez alinea la estrategia con la ejecución: la dirección elige las iniciativas adecuadas y los equipos tienen la capacidad de construirlas.",
            themes_h="Temas frecuentes en programas a medida",
            mix_h="Tecnología y liderazgo en un mismo programa",
            mix_p="Un programa puede combinar contenido técnico de un instituto tecnológico líder con contenido de liderazgo de una universidad de referencia. Cuando hay certificación, cada institución certifica su parte.",
            cat_h="Catálogo de temas", cat_all="Todos", cat_count="{n} temas", cat_hint="Seleccione un área para ver sus temas.", cat_close="Cerrar",
            cat_note="Lista orientativa. Cada programa se diseña para su organización; pregúntenos por temas que no aparezcan aquí.",
            cert_h="Certificados",
            cert_p="Algunos programas incluyen un certificado expedido por la propia universidad, a través de su plataforma de formación profesional online, sujeto a sus requisitos: completar las evaluaciones o un proyecto final. Otros formatos, como las sesiones ejecutivas cortas, no son certificados. En cada propuesta indicamos qué certificación incluye el programa.",
            more_h="Más allá de la formación",
            more_p="Además de programas formativos, podemos conectar a su empresa con equipos universitarios para proyectos de consultoría y desarrollo tecnológico.",
            proc_h="Cómo trabajamos", faq_h="Preguntas frecuentes",
            cta_h="Diseñemos el programa de su empresa", cta_p="Cuéntenos su objetivo, su audiencia y sus plazos. Le responderemos con una propuesta."),
        "en": dict(
            title="AI and technology courses for companies | NextMind Learning",
            desc="Custom corporate programs in AI, cybersecurity, digital transformation and leadership for executives and teams. Online, on site or on campus.",
            h1="AI and technology courses for companies",
            lead="Executive education and technology upskilling for large companies, their executive committees, managers and high-potential talent, with faculty from world-leading US universities.",
            fmt_h="Formats", fmt_p="All formats can be mixed and matched.",
            del_h="How and where it is delivered",
            delivery=[("Remote", "Faculty teach live sessions from their university."),
                      ("In your country", "Faculty travel to deliver in-person sessions at your premises."),
                      ("On campus", "Selected cohorts take part in an immersion on the university campus."),
                      ("Flexible length", "From a two-hour executive session to initiatives lasting months or years.")],
            lvl_h="A program for every level",
            levels=[("Executive committee", "Small cohorts focused on strategic judgment: where AI should and should not be used, how to prioritize investment and how to govern innovation."),
                    ("Managers and technical teams", "Applied programs for large groups, focused on identifying, designing and deploying use cases responsibly.")],
            lvl_p="Training both levels together aligns strategy and execution: leadership chooses the right initiatives and teams have the capability to build them.",
            themes_h="Frequent themes in tailored programs",
            mix_h="Technology and leadership in one program",
            mix_p="A program can combine technical content from a leading institute of technology with leadership content from a world-leading university. Where certification applies, each institution certifies its own part.",
            cat_h="Topic catalog", cat_all="All", cat_count="{n} topics", cat_hint="Choose an area to see its topics.", cat_close="Close",
            cat_note="Indicative list. Every program is designed for your organization; ask us about topics not listed here.",
            cert_h="Certificates",
            cert_p="Selected programs include a certificate issued by the university itself, through its online professional learning platform, subject to its requirements: completing the assessments or a capstone project. Other formats, such as short executive sessions, are not certified. Every proposal states which certification the program includes.",
            more_h="Beyond training",
            more_p="Beyond learning programs, we can connect your company with university teams for consulting and technology development projects.",
            proc_h="How we work", faq_h="Frequently asked questions",
            cta_h="Let's design your company's program", cta_p="Tell us your goal, your audience and your timeline. We will reply with a proposal."),
    }[lang]

    chips = f'<button class="tag" type="button" data-area="all" aria-pressed="false" aria-controls="catalog-panel">{e(T["cat_all"])}</button>' + "".join(
        f'<button class="tag" type="button" data-area="{c}" aria-pressed="false" aria-controls="catalog-panel">{e(es if lang == "es" else en)}</button>'
        for c, es, en in AREAS)
    items = []
    for a, tes, ses, ten, sen in TOPICS:
        t, s = (tes, ses) if lang == "es" else (ten, sen)
        items.append(f'<li data-area="{a}"><span class="area">{e(area_name(a, lang))}</span><h3>{e(t)}</h3><p>{e(s)}</p></li>')
    faqs = FAQ_HOME[lang][:5] + FAQ_COURSES_EXTRA[lang]
    blocks = lambda xs: '<div class="blocks">' + "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in xs) + "</div>"

    body = f"""
{page_hero(k, lang, T['h1'], T['lead'], 'courses-hero')}

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['fmt_h'])}</h2><p>{e(T['fmt_p'])}</p></div>
  {rows(FORMATS[lang])}
  <p style="margin-top:1.5rem"><a href="{rel(k, lang, ROUTES['consulting'][lang])}">{e(UI[lang]['nav']['consulting'])}</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['del_h'])}</h2></div>
  {media(k, lang, 'courses-delivery', wide=True)}
  {blocks(T['delivery'])}
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="section-head"><h2>{e(T['lvl_h'])}</h2></div>
  {blocks(T['levels'])}
  <p style="margin-top:2rem">{e(T['lvl_p'])}</p>
</div></section>

<section class="section"><div class="wrap split">
  <div><h2>{e(T['themes_h'])}</h2>{ticks(FREQUENT_THEMES[lang])}</div>
  <div><h2>{e(T['mix_h'])}</h2><p>{e(T['mix_p'])}</p>
       <h2 style="margin-top:2.5rem">{e(T['cert_h'])}</h2><p>{e(T['cert_p'])}</p></div>
</div></section>

<section class="section" id="catalog"><div class="wrap">
  <div class="section-head"><h2>{e(T['cat_h'])}</h2></div>
  <div class="catalog-filter tags" role="group" aria-label="{e(T['cat_h'])}">{chips}</div>
  <p class="catalog-hint">{e(T['cat_hint'])}</p>
  <div class="catalog-panel" id="catalog-panel">
    <div class="catalog-bar"><p class="catalog-count" aria-live="polite" data-template="{e(T['cat_count'])}">{e(T['cat_count'].replace('{n}', str(len(TOPICS))))}</p>
      <button class="btn btn-secondary catalog-close" type="button">{e(T['cat_close'])} <span aria-hidden="true">&times;</span></button></div>
    <ul class="catalog">{''.join(items)}</ul>
    <p class="note">{e(T['cat_note'])}</p>
  </div>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="section-head"><h2>{e(T['proc_h'])}</h2></div>
  {steps(lang)}
</div></section>

<section class="section"><div class="wrap split">
  <h2>{e(T['more_h'])}</h2><p class="lead">{e(T['more_p'])}</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(T['faq_h'])}</h2></div>
  {faq_html(faqs)}
</div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    service = {
        "@type": "Service", "@id": url(k, lang) + "#service",
        "name": T["h1"], "description": T["desc"],
        "serviceType": "Corporate training and executive education" if lang == "en" else "Formación corporativa y formación ejecutiva",
        "provider": {"@id": ORG_ID},
        "areaServed": [{"@type": "Country", "name": "Spain"}, {"@type": "Place", "name": "Latin America"}],
        "audience": {"@type": "BusinessAudience", "audienceType": "Large companies, multinationals and public institutions"},
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": T["cat_h"],
            "itemListElement": [{"@type": "Offer", "itemOffered": {
                "@type": "Course", "name": (tes if lang == "es" else ten),
                "description": (ses if lang == "es" else sen), "provider": {"@id": ORG_ID},
                "inLanguage": lang}} for a, tes, ses, ten, sen in TOPICS]},
    }
    return T["title"], T["desc"], body, [service, faq_ld(faqs)]


def consulting(lang):
    k = "consulting"
    T = {
        "es": dict(
            title="Consultoría ejecutiva en formación e IA | NextMind Learning",
            desc="Consultoría para la dirección: estrategia de aprendizaje, diagnóstico de capacidades en IA y tecnología, y proyectos con equipos universitarios de referencia.",
            h1="Consultoría ejecutiva",
            lead="Acompañamos a la dirección a convertir la estrategia de negocio en capacidades: qué debe aprender cada nivel de la organización, cómo hacerlo y con quién.",
            what_h="Qué hacemos",
            what=[("Estrategia de aprendizaje", "Definimos con la dirección las prioridades de formación y las alineamos con los objetivos de transformación del negocio."),
                  ("Diagnóstico de capacidades", "Identificamos qué necesita aprender cada nivel de la organización en IA y tecnología, conectando la visión de la dirección con las necesidades reales de los equipos técnicos."),
                  ("Desarrollo de capacidades a largo plazo", "Diseñamos itinerarios y academias corporativas que pueden ampliarse a otros departamentos, filiales y países."),
                  ("Proyectos con equipos universitarios", "Conectamos a su empresa con equipos de universidades de referencia mundial para proyectos de consultoría y desarrollo tecnológico.")],
            how_h="Cómo trabajamos",
            how=[("Primera conversación", "Nos cuenta sus retos. Antes de compartir información sensible, firmamos un acuerdo de confidencialidad."),
                 ("Diagnóstico", "Analizamos la situación con la dirección y con los equipos implicados."),
                 ("Recomendaciones", "Le presentamos recomendaciones concretas y las acciones para llevarlas a cabo."),
                 ("Puesta en marcha", "Le acompañamos en la ejecución, con programas de formación, proyectos con equipos universitarios o ambos.")],
            alone_h="Sola o junto a un programa",
            alone_p="La consultoría puede contratarse como servicio independiente o combinarse con nuestros programas de formación. Cada proyecto se presupuesta según su alcance.",
            alone_a="Ver cursos para empresas",
            faq_h="Preguntas frecuentes",
            faq=[("¿Se puede contratar la consultoría sin un programa de formación?", "Sí. Es un servicio independiente, aunque también puede combinarse con cualquiera de nuestros programas."),
                 ("¿A quién va dirigida?", "A comités de dirección, alta dirección y responsables de personas, estrategia, innovación y transformación digital de grandes organizaciones."),
                 ("¿Cómo se presupuesta?", "Según el alcance de cada proyecto. Cuéntenos su situación y le prepararemos una propuesta."),
                 ("¿Es confidencial?", "Sí. Firmamos un acuerdo de confidencialidad antes de compartir cualquier información sensible.")],
            cta_h="Hablemos de su estrategia", cta_p="Cuéntenos qué quiere conseguir y le propondremos cómo empezar."),
        "en": dict(
            title="Executive consulting in learning and AI | NextMind Learning",
            desc="Consulting for leadership teams: learning strategy, AI and technology capability assessment, and projects with world-leading university teams.",
            h1="Executive consulting",
            lead="We help leadership teams turn business strategy into capabilities: what each level of the organization should learn, how, and with whom.",
            what_h="What we do",
            what=[("Learning strategy", "We set learning priorities with leadership and align them with your business transformation goals."),
                  ("Capability assessment", "We identify what each level of the organization needs to learn in AI and technology, connecting leadership's vision with the real needs of technical teams."),
                  ("Long-term capability building", "We design learning journeys and corporate academies that can be extended to other departments, subsidiaries and countries."),
                  ("Projects with university teams", "We connect your company with teams from world-leading universities for consulting and technology development projects.")],
            how_h="How we work",
            how=[("First conversation", "You tell us about your challenges. Before any sensitive information is shared, we sign a confidentiality agreement."),
                 ("Assessment", "We review the situation with leadership and the teams involved."),
                 ("Recommendations", "We present concrete recommendations and the actions needed to carry them out."),
                 ("Implementation", "We support execution through learning programs, projects with university teams, or both.")],
            alone_h="On its own or with a program",
            alone_p="Consulting can be engaged as a standalone service or combined with our learning programs. Each project is quoted according to its scope.",
            alone_a="See corporate courses",
            faq_h="Frequently asked questions",
            faq=[("Can we engage consulting without a learning program?", "Yes. It is a standalone service, and it can also be combined with any of our programs."),
                 ("Who is it for?", "Executive committees, senior leaders and heads of people, strategy, innovation and digital transformation in large organizations."),
                 ("How is it priced?", "According to the scope of each project. Tell us about your situation and we will prepare a proposal."),
                 ("Is it confidential?", "Yes. We sign a confidentiality agreement before any sensitive information is shared.")],
            cta_h="Let's talk about your strategy", cta_p="Tell us what you want to achieve and we will suggest how to start."),
    }[lang]
    blocks = '<div class="blocks">' + "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in T["what"]) + "</div>"
    how = '<ol class="steps steps-4">' + "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in T["how"]) + "</ol>"
    body = f"""
{page_hero(k, lang, T['h1'], T['lead'], img="consulting-hero")}
<section class="section"><div class="wrap"><div class="section-head"><h2>{e(T['what_h'])}</h2></div>{blocks}</div></section>
<section class="section section-alt"><div class="wrap"><div class="section-head"><h2>{e(T['how_h'])}</h2></div>{how}</div></section>
<section class="section"><div class="wrap split"><h2>{e(T['alone_h'])}</h2><div><p class="lead">{e(T['alone_p'])}</p>
  <p><a href="{rel(k, lang, ROUTES['courses'][lang])}">{e(T['alone_a'])}</a></p></div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2>{e(T['faq_h'])}</h2></div>{faq_html(T['faq'])}</div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    service = {"@type": "Service", "@id": url(k, lang) + "#service", "name": T["h1"], "description": T["desc"],
               "serviceType": "Executive consulting" if lang == "en" else "Consultoría ejecutiva",
               "provider": {"@id": ORG_ID},
               "areaServed": [{"@type": "Country", "name": "Spain"}, {"@type": "Place", "name": "Latin America"}]}
    return T["title"], T["desc"], body, [service, faq_ld(T["faq"])]


def partners(lang):
    k = "partners"
    T = {
        "es": dict(
            title="Alianzas universitarias y formación ejecutiva | NextMind Learning",
            desc="Co-desarrollamos con universidades programas académicos, formación ejecutiva, bootcamps tecnológicos y experiencias internacionales.",
            h1="Alianzas con universidades",
            lead="Colaboramos con universidades e instituciones de educación superior para ampliar el acceso a formación ejecutiva de primer nivel y a programas en tecnologías emergentes.",
            what_h="Qué podemos construir juntos",
            what=[("Programas académicos co-desarrollados", "Nuevos programas diseñados junto a su institución y adaptados a sus objetivos."),
                  ("Formación ejecutiva", "Iniciativas de formación ejecutiva para ampliar su oferta a profesionales y empresas."),
                  ("Colaboración con profesorado", "Sesiones, módulos y proyectos con profesorado de universidades de referencia mundial."),
                  ("Bootcamps tecnológicos", "Programas intensivos en inteligencia artificial y otras tecnologías emergentes."),
                  ("Experiencias internacionales", "Estancias y experiencias de estudio en universidades de otros países."),
                  ("Programas a medida", "Oportunidades de aprendizaje diseñadas para cada institución.")],
            uni_h="Universidades con las que trabajamos",
            unis=[("Institutos tecnológicos líderes", "Inteligencia artificial, computación cuántica, ciberseguridad, internet de las cosas, biotecnología, innovación y liderazgo en ingeniería, con formación profesional online y presencial."),
                  ("Universidades de referencia en liderazgo y gestión", "Liderazgo y programas conjuntos que combinan el enfoque directivo con contenido tecnológico."),
                  ("Universidades de investigación en ciencias de la salud", "Proyectos en biotecnología y salud pública."),
                  ("Universidades públicas de referencia", "Programas preuniversitarios en sus campus.")],
            why_h="Un modelo flexible y a largo plazo",
            why=["Combinamos experiencia global con conocimiento local para ayudar a las universidades a reforzar su oferta y preparar a estudiantes y profesionales para el futuro del trabajo.",
                 "Tanto si quiere enriquecer su catálogo actual como lanzar nuevas iniciativas ejecutivas o tecnológicas, buscamos alianzas duraderas con impacto real."],
            cta_h="Exploremos una alianza", cta_p="Cuéntenos los objetivos de su institución y estudiaremos juntos el mejor modelo de colaboración."),
        "en": dict(
            title="University partnerships | NextMind Learning",
            desc="We work with universities to co-develop academic programs, executive education, technology bootcamps and international experiences in emerging technologies.",
            h1="University partnerships",
            lead="We work with universities and higher education institutions to widen access to world-class executive education and emerging technology programs.",
            what_h="What we can build together",
            what=[("Co-developed academic programs", "New programs designed with your institution and shaped around its goals."),
                  ("Executive education", "Executive education initiatives that extend your offer to professionals and companies."),
                  ("Faculty collaboration", "Sessions, modules and projects with faculty from world-leading universities."),
                  ("Technology bootcamps", "Intensive programs in artificial intelligence and other emerging technologies."),
                  ("International experiences", "Study experiences at universities abroad."),
                  ("Tailored programs", "Learning opportunities designed for each institution.")],
            uni_h="Universities we work with",
            unis=[("Leading institutes of technology", "Artificial intelligence, quantum computing, cybersecurity, the Internet of Things, biotechnology, innovation and engineering leadership, with online and in-person professional education."),
                  ("Universities renowned for leadership and management", "Leadership, and joint programs that pair a management focus with technology content."),
                  ("Research universities in the health sciences", "Projects in biotechnology and public health."),
                  ("Leading public universities", "Pre-university programs on their campuses.")],
            why_h="A flexible, long-term model",
            why=["We combine global expertise with local knowledge to help universities strengthen their offer and prepare students and professionals for the future of work.",
                 "Whether you want to enrich your existing portfolio or launch new executive or technology initiatives, we look for lasting partnerships with real impact."],
            cta_h="Let's explore a partnership", cta_p="Tell us your institution's goals and we will work out the best collaboration model together."),
    }[lang]
    blocks = '<div class="blocks">' + "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in T["what"]) + "</div>"
    unis = '<ul class="uni">' + "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in T["unis"]) + "</ul>"
    body = f"""
{page_hero(k, lang, T['h1'], T['lead'], 'partners-hero')}
<section class="section"><div class="wrap"><div class="section-head"><h2>{e(T['what_h'])}</h2></div>{blocks}</div></section>
<section class="section section-alt"><div class="wrap"><div class="section-head"><h2>{e(T['uni_h'])}</h2></div>{unis}</div></section>
<section class="section"><div class="wrap split"><h2>{e(T['why_h'])}</h2><div>{''.join(f'<p>{e(p)}</p>' for p in T['why'])}</div></div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    return T["title"], T["desc"], body, []


def camps(lang):
    k = "camps"
    T = {
        "es": dict(
            title="Campamentos de IA para estudiantes | NextMind Learning",
            desc="Campamentos tecnológicos de verano e invierno desde los 16 años en campus de EE. UU.: IA, innovación, inglés y acceso a la universidad.",
            h1="Campamentos tecnológicos para estudiantes preuniversitarios",
            lead="Programas inmersivos de verano y de invierno para estudiantes a partir de 16 años que se preparan para la universidad y para una carrera en tecnología.",
            learn_h="Qué aprenden",
            learn="Según la edición, los programas se centran en inteligencia artificial, aprendizaje automático, ciberseguridad, ciencia de datos, internet de las cosas, robótica o emprendimiento, combinando aprendizaje académico con experiencias prácticas.",
            how_h="Cómo es un campamento",
            how_p="Cada edición combina algunos de estos elementos:",
            parts=[("Vida en un campus universitario", "Residencias, comedores, bibliotecas e instalaciones de universidades de Estados Unidos."),
                   ("Inteligencia artificial e innovación", "Sesiones impartidas por profesorado universitario, con casos reales y trabajo en grupo."),
                   ("Inglés y cultura", "Clases de inglés por niveles y actividades culturales."),
                   ("Preparación para la admisión universitaria", "Orientación sobre el ensayo de admisión, el SAT y el Duolingo English Test."),
                   ("Formato combinado", "Un curso online con certificado seguido de una estancia en el campus."),
                   ("Visitas a campus", "Visitas guiadas a campus de universidades de referencia en Estados Unidos."),
                   ("Acompañamiento", "Personal de apoyo durante el programa, guía previa al viaje y documentación de apoyo para el visado.")],
            why_h="Por qué participar",
            why=["Vivir la vida universitaria antes de solicitar plaza.",
                 "Reforzar la candidatura a universidades competitivas.",
                 "Obtener un certificado al completar el programa, cuando la edición lo incluye.",
                 "Conocer a estudiantes de otros países."],
            note="El contenido, la sede y el calendario varían en cada edición.",
            cta_h="Pregúntenos por las próximas ediciones", cta_p="Escríbanos y le informaremos de los programas, sedes y requisitos."),
        "en": dict(
            title="AI camps for pre-university students | NextMind Learning",
            desc="Summer and winter technology camps for students aged 16+ on US university campuses: AI, innovation, English and admissions preparation.",
            h1="Technology camps for pre-university students",
            lead="Immersive summer and winter programs for students aged 16 and over who are preparing for university and a career in technology.",
            learn_h="What students learn",
            learn="Depending on the edition, programs focus on artificial intelligence, machine learning, cybersecurity, data science, the Internet of Things, robotics or entrepreneurship, combining academic learning with hands-on experience.",
            how_h="What a camp looks like",
            how_p="Each edition combines some of these elements:",
            parts=[("Life on a university campus", "Residence halls, dining halls, libraries and facilities at US universities."),
                   ("Artificial intelligence and innovation", "Sessions taught by university faculty, with real cases and group work."),
                   ("English and culture", "Level-based English classes and cultural activities."),
                   ("University admissions preparation", "Guidance on admission essays, the SAT and the Duolingo English Test."),
                   ("Blended format", "A certificate-bearing online course followed by a stay on campus."),
                   ("Campus visits", "Guided visits to the campuses of leading US universities."),
                   ("Support", "Staff support throughout the program, pre-departure guidance and visa support documents.")],
            why_h="Why take part",
            why=["Experience university life before applying.",
                 "Strengthen applications to competitive universities.",
                 "Earn a certificate on completion, where the edition includes one.",
                 "Meet students from other countries."],
            note="Content, location and dates vary with each edition.",
            cta_h="Ask us about upcoming editions", cta_p="Write to us and we will tell you about programs, locations and requirements."),
    }[lang]
    blocks = '<div class="blocks">' + "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in T["parts"]) + "</div>"
    body = f"""
{page_hero(k, lang, T['h1'], T['lead'], 'camps-hero')}
<section class="section"><div class="wrap split"><h2>{e(T['learn_h'])}</h2><p class="lead">{e(T['learn'])}</p></div></section>
<section class="section section-alt"><div class="wrap"><div class="section-head"><h2>{e(T['how_h'])}</h2><p>{e(T['how_p'])}</p></div>{media(k, lang, 'camps-campus', wide=True)}{blocks}</div></section>
<section class="section"><div class="wrap split"><h2>{e(T['why_h'])}</h2><div>{ticks(T['why'])}<p class="note">{e(T['note'])}</p></div></div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    return T["title"], T["desc"], body, []


def about(lang):
    k = "about"
    T = {
        "es": dict(
            title="Sobre NextMind Learning | Formación ejecutiva en tecnología",
            desc="NextMind Learning ayuda a grandes organizaciones a formar líderes y equipos preparados para el futuro en tecnologías emergentes, ingeniería y liderazgo.",
            h1="Sobre NextMind Learning",
            lead="Creemos que el futuro pertenece a las organizaciones que aprenden, se adaptan e innovan de forma continua.",
            body=["A medida que la tecnología transforma cada sector, las empresas necesitan algo más que conocimiento: necesitan capacidades prácticas que permitan a sus líderes decidir mejor, impulsar la transformación y crear ventajas competitivas duraderas.",
                  "Trabajamos con grandes organizaciones para ofrecer formación ejecutiva de primer nivel en tecnologías emergentes, ingeniería y liderazgo, combinando aprendizaje online, sesiones en directo y programas totalmente a medida. Cada proyecto parte de las prioridades estratégicas del cliente, para que el aprendizaje se traduzca en impacto en el negocio."],
            mission_l="Misión", mission="Impulsar a las organizaciones con experiencias de aprendizaje que formen líderes preparados para el futuro, aceleren la adopción tecnológica y desarrollen las capacidades necesarias en un mundo en rápida evolución.",
            vision_l="Visión", vision="Ser el socio global de confianza en formación ejecutiva, para que las organizaciones desarrollen el potencial de su gente, abracen la innovación y lideren el futuro mediante el aprendizaje continuo.",
            values_h="Nuestros valores",
            values=[("Excelencia", "Experiencias de aprendizaje con el máximo nivel académico y profesional."),
                    ("Innovación", "Tecnologías emergentes, ideas nuevas y enfoques que ayudan a anticiparse al cambio."),
                    ("Impacto", "Todo lo que hacemos busca resultados medibles para el crecimiento y la transformación."),
                    ("Colaboración", "Entendemos los retos de cada cliente y co-creamos con él su programa."),
                    ("Integridad", "Relaciones a largo plazo basadas en la confianza, la transparencia y la confidencialidad."),
                    ("Aprendizaje continuo", "La base de la innovación, el liderazgo y el éxito sostenible.")],
            cta_h="Construyamos lo que viene", cta_p="Cada organización tiene su propio camino de aprendizaje. Hablemos del suyo."),
        "en": dict(
            title="About NextMind Learning | Executive education in technology",
            desc="NextMind Learning helps large organizations develop future-ready leaders and teams through executive education in emerging technologies, engineering and leadership.",
            h1="About NextMind Learning",
            lead="We believe the future belongs to organizations that continuously learn, adapt and innovate.",
            body=["As technology reshapes every industry, businesses need more than knowledge: they need practical capabilities that help their leaders make better decisions, drive transformation and build lasting competitive advantage.",
                  "We work with large organizations to deliver world-class executive education in emerging technologies, engineering and leadership, combining online learning, live instruction and fully tailored programs. Every engagement starts from the client's strategic priorities, so that learning turns into business impact."],
            mission_l="Mission", mission="To empower organizations with learning experiences that develop future-ready leaders, accelerate technology adoption and build the capabilities needed to thrive in a fast-changing world.",
            vision_l="Vision", vision="To be the trusted global partner for executive education, helping organizations unlock their people's potential, embrace innovation and lead the future through lifelong learning.",
            values_h="Our values",
            values=[("Excellence", "Learning experiences of the highest academic and professional standard."),
                    ("Innovation", "Emerging technologies, new ideas and approaches that keep organizations ahead of change."),
                    ("Impact", "Everything we do aims at measurable outcomes for growth and transformation."),
                    ("Collaboration", "We understand each client's challenges and co-create their program with them."),
                    ("Integrity", "Long-term relationships built on trust, transparency and confidentiality."),
                    ("Lifelong learning", "The foundation of innovation, leadership and sustainable success.")],
            cta_h="Let's build what's next", cta_p="Every organization has its own learning journey. Let's talk about yours."),
    }[lang]
    vals = '<ul class="values">' + "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in T["values"]) + "</ul>"
    body = f"""
{page_hero(k, lang, T['h1'], T['lead'], 'about-hero')}
<section class="section"><div class="wrap split"><div></div><div>{''.join(f'<p>{e(p)}</p>' for p in T['body'])}</div></div></section>
<section class="section section-alt"><div class="wrap split">
  <div><p class="kicker">{e(T['mission_l'])}</p><p class="statement">{e(T['mission'])}</p></div>
  <div><p class="kicker">{e(T['vision_l'])}</p><p class="statement">{e(T['vision'])}</p></div>
</div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2>{e(T['values_h'])}</h2></div>{vals}</div></section>
{cta_band(k, lang, T['cta_h'], T['cta_p'])}
"""
    return T["title"], T["desc"], body, []


def contact(lang):
    k = "contact"
    T = {
        "es": dict(
            title="Contacto: formación ejecutiva a medida | NextMind Learning",
            desc="Cuéntenos sus objetivos y diseñaremos con usted un programa de formación ejecutiva en IA y tecnología para su organización.",
            h1="Hablemos",
            lead="Transformar una organización empieza por desarrollar a sus personas. Cuéntenos sus objetivos y le ayudaremos a diseñar una experiencia de aprendizaje con impacto duradero.",
            name="Nombre y apellidos", company="Empresa o institución", role="Cargo", email="Correo electrónico", phone="Teléfono (opcional)",
            interest="Me interesa", opts=["Cursos para empresas", "Alianza universitaria", "Campamentos", "Otro"],
            msg="Mensaje", consent="He leído la {link} y acepto que NextMind Learning use estos datos para responder a mi consulta.", consent_link="política de privacidad", layer="Responsable: NextMind Learning S.L. Finalidad: responder a su consulta. Base jurídica: su consentimiento. Destinatarios: no se ceden datos a terceros, salvo obligación legal. Derechos: acceso, rectificación, supresión y otros, como se explica en la política de privacidad.",
            send="Enviar mensaje", sending="Enviando…", ok_h="Gracias por escribirnos", ok_p="Hemos recibido su mensaje y le responderemos lo antes posible.", ok_redirect="Le llevaremos a la página de inicio en {n} segundos.", ok_home="Ir al inicio ahora", side_h="Escríbanos directamente", subject="Nuevo contacto desde la web"),
        "en": dict(
            title="Contact us about executive education | NextMind Learning",
            desc="Tell us your goals and we will design an executive education program in AI and technology for your organization with you.",
            h1="Let's talk",
            lead="Transforming an organization starts with developing its people. Tell us your goals and we will help you design a learning experience with lasting impact.",
            name="Full name", company="Company or institution", role="Job title", email="Email", phone="Phone (optional)",
            interest="I'm interested in", opts=["Corporate courses", "University partnership", "Camps", "Other"],
            msg="Message", consent="I have read the {link} and agree that NextMind Learning may use this information to reply to my enquiry.", consent_link="privacy policy", layer="Controller: NextMind Learning S.L. Purpose: to answer your enquiry. Legal basis: your consent. Recipients: data is not shared with third parties unless legally required. Rights: access, rectification, erasure and others, as explained in the privacy policy.",
            send="Send message", sending="Sending…", ok_h="Thank you for getting in touch", ok_p="We have received your message and will get back to you as soon as possible.", ok_redirect="We will take you to the home page in {n} seconds.", ok_home="Go to the home page now", side_h="Or write to us directly", subject="New website enquiry"),
    }[lang]
    opts = "".join(f"<option>{e(o)}</option>" for o in T["opts"])
    phone = f'<p>{e(CONFIG["phone"])}</p>' if CONFIG["phone"] else ""
    li = f'<p><a href="{e(CONFIG["linkedin"])}" rel="me">LinkedIn</a></p>' if CONFIG["linkedin"] else ""
    body = f"""
{page_hero(k, lang, T['h1'], T['lead'])}
<section class="section"><div class="wrap contact-grid">
  <div class="form-ok" id="form-ok" tabindex="-1" role="status" hidden data-home="{rel(k, lang, ROUTES['home'][lang]) or './'}" data-redirect="{e(T['ok_redirect'])}"><h2>{e(T['ok_h'])}</h2><div class="stem"><div><p class="lead">{e(T['ok_p'])}</p>
    <p class="form-ok-redirect"></p><p><a href="{rel(k, lang, ROUTES['home'][lang]) or './'}">{e(T['ok_home'])}</a></p></div></div></div>
  <form class="form" id="contact-form" action="{e(CONFIG['form_endpoint'])}" method="POST" data-sending="{e(T['sending'])}">
    <input type="hidden" name="_subject" value="{e(T['subject'])}">
    <input type="hidden" name="language" value="{lang}">
    <div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
    <div class="field"><label for="f-name">{e(T['name'])}</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-company">{e(T['company'])}</label><input id="f-company" name="company" autocomplete="organization" required></div>
    <div class="field"><label for="f-role">{e(T['role'])}</label><input id="f-role" name="role" autocomplete="organization-title"></div>
    <div class="field"><label for="f-email">{e(T['email'])}</label><input id="f-email" type="email" name="email" autocomplete="email" required></div>
    <div class="field"><label for="f-phone">{e(T['phone'])}</label><input id="f-phone" type="tel" name="phone" autocomplete="tel"></div>
    <div class="field"><label for="f-interest">{e(T['interest'])}</label><select id="f-interest" name="interest">{opts}</select></div>
    <div class="field full"><label for="f-msg">{e(T['msg'])}</label><textarea id="f-msg" name="message" required></textarea></div>
    <div class="field full"><label class="check"><input type="checkbox" name="consent" value="yes" required> <span>{e(T['consent']).replace('{link}', f'<a href="{rel(k, lang, ROUTES["privacy"][lang])}">' + e(T['consent_link']) + '</a>')}</span></label></div>
    <p class="field full form-layer">{e(T['layer'])}</p>
    <div class="field full"><button class="btn btn-primary" type="submit">{e(T['send'])}</button></div>
  </form>
  <div class="contact-side"><h2 style="font-size:1.4rem">{e(T['side_h'])}</h2>
    <p><a href="mailto:{e(CONFIG['email'])}">{e(CONFIG['email'])}</a></p>{phone}{li}</div>
</div></section>
"""
    return T["title"], T["desc"], body, [{"@type": "ContactPage", "url": url(k, lang), "name": T["title"]}]


def _legal_page(k, lang, D):
    secs = "".join(
        f'<section class="legal-sec"><h2>{e(h)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) + "</section>"
        for h, ps in D["sections"])
    body = f"""
{page_hero(k, lang, D['h1'], D['lead'])}
<section class="section"><div class="wrap legal-text">{secs}<p class="note">{e(UPDATED[lang])}</p></div></section>
"""
    return D["title"], D["desc"], body, []


def legal(lang):
    return _legal_page("legal", lang, LEGAL[lang])


def privacy(lang):
    return _legal_page("privacy", lang, PRIVACY[lang])


PAGES = {"home": home, "courses": courses, "consulting": consulting, "partners": partners, "camps": camps, "about": about, "contact": contact, "legal": legal, "privacy": privacy}


# ------------------------------------------------------------------ layout
def org_ld():
    org = {
        "@type": "EducationalOrganization", "@id": ORG_ID, "name": BRAND, "url": SITE + "/",
        "logo": SITE + "/assets/logo.png", "email": CONFIG["email"],
        "legalName": CONFIG["legal_name"], "taxID": CONFIG["tax_id"],
        "address": {"@type": "PostalAddress", "streetAddress": CONFIG["street"], "postalCode": CONFIG["postal_code"],
                    "addressLocality": CONFIG["city"], "addressCountry": CONFIG["country_code"]},
        "description": "NextMind Learning designs corporate courses and executive education programs in artificial intelligence, cybersecurity, digital transformation, engineering and leadership for large companies, with faculty from world-leading US universities. It also runs university partnerships and pre-university technology camps.",
        "areaServed": ["Spain", "Latin America"],
        "knowsAbout": ["Artificial intelligence", "Agentic AI", "Generative AI", "Machine learning", "Cybersecurity",
                       "Quantum computing", "Internet of Things", "Digital transformation", "Data science",
                       "Systems engineering", "Supply chain", "ESG", "Innovation", "Executive leadership",
                       "Corporate training", "Executive education"],
    }
    if CONFIG["phone"]:
        org["telephone"] = CONFIG["phone"]
    if CONFIG["linkedin"]:
        org["sameAs"] = [CONFIG["linkedin"]]
    return org


def layout(key, lang, title, desc, body, extra_ld):
    u = UI[lang]
    other = "en" if lang == "es" else "es"
    canonical = url(key, lang)
    nav_links = "".join(
        f'<a href="{rel(key, lang, ROUTES[n][lang])}"{" class=\"nav-primary\"" if n == "courses" else ""}'
        f'{" aria-current=\"page\"" if n == key else ""}>{e(u["nav"][n])}</a>' for n in NAV)
    home_href = rel(key, lang, ROUTES["home"][lang]) or "./"
    crumbs = [{"@type": "ListItem", "position": 1, "name": u["nav"]["home"], "item": url("home", lang)}]
    if key != "home":
        crumbs.append({"@type": "ListItem", "position": 2, "name": u["nav"][key], "item": canonical})
    graph = [org_ld(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND,
              "publisher": {"@id": ORG_ID}, "inLanguage": ["es", "en"]},
             {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
              "description": desc, "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"},
              "about": {"@id": ORG_ID}, "dateModified": TODAY},
             {"@type": "BreadcrumbList", "itemListElement": crumbs}] + extra_ld
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    foot_nav = "".join(f'<li><a href="{rel(key, lang, ROUTES[n][lang])}">{e(u["nav"][n])}</a></li>' for n in ["home"] + NAV + ["contact"])
    phone = f'<li>{e(CONFIG["phone"])}</li>' if CONFIG["phone"] else ""
    li = f'<li><a href="{e(CONFIG["linkedin"])}" rel="me">LinkedIn</a></li>' if CONFIG["linkedin"] else ""
    year = datetime.date.today().year
    a = lambda p: rel(key, lang, p)
    og_locale = "es_ES" if lang == "es" else "en_US"
    verify_tags = ""
    if CONFIG.get("google_site_verification"):
        verify_tags += f'\n<meta name="google-site-verification" content="{e(CONFIG["google_site_verification"])}">'
    if CONFIG.get("bing_site_verification"):
        verify_tags += f'\n<meta name="msvalidate.01" content="{e(CONFIG["bing_site_verification"])}">'
    lang_names = {"es": "Español", "en": "English"}
    lang_items = "".join(
        f'<li><a href="{rel(key, lang, ROUTES[key][l]) or "./"}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=\"true\"" if l == lang else ""}><b>{l.upper()}</b> {lang_names[l]}</a></li>'
        for l in ("es", "en"))
    lang_label = "Idioma" if lang == "es" else "Language"
    lang_menu = (f'<details class="lang-menu"><summary aria-label="{lang_label}: {lang_names[lang]}">'
                 f'{lang.upper()}<svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></summary>'
                 f'<ul>{lang_items}</ul></details>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">{verify_tags}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{url(key, 'es')}">
<link rel="alternate" hreflang="en" href="{url(key, 'en')}">
<link rel="alternate" hreflang="x-default" href="{url(key, 'es')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'es' else 'es_ES'}">
<meta property="og:image" content="{SITE}/assets/og-{lang}.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{a('assets/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{a('assets/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{a('assets/apple-touch-icon.png')}">
<link rel="preload" href="{a('assets/fonts/ArchivoExpanded-Variable.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a('assets/fonts/Archivo-Variable.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a('assets/styles.css')}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{e(u['skip'])}</a>
<header class="site-header"><div class="wrap bar">
  <a class="logo" href="{home_href}" aria-label="{BRAND}">{LOGO_SVG}</a>
  <nav class="nav" id="site-nav" aria-label="{e(u['footer_nav'])}">{nav_links}<a class="nav-cta" href="{a(ROUTES['contact'][lang])}">{e(u['cta'])}</a></nav>
  {lang_menu}
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{e(u['menu'])}"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
  <a class="btn btn-primary" href="{a(ROUTES['contact'][lang])}">{e(u['cta'])}</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer on-black"><div class="wrap">
  <div class="foot-grid">
    <div><a class="foot-logo" href="{home_href}" aria-label="{BRAND}">{LOGO_SVG}</a><p>{e(u['footer_tag'])}</p></div>
    <div><h2>{e(u['footer_nav'])}</h2><ul>{foot_nav}</ul></div>
    <div><h2>{e(u['footer_contact'])}</h2><ul><li><a href="mailto:{e(CONFIG['email'])}">{e(CONFIG['email'])}</a></li>{phone}{li}
      <li><a href="{rel(key, lang, ROUTES[key][other]) or './'}" hreflang="{other}" lang="{other}">{e(u['switch'])}</a></li></ul></div>
  </div>
  <div class="legal"><p>&copy; {year} {CONFIG['legal_name']} · NIF {CONFIG['tax_id']} · {e(CONFIG['street'])}, {CONFIG['postal_code']} {CONFIG['city']}. {e(u['rights'])}</p>
    <p><a href="{a(ROUTES['legal'][lang])}">{e(u['nav']['legal'])}</a> · <a href="{a(ROUTES['privacy'][lang])}">{e(u['nav']['privacy'])}</a> · {e(u['universities_note'])}</p></div>
</div></footer>
<script src="{a('assets/site.js')}" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ extra files
def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    prio = {"home": "1.0", "courses": "0.9", "consulting": "0.8", "legal": "0.2", "privacy": "0.2"}
    for key in ROUTES:
        for lang in ("es", "en"):
            out.append(f"<url><loc>{url(key, lang)}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(key, '0.6')}</priority>"
                       f'<xhtml:link rel="alternate" hreflang="es" href="{url(key, "es")}"/>'
                       f'<xhtml:link rel="alternate" hreflang="en" href="{url(key, "en")}"/>'
                       f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(key, "es")}"/></url>')
    out.append("</urlset>")
    return "\n".join(out)


def robots():
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "PerplexityBot", "Google-Extended", "Applebot", "Applebot-Extended"]
    lines = [f"User-agent: {b}\nAllow: /\n" for b in bots]
    return "\n".join(lines) + f"\nUser-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"


def llms():
    topics_en = "\n".join(f"- {area_name(a, 'en')}: {ten}" for a, tes, ses, ten, sen in TOPICS)
    return f"""# {BRAND}

> {BRAND} designs corporate courses and executive education programs for large companies in artificial intelligence (including generative and agentic AI), cybersecurity, digital transformation, quantum computing, the Internet of Things, engineering, fashion and retail technology, sustainability and leadership. Programs are delivered with faculty from world-leading US universities, including leading institutes of technology and universities renowned for leadership, management and health sciences. Institution details are shared in proposals. It serves organizations in Spain and Latin America, and programs can be rolled out internationally. Website available in Spanish and English.

## Main service: corporate courses for large companies
- Formats: pre-designed programs (online courses from the universities' own professional learning platforms), blended programs (online + live workshops with university faculty), live virtual programs (from a single executive session or masterclass to multi-session journeys), custom programs (curricula co-developed with each organization), and executive consulting on learning strategy.
- Delivery: remote, on site in the client's country, or campus immersion for selected cohorts. Length from a two-hour executive session to multi-month or multi-year initiatives.
- Audiences: executive committees and C-suite, senior leaders, directors, technical and engineering leaders, high-potential talent, innovation and transformation teams. Cohorts from small executive groups to hundreds of managers.
- Certificates: selected programs include a certificate issued by the university itself, subject to its requirements. Programs can combine technical content from a leading institute of technology with leadership content from a world-leading university; each institution certifies its own part.
- Process: first conversation and confidentiality agreement, needs assessment, tailored proposal, content design with university faculty, delivery with pre- and post-program assessment, scale-up to other departments, subsidiaries and countries.
- Pricing: quoted per project according to audience, format, duration and certification. No public price list.

## Topic catalog (indicative)
{topics_en}

## Secondary services
- Executive consulting: learning strategy, AI and technology capability assessment, long-term capability building and corporate academies, and consulting or technology development projects with university teams. Standalone or combined with programs.
- University partnerships: co-developed academic programs, executive education, faculty collaboration, technology bootcamps, international study experiences.
- Camps: summer and winter technology camps for pre-university students aged 16+, on US university campuses (AI, innovation, English, university admissions preparation).

## Pages
- [Home (ES)]({url('home', 'es')}) / [Home (EN)]({url('home', 'en')})
- [Cursos para empresas]({url('courses', 'es')}) / [Corporate courses]({url('courses', 'en')})
- [Consultoría]({url('consulting', 'es')}) / [Consulting]({url('consulting', 'en')})
- [Alianzas universitarias]({url('partners', 'es')}) / [University partnerships]({url('partners', 'en')})
- [Campamentos]({url('camps', 'es')}) / [Camps]({url('camps', 'en')})
- [Sobre nosotros]({url('about', 'es')}) / [About]({url('about', 'en')})
- [Contacto]({url('contact', 'es')}) / [Contact]({url('contact', 'en')})

## Contact
- Email: {CONFIG['email']}
"""


def not_found():
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada | {BRAND}</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="{SITE}/assets/styles.css"></head><body>
<section class="page-hero" style="min-height:100vh"><div class="wrap"><a class="logo" href="{SITE}/" aria-label="{BRAND}" style="margin-bottom:48px;display:inline-block">{LOGO_SVG}</a>
<h1>Página no encontrada</h1><div class="stem"><div><p class="lead">La página que busca no existe.</p><p>The page you are looking for does not exist.</p></div></div>
<p style="margin-top:2rem"><a class="btn btn-primary" href="{SITE}/">Ir al inicio</a> <a class="btn btn-secondary" href="{SITE}/en/">Go to home</a></p>
</div></section></body></html>"""


def images():
    """Renders icons and social images with the brand fonts and logo (needs playwright + chromium)."""
    import base64
    from playwright.sync_api import sync_playwright
    A = os.path.join(OUT, "assets")
    app_icon = open(os.path.join(ROOT, "brand", "app-icon.svg"), encoding="utf-8").read()
    logo = open(os.path.join(ROOT, "brand", "logo-black.svg"), encoding="utf-8").read()
    fonts = "".join(
        f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,'
        f'{base64.b64encode(open(os.path.join(ROOT, "assets", "fonts", f), "rb").read()).decode()}) format("woff2");font-weight:100 900}}'
        for fam, f in [("Archivo Expanded", "ArchivoExpanded-Variable.woff2"), ("Archivo", "Archivo-Variable.woff2")])
    og = {"es": ("Cursos para empresas con profesorado de universidades de referencia mundial",
                 "Formación ejecutiva en IA, ciberseguridad, transformación digital y liderazgo"),
          "en": ("Corporate courses with faculty from world-leading universities",
                 "Executive education in AI, cybersecurity, digital transformation and leadership")}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "logo.png")]:
            pg.set_viewport_size({"width": size, "height": size})
            pg.set_content(f'<style>*{{margin:0}}svg{{width:{size}px;height:{size}px;display:block}}</style>' +
                           app_icon.replace('rx="229"', 'rx="0"' if name == "logo.png" else 'rx="229"'))
            pg.screenshot(path=os.path.join(A, name), omit_background=True)
        pg.set_viewport_size({"width": 1200, "height": 630})
        for lang, (h, sub) in og.items():
            pg.set_content(f"""<style>{fonts}*{{margin:0;box-sizing:border-box}}
            body{{width:1200px;height:630px;background:#fff;padding:72px 80px;font-family:Archivo,Arial,sans-serif;position:relative}}
            .logo svg{{width:230px;height:auto;display:block}}
            h1{{font-family:"Archivo Expanded",Arial,sans-serif;font-weight:640;font-size:58px;line-height:66px;max-width:900px;margin-top:88px}}
            .stem{{display:flex;gap:20px;margin-top:32px}}.stem i{{width:12px;background:#F0A202}}
            p{{font-size:26px;line-height:36px;color:#575757;max-width:820px}}</style>
            <div class="logo">{logo}</div><h1>{e(h)}</h1><div class="stem"><i></i><p>{e(sub)}</p></div>""")
            pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(A, f"og-{lang}.png"))
        b.close()


def check_config():
    """Warns loudly while example values are still in CONFIG: SEO tags would point to a fake domain."""
    bad = [k for k in ("site_url", "email", "form_endpoint") if "YOUR-" in CONFIG[k]]
    if bad:
        print("\n" + "!" * 70)
        print("  NOT READY TO PUBLISH: edit these values in content.py ->", ", ".join(bad))
        print("  (canonical URLs, sitemap, hreflang and social images all depend on site_url)")
        print("!" * 70 + "\n")
    return not bad


def main():
    check_config()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(ROOT, "brand", "app-icon.svg"), os.path.join(OUT, "assets", "favicon.svg"))
    for f in ("logo-black.svg", "logo-white.svg"):
        shutil.copy(os.path.join(ROOT, "brand", f), os.path.join(OUT, "assets", f))
    optimize_video()
    for key, fn in PAGES.items():
        for lang in ("es", "en"):
            title, desc, body, ld = fn(lang)
            write(ROUTES[key][lang] + "index.html", layout(key, lang, title, desc, body, ld))
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    write("llms.txt", llms())
    write("404.html", not_found())
    write(".nojekyll", "")
    # Files in static/ are copied as-is to the site root (e.g. BingSiteAuth.xml, googleXXXX.html)
    static = os.path.join(ROOT, "static")
    if os.path.isdir(static):
        for name in os.listdir(static):
            src = os.path.join(static, name)
            if os.path.isfile(src) and not name.startswith("."):
                shutil.copy(src, os.path.join(OUT, name))
    if CONFIG["custom_domain"]:
        write("CNAME", CONFIG["custom_domain"] + "\n")
    images()
    print("Built", sum(len(f) for _, _, f in os.walk(OUT)), "files into", OUT)


if __name__ == "__main__":
    main()
