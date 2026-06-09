# Medical Store Invoicing System - Setup Instructions

## 📋 Table of Contents

1. [Development Setup](#development-setup)
2. [Building the .exe Installer](#building-the-exe-installer)
3. [Installation Guide](#installation-guide)
4. [Troubleshooting](#troubleshooting)

---

## 🔧 Development Setup

### Prerequisites

- **Python 3.8 or higher** - Download from https://www.python.org/downloads/
- **Git** (optional) - For cloning the repository
- **Visual C++ Build Tools** (for Windows) - Required by some Python packages

### Step 1: Clone the Repository

```bash
git clone https://github.com/shehriyarkhan6930-cpu/medical-store-invoicing.git
cd medical-store-invoicing
```

### Step 2: Create Virtual Environment

Create an isolated Python environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app/main.py
```

The application will be available at `http://localhost:5000`

**Default Login Credentials:**
- Username: `admin`
- Password: `admin`

---

## 📦 Building the .exe Installer

### Prerequisites for Building

1. **PyInstaller** - Already included in requirements.txt
2. **NSIS** (Nullsoft Scriptable Install System) - For creating the installer
   - Download from: https://nsis.sourceforge.io/
   - Install to default location: `C:\Program Files (x86)\NSIS`

### Step 1: Prepare the Build

```bash
# Make sure you're in the project root directory
cd medical-store-invoicing

# Activate virtual environment
venv\Scripts\activate
```

### Step 2: Create Application Icon (Optional)

Create a 256x256 PNG icon and convert it to ICO format:

```bash
pip install pillow
```

Then save your icon as `app/static/icon.ico`

### Step 3: Build the Executable

```bash
python build_exe.py
```

This will:
- Clean previous builds
- Build the executable with PyInstaller
- Create the installer if NSIS is installed
- Generate output files in `dist/` directory

### Step 4: Output Files

After successful build, you'll have:

```
dist/
├── MedicalStoreInvoicing.exe          # Standalone executable
└── MedicalStoreInvoicing-Setup.exe    # Installer (if NSIS installed)
```

---

## 💻 Installation Guide

### For End Users (Using the Installer)

#### On Windows:

1. **Download** `MedicalStoreInvoicing-Setup.exe`
2. **Double-click** the installer
3. **Follow** the installation wizard:
   - Click "Next" to proceed
   - Choose installation directory (default: `C:\Program Files\MedicalStoreInvoicing`)
   - Click "Install"
   - Finish
4. **Launch** the application from:
   - Desktop shortcut, OR
   - Start Menu → Medical Store Invoicing

#### System Requirements:
- Windows 7 or higher
- 2 GB RAM minimum
- 500 MB disk space
- Display: 1024x768 or higher

### For Developers (Development Installation)

See [Development Setup](#development-setup) section above.

---

## 🐛 Troubleshooting

### Issue: "Python not found"

**Solution:**
- Install Python from https://www.python.org/downloads/
- Make sure "Add Python to PATH" is checked during installation
- Verify installation: `python --version`

### Issue: "pip install" fails

**Solutions:**
- Upgrade pip: `python -m pip install --upgrade pip`
- Try using pip3: `pip3 install -r requirements.txt`
- Check internet connection
- Use a VPN if pip repository is blocked

### Issue: "No module named 'flask'"

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Issue: "Application won't start after installation"

**Solutions:**
- Check Windows Defender/Antivirus settings (they may block the .exe)
- Add the application to antivirus whitelist
- Run as Administrator
- Check disk space availability

### Issue: "Database error" or "Cannot create database"

**Solutions:**
- Ensure AppData folder has write permissions
- Run application as Administrator
- Delete `medical_store.db` file and restart (creates fresh database)
- Check available disk space

### Issue: "PyInstaller fails to build executable"

**Solutions:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Try rebuilding: `python build_exe.py`
- Check console output for specific error messages

### Issue: "Installer creation fails (NSIS error)"

**Solutions:**
- Ensure NSIS is installed from https://nsis.sourceforge.io/
- Reinstall NSIS if it's corrupted
- The executable will still be created even if installer fails
- You can distribute `dist/MedicalStoreInvoicing.exe` directly

### Issue: "Port 5000 already in use"

**Solution:**
- The application uses port 5000 by default
- Close other applications using this port, OR
- Edit `app/main.py` and change port number:
  ```python
  app.run(port=5001)  # Use 5001 instead
  ```

### Issue: "Login fails with admin/admin"

**Solution:**
- Delete the database file: `medical_store.db`
- Restart the application (will create fresh database with default admin user)

---

## 📝 Configuration

### Company Details

Edit `app/config.py` to customize company information:

```python
COMPANY_NAME = 'Your Medical Store Name'
COMPANY_ADDRESS = 'Your Address'
COMPANY_PHONE = 'Your Phone'
COMPANY_EMAIL = 'Your Email'
COMPANY_GST = 'Your GST Number'
```

### Database Location

- **Development**: `medical_store.db` (in project root)
- **Production**: `C:\Users\{Username}\AppData\Local\MedicalStore\database.db`

### Change Default Password

1. Login with `admin/admin`
2. Go to Settings → Change Password
3. Enter new password and save

---

## 📚 Additional Resources

- **Python Documentation**: https://docs.python.org/3/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Documentation**: https://www.sqlalchemy.org/
- **PyInstaller Guide**: https://pyinstaller.readthedocs.io/
- **NSIS Documentation**: https://nsis.sourceforge.io/Docs/

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review application logs
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Operating system version
   - Python version

---

**Last Updated**: June 2024
