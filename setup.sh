#!/bin/bash

DOWNLOADS_DIR="downloads"
if [ ! -d "$DOWNLOADS_DIR" ]; then
  echo "📁 Creating $DOWNLOADS_DIR (stores downloaded music files)"
  mkdir -p "$DOWNLOADS_DIR"
fi
chmod 777 "$DOWNLOADS_DIR"

echo "✅ Setup complete!"
