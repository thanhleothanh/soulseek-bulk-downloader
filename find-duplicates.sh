#!/bin/bash

DOWNLOADS_DIR="downloads"
OUTPUT_FILE="duplicate-durations.txt"
TMP_FILE="/tmp/durations.tmp"
COUNTS_FILE="/tmp/counts.tmp"

if ! command -v ffprobe &> /dev/null; then
  echo "❌ ffprobe is not installed. Please install ffmpeg first."
  exit 1
fi

echo "🔍 Scanning music files in $DOWNLOADS_DIR..."

> "$TMP_FILE"

find "$DOWNLOADS_DIR" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.m4a" -o -iname "*.wav" -o -iname "*.ogg" \) | while read -r file; do
  duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file" 2>/dev/null)
  if [ -n "$duration" ]; then
    rounded=$(printf "%.0f" "$duration")
    echo "$rounded $file" >> "$TMP_FILE"
  fi
done

echo "📝 Writing results to $OUTPUT_FILE..."

> "$OUTPUT_FILE"

cut -d' ' -f1 "$TMP_FILE" | sort | uniq -c | sort -rn > "$COUNTS_FILE"

total=$(awk '$1 >= 2' "$COUNTS_FILE" | wc -l)

if [ "$total" -eq 0 ]; then
  echo "✅ No duplicates found!"
else
  while read -r count duration; do
    if [ "$count" -ge 2 ]; then
      echo "=== Duration: ${duration}s ($count files) ===" >> "$OUTPUT_FILE"
      grep "^${duration} " "$TMP_FILE" | cut -d' ' -f2- >> "$OUTPUT_FILE"
      echo "" >> "$OUTPUT_FILE"
    fi
  done < "$COUNTS_FILE"

  echo "📋 Found $total potential duplicate groups. Check $OUTPUT_FILE"
fi

rm -f "$TMP_FILE" "$COUNTS_FILE"
