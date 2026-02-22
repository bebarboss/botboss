# 🚀 การ Deploy BOTBOSS บน macOS

## วิธีที่ 1: Build แอป macOS (.app)

### ขั้นตอน:

1. **เตรียมสภาพแวดล้อม**
```bash
pip3 install -r requirements.txt
```

2. **Build แอป**
```bash
chmod +x build_mac.sh
./build_mac.sh
```

3. **ทดสอบแอป**
```bash
open dist/main.app
```

4. **สร้าง DMG installer (optional)**
```bash
chmod +x create_dmg.sh
./create_dmg.sh
```

---

## วิธีที่ 2: แชร์ให้คนอื่นใช้

### A. แชร์ .app ไฟล์เดียว

1. Zip ไฟล์:
```bash
cd dist
zip -r BOTBOSS.zip main.app
```

2. อัปโหลดไปที่:
   - **GitHub Releases** (แนะนำ)
   - **Google Drive / Dropbox**
   - **WeTransfer**

3. ผู้ใช้ดาวน์โหลด → แตกไฟล์ → ลาก `main.app` ไปที่ `/Applications`

### B. แชร์ DMG installer (สวยงามกว่า)

1. สร้าง DMG:
```bash
./create_dmg.sh
```

2. แชร์ไฟล์ `dist/BOTBOSS.dmg`

3. ผู้ใช้:
   - Double-click DMG
   - ลาก BOTBOSS ไปที่โฟลเดอร์ Applications
   - เสร็จ!

---

## ⚠️ แก้ปัญหา macOS Gatekeeper

เมื่อผู้ใช้เปิดแอปครั้งแรกอาจขึ้นข้อความ *"cannot be opened because it is from an unidentified developer"*

### วิธีแก้สำหรับผู้ใช้:

**วิธีที่ 1: คลิกขวา**
1. คลิกขวาที่แอป
2. เลือก "Open"
3. คลิก "Open" อีกครั้ง

**วิธีที่ 2: ผ่าน Terminal**
```bash
xattr -cr /Applications/BOTBOSS.app
```

**วิธีที่ 3: System Settings**
1. System Settings → Privacy & Security
2. หาข้อความ "BOTBOSS was blocked"
3. คลิก "Open Anyway"

---

## 🔐 Code Signing (สำหรับการแจกจ่ายอย่างเป็นทางการ)

ถ้าต้องการให้ผู้ใช้เปิดได้โดยไม่มีปัญหา ต้อง sign แอป:

1. **ต้องมี Apple Developer Account** ($99/ปี)

2. **Sign แอป:**
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: YOUR_NAME" dist/main.app
```

3. **Notarize (ส่งให้ Apple ตรวจสอบ):**
```bash
xcrun notarytool submit dist/BOTBOSS.dmg --apple-id YOUR_EMAIL --password APP_SPECIFIC_PASSWORD --team-id YOUR_TEAM_ID
```

---

## 📋 Checklist ก่อน Deploy

- [ ] แอปรันได้บน Mac ของคุณ
- [ ] ทดสอบบน Mac เครื่องอื่น (ถ้าทำได้)
- [ ] ตรวจสอบว่าผู้ใช้ต้องติดตั้ง Google Chrome
- [ ] เขียนคู่มือการใช้งานให้ชัดเจน
- [ ] ระบุ macOS version ที่รองรับ (เช่น macOS 11+)

---

## 🎯 แจกจ่ายผ่าน GitHub Releases

1. **สร้าง Release ใหม่**
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **ไปที่ GitHub → Releases → Create new release**

3. **อัปโหลดไฟล์:**
   - `BOTBOSS.dmg` หรือ
   - `BOTBOSS.zip` (ที่มี .app)

4. **เขียน Release notes:**
```markdown
## BOTBOSS v1.0.0

### Requirements
- macOS 11 (Big Sur) or later
- Google Chrome installed

### Installation
1. Download BOTBOSS.dmg
2. Open DMG file
3. Drag BOTBOSS to Applications folder
4. Launch from Applications

### First Launch
If you see security warning:
- Right-click app → Open → Open
```

---

## 💡 Tips

1. **ขนาดไฟล์**: `.app` จะมีขนาดประมาณ 50-150 MB
2. **Universal Binary**: ถ้าต้องการรองรับทั้ง Intel และ Apple Silicon ต้อง build แยก
3. **Updates**: ใช้ GitHub Releases สำหรับ version ใหม่ๆ

---

## 🆘 ติดปัญหา?

- ตรวจสอบว่า Google Chrome ติดตั้งแล้ว
- ลอง run จาก Terminal: `open -a Terminal` แล้ว `./dist/main.app/Contents/MacOS/main` เพื่อดู error
- ตรวจสอบ permissions: `chmod +x dist/main.app/Contents/MacOS/main`
