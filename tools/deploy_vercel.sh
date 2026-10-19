#!/usr/bin/env bash
# Deploy origin/main to https://brendan-lynskey.vercel.app (the owner runs this; nothing deploys from CI).
#
#   tools/deploy_vercel.sh
#
# Needs the Vercel CLI, logged in to the brendan-lynskeys-projects team. It deploys exactly what is on
# origin/main (a git archive, so no local edits or untracked files go up), as a static site with no build step;
# .vercelignore keeps tools/, docs/, src/ and data/ out. Then it checks the live pages answer 200.
set -euo pipefail

SCOPE=brendan-lynskeys-projects
PROJECT=brendan-lynskey
URL=https://brendan-lynskey.vercel.app

repo=$(git rev-parse --show-toplevel)
git -C "$repo" fetch -q origin main
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git -C "$repo" archive origin/main | tar -x -C "$tmp"
echo "deploying origin/main @ $(git -C "$repo" rev-parse --short origin/main) from $tmp"

cd "$tmp"
# link the temporary directory to the existing project, then deploy it to production
vercel link --yes --scope "$SCOPE" --project "$PROJECT" >/dev/null
vercel deploy --prod --yes --scope "$SCOPE"

for path in / /sites/ /cv/ /cv/Brendan_Lynskey_CV.pdf /checks/ /og.png /sitemap.xml; do
  printf '%s  %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$URL$path")" "$URL$path"
done
printf '%s  %s (should be 404)\n' "$(curl -s -o /dev/null -w '%{http_code}' "$URL/tools/build.py")" "$URL/tools/build.py"
