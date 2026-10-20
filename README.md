# NextMind Learning website

Static, bilingual (Spanish at the root, English under /en/) website ready for GitHub Pages.

## 1. Fill in your details (required before publishing)
Open `content.py` and edit `CONFIG` at the top:

| Setting | What to put |
|---|---|
| `site_url` | Final address, no trailing slash. Custom domain: `https://www.yourdomain.com` · GitHub: `https://USERNAME.github.io/REPO` |
| `email` | Public contact email |
| `form_endpoint` | Create a free form at https://formspree.io and paste its endpoint (`https://formspree.io/f/xxxxxx`) |
| `phone`, `linkedin` | Optional. Leave `""` to hide |
| `custom_domain` | Only if you use one, e.g. `www.yourdomain.com` (creates the CNAME file) |

Then rebuild:
```
pip install playwright && python3 -m playwright install chromium   # used to render icons and social images
python3 build.py
```
Everything is generated into `site/`.

## 2. Publish on GitHub Pages
Option A, automatic (recommended): upload this whole folder (including `.github/`) to a repository's `main` branch,
then Settings -> Pages -> Source: "GitHub Actions". Every push downloads the photos and video, optimizes them,
builds the site and publishes it. Nothing to install on your computer.

Option B, quick: upload only the contents of `site/` to the repository root, then Settings -> Pages ->
Source: "Deploy from a branch" -> `main` / root. Photos and video then load from Unsplash and Mixkit.

Custom domain (nextmindlearning.com): Settings -> Pages -> Custom domain, then at your domain provider create
A records for the apex domain pointing to GitHub Pages' IPs (listed in GitHub's "Managing a custom domain" docs)
and a CNAME record for www pointing to USERNAME.github.io. Then tick "Enforce HTTPS".

## 3. After publishing (SEO)
1. Google Search Console: add the property, verify it, and submit `sitemap.xml`.
2. Bing Webmaster Tools: same (Bing also feeds ChatGPT and Copilot search).
3. Create a Google Business Profile and a LinkedIn company page with the same name, description and website. Add the LinkedIn URL to `CONFIG` and rebuild (it links your entity across the web).

## What is included for SEO / GEO
- Per-page titles and descriptions written for the searches large companies make (ES + EN).
- `hreflang`, canonical URLs, Open Graph / social images.
- Schema.org structured data: EducationalOrganization, WebSite, Service with a 53-course OfferCatalog, FAQPage, BreadcrumbList.
- `sitemap.xml` with language alternates, `robots.txt` that explicitly allows search and AI crawlers, and `llms.txt` (a plain summary for AI assistants).
- Fast static pages, mobile-first, accessible, with automatic dark mode as defined in the brand book.
- Brand fonts (Archivo, Archivo Expanded) are self-hosted in `assets/fonts`, so no visitor data goes to Google Fonts.

## Photos and hero video
The site uses royalty-free material, each item checked on its source page:
- Photos: 4 images from Unsplash (Unsplash License: free commercial use, no attribution required). Sources listed in `MEDIA_SOURCES` in `content.py`.
- Hero video: "Presentation in a business meeting room" from Mixkit (Mixkit Stock Video Free License).

Out of the box the site loads them directly from Unsplash and Mixkit. For best speed, and so the site doesn't depend on those servers, host them yourself:
```
python3 fetch_media.py   # downloads everything into media/
python3 build.py         # creates responsive WebP images; with ffmpeg installed, also optimized hero.mp4, hero.webm and a vertical mobile video
```
To use your own photos or video, drop files with the same names into `media/` (e.g. `media/home-intro.jpg`, `media/hero-source.mp4`) and rebuild.
The video only plays when the visitor allows motion and isn't saving data; otherwise the still poster shows. A pause button is always available.

## Editing text
All text lives in `content.py` (shared blocks and the topic catalog) and in the page functions inside `build.py`. Edit, run `python3 build.py`, upload `site/` again.
