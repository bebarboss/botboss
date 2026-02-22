#!/bin/bash

echo "🚀 Building BOTBOSS for macOS..."

# ตรวจสอบว่ามี dependencies ครบไหม
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python first."
    exit 1
fi

# ใช้ virtual environment ถ้ามี
if [ -d ".venv" ]; then
    echo "📦 Using virtual environment..."
    source .venv/bin/activate
else
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# ลบโฟลเดอร์เก่า
echo "🧹 Cleaning old build..."
rm -rf build dist

# Build .app
echo "🔨 Building application..."
python3 -m PyInstaller main.spec

# ตรวจสอบว่า build สำเร็จหรือไม่
if [ -d "dist/main.app" ]; then
    echo "✅ Build successful!"
    echo "📁 Application location: dist/main.app"
    echo ""
    echo "To run: open dist/main.app"
    echo "To create DMG: ./create_dmg.sh"
else
    echo "❌ Build failed!"
    exit 1
fi
