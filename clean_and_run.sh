#!/bin/bash
# Complete cache cleanup and run Automap

echo "🧹 Cleaning Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

echo "✅ Cache cleaned"
echo "🚀 Running Automap..."
python main.py
