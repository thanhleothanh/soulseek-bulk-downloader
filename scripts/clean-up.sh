#!/bin/bash

echo "🛑 Stopping containers..."
docker compose down

echo "🗑️ Cleaning downloads folder..."
rm -rf downloads/*

echo "🗑️ Cleaning slskd-data folder..."
rm -rf slskd-data/*

echo "✅ Cleanup complete!"
