#!/usr/bin/env bash
# Build the dist/ output directory for Cloudflare Pages.
# Copies only the files the site needs at runtime and leaves out .git (660 MB of pack
# objects that Pages would scan as static assets and reject for exceeding the 25 MiB file limit).
set -euo pipefail

cd "$(dirname "$0")/.."

rm -rf dist
mkdir -p dist

cp -R index.html _headers robots.txt sitemap.xml og-cover.jpg data thumbs img dist/

echo "dist ready:"
du -sh dist
find dist -type f | wc -l
