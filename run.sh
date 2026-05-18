#!/bin/bash

echo "🛑 Stopping containers..."
docker compose down

echo "🔨 Rebuilding downloader (clearing cache)..."
docker compose build --no-cache downloader

echo "🚀 Starting services..."
docker compose up -d

echo "📋 Showing downloader logs (waiting for completion)..."
docker logs -f soulseek-bulk-downloader

echo ""
echo "💾 Saving logs to logs/soulseek-bulk-downloader-$(date +%Y%m%d_%H%M%S).log..."
mkdir -p logs
docker logs soulseek-bulk-downloader > "logs/soulseek-bulk-downloader-$(date +%Y%m%d_%H%M%S).log" 2>&1
echo "✅ Log saved!"
