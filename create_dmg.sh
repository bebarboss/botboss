#!/bin/bash

echo "📦 Creating DMG installer..."

APP_NAME="BOTBOSS"
DMG_NAME="${APP_NAME}.dmg"
VOLUME_NAME="${APP_NAME}"

# ตรวจสอบว่ามี .app อยู่ไหม
if [ ! -d "dist/BOTBOSS.app" ]; then
    echo "❌ BOTBOSS.app not found. Please build first: ./build_mac.sh"
    exit 1
fi

# ลบ DMG เก่า
rm -f "dist/${DMG_NAME}"

# สร้าง temporary folder
TMP_DIR=$(mktemp -d)
cp -R "dist/BOTBOSS.app" "${TMP_DIR}/${APP_NAME}.app"

# สร้าง symlink ไปที่ Applications
ln -s /Applications "${TMP_DIR}/Applications"

# สร้าง DMG
echo "Creating DMG..."
hdiutil create -volname "${VOLUME_NAME}" \
    -srcfolder "${TMP_DIR}" \
    -ov -format UDZO \
    "dist/${DMG_NAME}"

# ลบ temp folder
rm -rf "${TMP_DIR}"

if [ -f "dist/${DMG_NAME}" ]; then
    echo "✅ DMG created successfully!"
    echo "📁 Location: dist/${DMG_NAME}"
else
    echo "❌ DMG creation failed!"
    exit 1
fi
