#!/usr/bin/env bash
# Regenerates servers.json from Lunar Client's public ServerMappings repo.
# Run this occasionally (weekly/monthly) to pick up new/removed servers,
# then commit + push servers.json - GitHub Pages serves the new version
# automatically within a minute or two.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf .src
git clone --depth 1 https://github.com/LunarClient/ServerMappings.git .src
python3 aggregate.py .src servers.json
rm -rf .src
echo "Done. Review the diff, then: git add servers.json && git commit -m 'Refresh server list' && git push"
