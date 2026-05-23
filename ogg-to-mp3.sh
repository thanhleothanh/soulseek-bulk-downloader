#!/bin/bash

DOWNLOADS_DIR="downloads"

if ! command -v ffmpeg &> /dev/null; then
  echo "❌ ffmpeg is not installed. Please install it first."
  exit 1
fi

echo "🎵 Converting OGG to MP3 (320kbps) in $DOWNLOADS_DIR..."

find "$DOWNLOADS_DIR" -type f -iname "*.ogg" | while read -r file; do
  mp3="${file%.ogg}.mp3"
  echo "  🔄 Converting: $(basename "$file")"
  ffmpeg -i "$file" -ab 320k -y "$mp3" </dev/null
  if [ $? -eq 0 ]; then
    echo "  ✅ Converted: $(basename "$mp3")"
  else
    echo "  ❌ Failed: $(basename "$file")"
  fi
done

echo "✅ Conversion complete!"
