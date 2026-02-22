# 🎫 BOTBOSS

A Python-based automatic ticket clicking bot with a beautiful GUI interface. Built with Selenium and PyQt6 for easy automation without terminal commands.

<img width="537" alt="BOTBOSS GUI" src="https://github.com/user-attachments/assets/2467cb5b-d36f-4380-89bc-bbefb4d24dbd" />

---

## ✨ Features

- 🎯 **Automatic Ticket Clicking** - Schedule-based automation
- 🖥️ **User-Friendly GUI** - Built with PyQt6, no terminal needed
- 🌐 **Chrome Integration** - Uses Chrome debug mode for control
- ⏰ **Smart Scheduling** - Click at specific times
- 🎮 **Start/Stop Control** - Full control from the interface
- 🔧 **Configurable** - Support multiple websites and buttons

---

## 📥 Download & Installation

### For Users (macOS)

#### Option 1: DMG Installer (Recommended)
1. Download `BOTBOSS.dmg` from [Releases](https://github.com/bebarboss/botboss/releases)
2. Open the DMG file
3. Drag **BOTBOSS** to **Applications** folder
4. Right-click the app → **Open** (first time only)

#### Option 2: ZIP Archive
1. Download `BOTBOSS-macOS.zip` from [Releases](https://github.com/bebarboss/botboss/releases)
2. Extract the zip file
3. Move `BOTBOSS.app` to **Applications** folder
4. Right-click the app → **Open** (first time only)

### Requirements
- macOS 11 (Big Sur) or later
- Apple Silicon (M1/M2/M3) or Intel
- **Google Chrome** must be installed

### First Launch Security Warning

If you see: *"BOTBOSS cannot be opened because it is from an unidentified developer"*

**Solution:**
1. Right-click (or Control+click) on the app
2. Select **"Open"**
3. Click **"Open"** again in the dialog
4. Done! (you only need to do this once)

---

## 🚀 Usage

1. **Launch BOTBOSS** from Applications
2. **Enter URL** of the ticket website
3. **Click "Connect"** to open Chrome in debug mode
4. **Set schedule** for automatic clicking
5. **Start** the bot and let it work!

<img width="1912" alt="BOTBOSS in action" src="https://github.com/user-attachments/assets/3dcb8a8c-0379-4893-a227-4e74cd4a8f32" />

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.10+
- Google Chrome
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/bebarboss/botboss.git
cd botboss

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Project Structure

```
botboss/
├── main.py              # Main GUI application
├── selenium_func.py     # Selenium automation logic
├── chrome.py           # Chrome browser control
├── requirements.txt    # Python dependencies
├── main.spec          # PyInstaller configuration
├── build_mac.sh       # macOS build script
├── create_dmg.sh      # DMG creator script
└── README.md          # This file
```

### Dependencies

- **selenium** - Browser automation
- **PyQt6** - GUI framework
- **pyinstaller** - App bundling

---

## 📦 Building from Source

### macOS

```bash
# Make scripts executable
chmod +x build_mac.sh create_dmg.sh

# Build .app bundle
./build_mac.sh

# Create DMG installer (optional)
./create_dmg.sh

# Output will be in dist/
```

### Windows

```bash
# Build executable
pyinstaller main.spec

# Output will be in dist/
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Please use responsibly and respect the terms of service of any websites you interact with.

---

## 🐛 Issues & Support

Found a bug or have a feature request? Please [open an issue](https://github.com/bebarboss/botboss/issues).

---

## 🙏 Acknowledgments

- Built with Python, Selenium, and PyQt6
- Inspired by the need for accessible automation tools
- Thanks to all contributors!

---

**Made with ❤️ by bebarboss**

