# 🚀 Build Standalone EXE Installer

This guide explains how to create a standalone `.exe` installer that can be distributed to users without requiring Python installation.

## 📋 Prerequisites

Before building the EXE, ensure you have:

1. **Python 3.8+** installed and working
2. **Virtual environment activated** with all dependencies installed
3. **NSIS** (Nullsoft Scriptable Install System) - for creating the installer

---

## 📥 Step 1: Install NSIS

### Download NSIS:

1. Go to https://nsis.sourceforge.io/Download
2. Click **"Download"** (latest version, e.g., nsis-3.09-setup.exe)
3. Run the installer
4. Choose **"Add NSIS to system PATH"** (recommended)
5. Click **Install**
6. Click **Finish**

### Verify NSIS Installation:

1. Open Command Prompt
2. Type: `makensis -VERSION`
3. Press Enter
4. Should display NSIS version

If it says "command not found", restart your computer.

---

## 📦 Step 2: Prepare Your Project

### Activate Virtual Environment:

```bash
cd C:\path\to\medical-store-invoicing
venv\Scripts\activate
```

### Ensure All Dependencies are Installed:

```bash
pip install -r requirements.txt
```

### Verify PyInstaller:

```bash
pip install --upgrade pyinstaller
pyinstaller --version
```

---

## 🎨 Step 3: Create Application Icon (Optional)

A nice icon makes your EXE look professional.

### Create Icon:

1. Find or create a 256×256 PNG image
2. Save it as `app/static/icon.png`
3. Convert it to ICO format using:
   - Online tool: https://convertio.co/png-ico/
   - Or ImageMagick: `magick convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico`
4. Save as `app/static/icon.ico`

---

## 🔨 Step 4: Build the Executable

### Run Build Script:

1. Open Command Prompt in project folder
2. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
3. Run build script:
   ```bash
   python build_exe.py
   ```
4. Wait for build to complete (5-15 minutes)

### Build Output:

You'll see output like:
```
============================================================
Building MedicalStoreInvoicing v1.0.0
============================================================
Cleaning previous builds...
Building MedicalStoreInvoicing executable...
✓ Executable built successfully!
Creating installer...
✓ Installer created successfully!

============================================================
Build completed!
Executable: dist/MedicalStoreInvoicing.exe
Installer: dist/MedicalStoreInvoicing-Setup.exe
============================================================
```

---

## 📂 Step 5: Locate Your Files

After successful build, you'll find:

```
dist/
├── MedicalStoreInvoicing.exe          (Standalone executable)
└── MedicalStoreInvoicing-Setup.exe    (Installer)
```

### Files Size:

- **MedicalStoreInvoicing.exe**: ~200-300 MB
- **MedicalStoreInvoicing-Setup.exe**: ~250-350 MB

---

## ✅ Step 6: Test Your EXE

### Test Standalone EXE:

1. Double-click `dist/MedicalStoreInvoicing.exe`
2. Application should launch
3. Test all features
4. Close application

### Test Installer:

1. Copy `dist/MedicalStoreInvoicing-Setup.exe` to another folder
2. Double-click it
3. Follow installation wizard
4. Choose installation location
5. Click "Install"
6. Launch from Desktop shortcut or Start Menu
7. Verify application works correctly

---

## 🚀 Step 7: Distribution

### Option A: Direct EXE Distribution

**Best for:** Small teams, testing

1. Share `dist/MedicalStoreInvoicing.exe` via:
   - Email
   - File sharing (Google Drive, Dropbox, WeTransfer)
   - USB drive
   - Network folder

**Pros:**
- Single file
- No installation needed
- Works immediately

**Cons:**
- Larger file size
- No start menu shortcut
- No uninstall option

### Option B: Installer Distribution

**Best for:** Professional deployment, end users

1. Share `dist/MedicalStoreInvoicing-Setup.exe` via:
   - Website download
   - Email (compressed)
   - USB drive
   - Network deployment

**Pros:**
- Proper installation experience
- Desktop and start menu shortcuts
- Uninstall option
- Professional appearance

**Cons:**
- Requires user to run installer
- Slightly larger

---

## ⚙️ Customization Options

### Edit build_exe.py to Customize:

1. Open `build_exe.py` in text editor
2. Modify:

```python
APP_NAME = "MedicalStoreInvoicing"     # Your app name
APP_VERSION = "1.0.0"                  # Version number
OUTPUT_DIR = "dist"                    # Output folder
```

### Customize Installer:

1. Edit `installer.nsi` generated during build
2. Change:
   - Company name
   - Installation path
   - Shortcuts location
   - License text
3. Rebuild using:
   ```bash
   makensis installer.nsi
   ```

---

## 🐛 Troubleshooting Build Issues

### Issue: "PyInstaller not found"

**Solution:**
```bash
pip install pyinstaller
```

### Issue: "NSIS not found"

**Solution:**
1. Reinstall NSIS from https://nsis.sourceforge.io/
2. Add NSIS to PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings
   - Environment variables
   - Add `C:\Program Files (x86)\NSIS` to PATH
3. Restart computer

### Issue: "Build takes very long"

**Solution:**
- Normal for first build (can take 15+ minutes)
- Subsequent builds are faster
- Close other applications to free resources

### Issue: "Executable doesn't run"

**Solution:**
1. Check if Python dependencies are complete:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
2. Rebuild:
   ```bash
   python build_exe.py
   ```
3. Test from project folder:
   ```bash
   python app/main.py
   ```

---

## 🔒 Antivirus & Windows Defender

Windows Defender or antivirus may flag your EXE as suspicious (false positive).

### To Whitelist:

1. **Windows Defender:**
   - Open Windows Defender
   - Virus & threat protection
   - Manage settings
   - Add exclusions
   - Add your application folder

2. **Other Antivirus:**
   - Open antivirus software
   - Settings → Exceptions/Whitelist
   - Add `MedicalStoreInvoicing.exe`

3. **For Users:**
   - Inform users it's a false positive
   - They can click "More info" → "Run anyway" in Windows

---

## 📊 Version Updates

### To Build New Version:

1. Make code changes
2. Update version in `build_exe.py`:
   ```python
   APP_VERSION = "1.1.0"  # New version
   ```
3. Run build again:
   ```bash
   python build_exe.py
   ```
4. New EXE will be created in `dist/`

---

## 📋 Release Checklist

Before distributing, verify:

- [ ] Application runs without errors
- [ ] Login works with default credentials
- [ ] Can create invoices
- [ ] Can add products
- [ ] Can add customers
- [ ] Can view reports
- [ ] PDF export works
- [ ] Database backup works
- [ ] No Python installation required on target PC
- [ ] Windows Defender white-listed (optional)
- [ ] Icon looks good
- [ ] Version number correct

---

## 🎉 Success!

Your EXE installer is ready to distribute!

### Next Steps:

1. Test on clean PC without Python
2. Get feedback from users
3. Make improvements
4. Release new versions

---

## 📞 Support

If users have issues:

1. Direct them to `QUICK_START_GUIDE.md`
2. Provide System Requirements
3. Help with installation
4. Troubleshoot issues

---

**Happy distributing!** 🚀
