#!/bin/bash

DOWNLOADS_DIR="downloads"

echo "📂 Flattening downloads folder..."

# Find all audio files in subdirectories
find "$DOWNLOADS_DIR" -mindepth 2 -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.ogg" -o -iname "*.m4a" \) | while read -r file; do
    filename=$(basename "$file")
    dest="$DOWNLOADS_DIR/$filename"
    
    # Handle filename collisions
    if [ -f "$dest" ]; then
        name="${filename%.*}"
        ext="${filename##*.}"
        counter=1
        while [ -f "$DOWNLOADS_DIR/${name}_${counter}.${ext}" ]; do
            ((counter++))
        done
        dest="$DOWNLOADS_DIR/${name}_${counter}.${ext}"
        echo "  ⚠️ Collision: $filename -> $(basename "$dest")"
    fi
    
    mv "$file" "$dest"
    echo "  ✅ Moved: $(basename "$file")"
done

# Remove empty directories
find "$DOWNLOADS_DIR" -mindepth 1 -type d -empty -delete 2>/dev/null

echo "✅ Flattening complete!"
