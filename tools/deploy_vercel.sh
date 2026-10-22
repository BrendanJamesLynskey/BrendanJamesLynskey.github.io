#!/usr/bin/env bash
# Deploy origin/main (or another ref) to https://brendan-lynskey.vercel.app (the owner runs this; nothing deploys
# from CI).
#
#   tools/deploy_vercel.sh                    # origin/main
#   tools/deploy_vercel.sh design-classic     # any branch, tag or commit, e.g. the pre-datasheet design
#                                             # (tools/revert_design.sh does exactly this)
#
# Needs the Vercel CLI, logged in to the brendan-lynskeys-projects team. It deploys exactly what is at the ref
# (a git archive, so no local edits or untracked files go up), as a static site with no build step;
# .vercelignore keeps tools/, docs/, src/ and data/ out. Then it checks the live pages answer 200.
set -euo pipefail

SCOPE=brendan-lynskeys-projects
PROJECT=brendan-lynskey
URL=https://brendan-lynskey.vercel.app

repo=$(git rev-parse --show-toplevel)
ref=${1:-origin/main}
git -C "$repo" fetch -q --tags origin main
git -C "$repo" rev-parse -q --verify "$ref^{commit}" >/dev/null || { echo "no such ref: $ref" >&2; exit 1; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git -C "$repo" archive "$ref" | tar -x -C "$tmp"
echo "deploying $ref @ $(git -C "$repo" rev-parse --short "$ref^{commit}") from $tmp"

cd "$tmp"
# link the temporary directory to the existing project, then deploy it to production
vercel link --yes --scope "$SCOPE" --project "$PROJECT" >/dev/null
vercel deploy --prod --yes --scope "$SCOPE"

for path in / /sites/ /library/ /optalysys/ /cv/ /cv/Brendan_Lynskey_CV.pdf /checks/ /og.png /sitemap.xml; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "$URL$path")
  # a page that was checked before it existed can serve a cached 404 for a few seconds after the deploy
  for _ in 1 2 3; do [ "$code" = 200 ] && break; sleep 10; code=$(curl -s -o /dev/null -w '%{http_code}' "$URL$path"); done
  printf '%s  %s\n' "$code" "$URL$path"
done
printf '%s  %s (should be 404)\n' "$(curl -s -o /dev/null -w '%{http_code}' "$URL/tools/build.py")" "$URL/tools/build.py"
# the Digital Twin is a separate Vercel project (brendan-lynskey-twin), reached through the /twin rewrite in vercel.json
code=$(curl -s -o /dev/null -w '%{http_code}' "$URL/twin/")
for _ in 1 2 3; do [ "$code" = 200 ] && break; sleep 10; code=$(curl -s -o /dev/null -w '%{http_code}' "$URL/twin/"); done
if [ "$code" = 200 ]; then
  printf '%s  %s (Digital Twin, via the rewrite)\n' "$code" "$URL/twin/"
else
  printf '%s  %s (Digital Twin not answering: deploy it first with tools/deploy_both.sh or its own tools/deploy_twin.sh)\n' "$code" "$URL/twin/"
fi
# the chat endpoint ends in a slash, so it needs the catch-all rewrite as well as the page
chat=$(curl -s -o /dev/null -m 60 -w '%{http_code}' -X POST "$URL/twin/api/chat/" -H 'content-type: application/json' \
  -d '{"messages":[{"id":"deploy-check","role":"user","parts":[{"type":"text","text":"Hello"}]}]}')
printf '%s  %s (Digital Twin chat, via the rewrite)\n' "$chat" "$URL/twin/api/chat/"
