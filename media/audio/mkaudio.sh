#!/bin/zsh

for f in *; do
  # Skip files starting with "new-"
  [[ "$f" == new-* ]] && continue

  # Skip if new version already exists
  [[ -f "new-$f" ]] && {
    echo "removing '$f' — new version exists"
    rm "$f"
    continue
  }

  # Run ffmpeg normalization
  echo "Processing '$f'..."
  ffmpeg -i "$f" -af loudnorm "new-$f"

  # Remove original if conversion succeeded
  if [[ -f "new-$f" ]]; then
    echo "Removing original '$f'"
    rm "$f"
  else
    echo "❌ Failed to create 'new-$f' — original retained"
  fi
done
