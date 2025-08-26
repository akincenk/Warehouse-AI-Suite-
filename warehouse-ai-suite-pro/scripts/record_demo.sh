#!/usr/bin/env bash
# Terminal demo recording using asciinema (install: brew install asciinema)
set -euo pipefail

# Record demo; press Ctrl-D to finish
asciinema rec -c "./scripts/demo.sh" docs/demo.cast

echo "Recorded to docs/demo.cast"
echo "Convert to GIF (optional):"
echo "  npm install -g asciinema-agg && agg docs/demo.cast docs/demo.gif"
