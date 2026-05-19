#!/bin/bash

echo "🛑 Stopping containers..."
docker compose down --remove-orphans

echo "🗑️ Cleaning downloads folder..."
rm -rf downloads/*

echo "✅ Cleanup complete!"
