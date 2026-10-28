# AI Pose Gallery · English Edition

> 288 pose sets / 1,439 AI human pose reference images. The original Japanese metadata is fully translated into English, with a responsive static gallery ready to deploy.

![Gallery preview](docs/preview.jpg)

<details><summary>Mobile preview</summary>

![Mobile preview](docs/mobile.jpg)

</details>

**Original site:** <https://ai-pose-gallery.pages.dev/>
**Original author:** ギア (@giaaibusi)
**Based on the Chinese edition by:** Anhao · [X @anhao_ai](https://x.com/anhao_ai) · <https://github.com/anhao/ai-pose-gallery-zh>

---

## What is this

The original site is a pose library for AI art, 3D and photography reference. Its metadata is entirely in Japanese and it offers no bulk download. This repository does three things:

1. **Full mirror**: all 1,439 thumbnails (JPG 300×400) and 1,439 full-size images (PNG 900×1200) for the 1,439 records, 2,878 files / 659.5 MB in total.
2. **Complete translation**: every Japanese field is translated into English, covering 4 sets, 26 categories, 288 pose names and 5 angles with nothing left out.
3. **A usable front end**: a zero-dependency responsive gallery that implements the original site's category filters, multi-angle switching, grouped browsing, lightbox navigation and full-size downloads, with a layout redesigned for phones.

## Features

- 4 set tabs, each showing its image and pose counts
- Search by pose name, number, ID or category; press `/` to focus the search box
- Filter by category and any of the 5 angles, with one-click reset
- Two modes: **Group by pose** and **All images**; grouped cards include multi-angle thumbnails
- Hover or tap a thumbnail to switch the main image's angle; click a card to open the lightbox
- The lightbox shows the thumbnail first, then loads the 900×1200 original; download the PNG, copy the ID or open it in a new tab
- `← / →` switch angle, `↑ / ↓` switch pose, `Esc` closes; swipe left/right on mobile
- Multi-column grid on desktop, two columns on mobile, collapsible filter panel on small screens
- Guide and terms dialogs; the footer credits the image source and maintainers

## SEO and sharing

The page ships with a full SEO and social sharing setup:

- Keyword-rich title: `AI Pose Reference Library | 288 Poses · 1,439 Multi-Angle Reference Images`
- Dedicated description, keywords, author and `max-image-preview:large`
- `canonical` points at the production domain so the custom domain and the pages.dev domain are not indexed twice
- Open Graph / Twitter Card use the 1200×630 `og-cover.jpg`
- JSON-LD structured data: `WebSite` + `ImageGallery`, declaring language, description and the page's primary image
- `robots.txt` allows the whole site and declares the sitemap; `sitemap.xml` points at the home page
- Semantic structure: a single H1, section H2s and card H3s; thumbnail `alt` text includes the pose name and angle; images are lazy-loaded

All absolute URLs in the repo point at `https://ai-pose-gallery.anhao.app/`. If you deploy under another domain, also replace the canonical, `og:*`, `twitter:*` and JSON-LD URLs in `index.html`, plus the URLs in `robots.txt` and `sitemap.xml`.

## Dataset

| Set | Records |
| --- | ---: |
| Full Body · Solo · Standard | 365 |
| Full Body · Solo · Sensual | 399 |
| Upper Body · Solo | 400 |
| Couple | 275 |
| **Total** | **1,439** |

Each record uses one of 5 angles: Front / 3/4 / Side / Above / Below.

## Directory layout

```
.
├── index.html              # Single-page gallery (zero dependencies)
├── robots.txt              # Crawler rules
├── sitemap.xml             # Sitemap
├── og-cover.jpg            # 1200×630 social sharing cover
├── data/
│   ├── pose.json           # Original Japanese data (1,439 records, unchanged)
│   ├── pose-en.json        # English data (read by the front end, includes a search field)
│   ├── meta.json           # Original set list
│   ├── meta-en.json        # English set list
│   └── translations.csv    # Japanese ⇄ English glossary (323 terms, for proofreading)
├── thumbs/                 # 1,439 JPG thumbnails 300×400 (22 MB)
├── img/                    # 1,439 PNG originals 900×1200 (637 MB)
├── scripts/
│   ├── download.py         # Concurrent downloader (48 threads / resumable / auto-retry)
│   ├── i18n.py             # Japanese → English dictionary (323 unique terms)
│   ├── apply_translation.py# Applies the dictionary and generates the English data
│   ├── verify.py           # Checks file integrity (existence / size / image header)
│   └── build.sh            # Builds the Cloudflare Pages output directory dist/
├── docs/                   # README preview images
├── _headers                # Cloudflare Pages cache rules
├── LICENSE
└── README.md
```

## Data format

Fields in `data/pose-en.json`:

| Field | Original Japanese field | Example | Notes |
| --- | --- | --- | --- |
| `id` | — | `full_sexy_P001_front` | Unique identifier |
| `system` | `系統` | Full Body · Solo · Sensual | 4 sets |
| `poseNo` | `ポーズ番号` | `P001` | Pose number (up to 80 per set) |
| `category` | `分類` | Standing | 26 categories |
| `name` | `ポーズ名` | S-curve stand, hip pushed to the side | 288 descriptions |
| `angle` | `アングル` | Front | 5 angles |
| `thumb` | `サムネ` | `thumbs/…jpg` | Relative path |
| `image` | `原寸` | `img/…png` | Relative path |
| `search` | — | Concatenated, lowercase | For fuzzy search |

The original Japanese data in `data/pose.json` is kept as-is, with field names matching the original site's API, so it can be compared or re-imported.

## Local preview

The gallery loads JSON with `fetch`, so it needs to be served over HTTP (opening `index.html` directly is blocked by CORS):

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000
```

## Scripts

```bash
# Re-download all images (existing files are skipped, safe to re-run)
python3 scripts/download.py
WORKERS=64 python3 scripts/download.py   # adjust concurrency

# After editing translations in scripts/i18n.py, regenerate the English data
python3 scripts/apply_translation.py

# Verify that all 2,878 files are complete
python3 scripts/verify.py
```

## Deploying to Cloudflare Pages

The repository is a plain static site with no framework and no dependencies.

**Option 1: automatic deploys from GitHub (recommended)**

1. Sign in to the Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Pick this repository → production branch `main`
3. Build settings:

   | Field | Value |
   | --- | --- |
   | Framework preset | `None` |
   | Build command | `bash scripts/build.sh` |
   | Build output directory | `dist` |

4. **Save and Deploy**; in 2–5 minutes you get `https://<project>.pages.dev`
5. Every `git push` redeploys automatically after that

> ⚠️ **Do not** set the Build output directory to `/`. The repo root contains `.git` (hundreds of MB);
> Cloudflare scans it as static assets and the pack files exceed the 25 MiB per-file limit, failing the build.
> `scripts/build.sh` copies only `index.html`, `_headers`, `data/`, `thumbs/` and `img/` into `dist/`.
> If you really want to use the root, the repo includes an `.assetsignore` that excludes non-site files as a fallback.

> Pages limits: ≤ 25 MiB per file and ≤ 20,000 files per deployment. The largest file here is 917 KB and there are 2,883 files in total, well within the limits.

**Option 2: direct upload from the command line**

```bash
bash scripts/build.sh
npx wrangler pages deploy dist --project-name ai-pose-gallery
```

`_headers` sets a one-year immutable cache for `img/` and `thumbs/`, so images are not fetched from origin repeatedly.

## Content notice

The library contains adult-oriented pose references (some category names use sexual terminology). It is intended only for artistic creation, figure reference and front-end learning. Do not use it for unlawful purposes. Not intended for minors.

## Copyright and credits

- **The copyright of the images and original data belongs to the original author ギア**; see the source link at the top
- This repository is a personal archive for learning, translation and static-site practice. It **claims no rights to the images** and does not grant any license for commercial use of the original work
- If the original author considers this repository to infringe their rights, please open an Issue and the content will be removed promptly
- The code in `scripts/` and `index.html` is open source under the MIT license (see [LICENSE](LICENSE)); that license **does not cover** the images and original data in `img/`, `thumbs/` and `data/`
