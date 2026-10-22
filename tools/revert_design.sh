#!/usr/bin/env bash
# Put the previous ("classic") design back on https://brendan-lynskey.vercel.app (the owner runs this).
#
#   tools/revert_design.sh
#
# Deploys the git tag design-classic (the site as it was before the Datasheet redesign, with PR #8's "software"
# headline) through tools/deploy_vercel.sh, which archives that tag and checks the live pages. It changes nothing
# in git: main still holds the datasheet design, so the next plain tools/deploy_vercel.sh would bring it back. To
# make the revert permanent, revert the Datasheet merge commit on main (git revert -m 1 <merge>) and deploy main.
set -euo pipefail
exec "$(dirname "$0")/deploy_vercel.sh" design-classic
