#!/bin/bash

# Create required folders for Docker volume mounts if they don't exist
# These folders are mounted into the containers, so they must exist on the host

DOWNLOADS_DIR="downloads"
if [ ! -d "$DOWNLOADS_DIR" ]; then
  echo "📁 Creating $DOWNLOADS_DIR (stores downloaded music files)"
  mkdir -p "$DOWNLOADS_DIR"
fi
chmod 777 "$DOWNLOADS_DIR"

SLSKD_DATA_DIR="slskd-data"
if [ ! -d "$SLSKD_DATA_DIR" ]; then
  echo "📁 Creating $SLSKD_DATA_DIR (stores slskd account data and settings)"
  mkdir -p "$SLSKD_DATA_DIR"
fi
chmod 777 "$SLSKD_DATA_DIR"

echo "✅ Setup complete!"
