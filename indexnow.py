"""Notifies IndexNow (Bing, Yandex, Seznam, Naver...) that the site's pages were updated.
Runs automatically in GitHub Actions after each deploy. It never fails the deploy: any error is only printed.
Manual dry run (prints the request without sending it):  python3 indexnow.py --dry-run"""
import json, os, sys, urllib.request
from content import CONFIG, ROUTES

def main():
    key = CONFIG.get("indexnow_key", "")
    site = CONFIG["site_url"].rstrip("/")
    if not key or "YOUR-" in site:
        print("IndexNow skipped: no key or site_url not set."); return
    here = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(here, "static", key + ".txt")):
        print(f"IndexNow skipped: static/{key}.txt not found."); return
    urls = [f"{site}/{ROUTES[k][l]}" for k in ROUTES for l in ("es", "en")]
    payload = {"host": site.split("://", 1)[1], "key": key,
               "keyLocation": f"{site}/{key}.txt", "urlList": urls}
    if "--dry-run" in sys.argv:
        print(json.dumps(payload, indent=2)); return
    req = urllib.request.Request("https://api.indexnow.org/indexnow",
                                 data=json.dumps(payload).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs (200/202 = accepted)")
    except Exception as err:
        print("IndexNow: not sent -", err)

if __name__ == "__main__":
    main()
