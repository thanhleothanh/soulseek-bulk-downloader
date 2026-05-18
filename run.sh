#!/bin/bash

echo "🛑 Stopping containers..."
docker compose down

echo "🔨 Rebuilding downloader (clearing cache)..."
docker compose build --no-cache downloader

echo "🚀 Starting services..."
docker compose up -d

echo "📋 Showing downloader logs..."
docker logs -f soulseek-bulk-downloader
