#!/usr/bin/env bash
# Deploy the Digital Twin, then this landing site, to production on Vercel (the owner runs this).
#
#   tools/deploy_both.sh
#   TWIN_REPO=/path/to/Digital_Twin tools/deploy_both.sh
#
# The twin (private repo BrendanJamesLynskey/Digital_Twin, Vercel project brendan-lynskey-twin) goes first, so
# that when this site's /twin rewrite goes live it has something to point at. Each step deploys its own
# origin/main and checks the live pages; both scripts are safe to run again.
set -euo pipefail

repo=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
twin=${TWIN_REPO:-$(dirname "$repo")/Digital_Twin}
[ -x "$twin/tools/deploy_twin.sh" ] || {
  echo "Digital Twin repo not found at $twin (clone BrendanJamesLynskey/Digital_Twin there, or set TWIN_REPO)" >&2
  exit 1
}

echo "######## 1/2 Digital Twin ($twin)"
"$twin/tools/deploy_twin.sh"
echo
echo "######## 2/2 landing site ($repo)"
"$repo/tools/deploy_vercel.sh"
