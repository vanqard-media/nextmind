"""Downloads the site's royalty-free photos and hero video into media/ so the site hosts them itself.
Run once on your computer (needs internet):  python3 fetch_media.py   then   python3 build.py
Photos: Unsplash License. Video: Mixkit Stock Video Free License. Both allow free commercial use without attribution."""
import os, urllib.request
from content import MEDIA_SOURCES, HERO_VIDEO_SOURCE

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "media")
os.makedirs(OUT, exist_ok=True)

def get(url, path):
    if os.path.exists(path):
        print("  exists ", os.path.basename(path)); return
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (NextMind site build)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        print("  saved  ", os.path.basename(path))
    except Exception as err:  # the site falls back to loading this file from its source
        print("  FAILED ", os.path.basename(path), "-", err)

for name, (base, page) in MEDIA_SOURCES.items():
    get(f"{base}?fm=jpg&q=85&w=2400", os.path.join(OUT, name + ".jpg"))
get(HERO_VIDEO_SOURCE["mp4"], os.path.join(OUT, "hero-source.mp4"))
get(HERO_VIDEO_SOURCE["poster"], os.path.join(OUT, "hero-poster.jpg"))
print("Done. Now run: python3 build.py (ffmpeg optimizes the video if installed).")
