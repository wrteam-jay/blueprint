#!/usr/bin/env bash
#
# Validate all Mermaid diagrams in markdown files.
#
# Usage:
#   ./scripts/validate-diagrams.sh [path]
#
# Examples:
#   ./scripts/validate-diagrams.sh orders.blueprint/
#   ./scripts/validate-diagrams.sh orders.blueprint/scenarios/order-placement.md
#   ./scripts/validate-diagrams.sh .   # validate everything in current directory
#
# Requires: @mermaid-js/mermaid-cli (mmdc)
#   npm install -g @mermaid-js/mermaid-cli
#
# Exit codes:
#   0 — all diagrams valid
#   1 — one or more diagrams have syntax errors
#   2 — mmdc not installed

set -euo pipefail

if ! command -v mmdc &>/dev/null; then
  echo "Error: mmdc not found. Install it with:"
  echo "  npm install -g @mermaid-js/mermaid-cli"
  exit 2
fi

target="${1:-.}"
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

total=0
failed=0
fileidx=0

# Find all markdown files
if [ -f "$target" ]; then
  mdfiles=("$target")
else
  mdfiles=()
  while IFS= read -r f; do
    mdfiles+=("$f")
  done < <(find "$target" -name '*.md' -not -path '*/.git/*' -not -path '*/node_modules/*' | sort)
fi

for mdfile in "${mdfiles[@]}"; do
  fileidx=$((fileidx + 1))
  # Extract mermaid blocks: write each to a separate file, track line numbers
  # Use fileidx prefix to avoid collisions across files
  awk -v tmpdir="$tmpdir" -v src="$mdfile" -v fid="$fileidx" '
    /^```mermaid/ {
      inside = 1
      start = NR
      idx++
      outfile = tmpdir "/block_" fid "_" idx ".mmd"
      metafile = tmpdir "/block_" fid "_" idx ".meta"
      print src ":" start > metafile
      next
    }
    /^```/ && inside {
      inside = 0
      next
    }
    inside {
      print >> outfile
    }
  ' "$mdfile"
done

# Now validate each extracted block
for metafile in "$tmpdir"/block_*.meta 2>/dev/null; do
  [ -f "$metafile" ] || continue
  total=$((total + 1))

  idx="${metafile%.meta}"
  idx="${idx##*/}"
  mmdfile="$tmpdir/${idx}.mmd"
  location=$(cat "$metafile")
  outfile="$tmpdir/${idx}.svg"

  if [ ! -f "$mmdfile" ]; then
    echo ""
    echo "FAIL: $location — empty mermaid block"
    failed=$((failed + 1))
    continue
  fi

  if ! mmdc -i "$mmdfile" -o "$outfile" --quiet 2>"$tmpdir/err.log"; then
    failed=$((failed + 1))
    echo ""
    echo "FAIL: $location"
    head -3 "$mmdfile" | sed 's/^/  | /'
    if [ "$(wc -l < "$mmdfile" | tr -d ' ')" -gt 3 ]; then
      echo "  | ..."
    fi
    # Extract the meaningful error line (skip stack trace)
    (grep -m1 'Error\|Parse error\|Syntax error\|Unknown' "$tmpdir/err.log" 2>/dev/null || sed -n '1p' "$tmpdir/err.log") | sed 's/^/  Error: /'
  fi
done

echo ""
echo "---"
echo "Diagrams checked: $total"
echo "Passed: $((total - failed))"
if [ "$failed" -gt 0 ]; then
  echo "Failed: $failed"
  exit 1
else
  echo "All diagrams valid."
  exit 0
fi
