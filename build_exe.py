#!/usr/bin/env python
"""
Build script for creating Windows .exe installer using PyInstaller
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "MedicalStoreInvoicing"
APP_VERSION = "1.0.0"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"

def clean_build_directories():
    """Remove previous build files"""
    print("Cleaning previous builds...")
    for directory in [OUTPUT_DIR, BUILD_DIR, f"{APP_NAME}.spec"]:
        if os.path.exists(directory):
            if os.path.isdir(directory):
                shutil.rmtree(directory)
            else:
                os.remove(directory)
            print(f"  Removed {directory}")

def build_executable():
    """Build executable using PyInstaller"""
    print(f"\nBuilding {APP_NAME} executable...")
    
    pyinstaller_cmd = [
        'pyinstaller',
        '--name', APP_NAME,
        '--onefile',
        '--windowed',
        '--icon', 'app/static/icon.ico' if os.path.exists('app/static/icon.ico') else None,
        '--add-data', 'app/templates:app/templates',
        '--add-data', 'app/static:app/static',
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=flask_login',
        '--collect-all=flask',
        '--collect-all=flask_sqlalchemy',
        '--collect-all=flask_login',
        '--distpath', OUTPUT_DIR,
        '--buildpath', BUILD_DIR,
        '--specpath', '.',
        'app/main.py'
    ]
    
    # Remove None values
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd is not None]
    
    try:
        result = subprocess.run(pyinstaller_cmd, check=True)
        if result.returncode == 0:
            print("✓ Executable built successfully!")
            return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error building executable: {e}")
        return False
    except FileNotFoundError:
        print("✗ PyInstaller not found. Install with: pip install pyinstaller")
        return False

def create_installer():
    """Create Windows installer using NSIS"""
    print(f"\nCreating installer...")
    
    nsis_script = f"""
; NSIS Installer Script for {APP_NAME}

!include "MUI2.nsh"

Name "{APP_NAME} v{APP_VERSION}"
OutFile "dist/{APP_NAME}-Setup.exe"
InstallDir "$PROGRAMFILES\\{APP_NAME}"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "dist\\{APP_NAME}\\*.*"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\{APP_NAME}"
    CreateShortCut "$SMPROGRAMS\\{APP_NAME}\\{APP_NAME}.lnk" "$INSTDIR\\{APP_NAME}.exe"
    CreateShortCut "$DESKTOP\\{APP_NAME}.lnk" "$INSTDIR\\{APP_NAME}.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\\{APP_NAME}"
    Delete "$DESKTOP\\{APP_NAME}.lnk"
SectionEnd
    """
    
    # Save NSIS script
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    # Check if NSIS is installed
    nsis_path = "C:\\Program Files (x86)\\NSIS\\makensis.exe"
    if os.path.exists(nsis_path):
        try:
            subprocess.run([nsis_path, 'installer.nsi'], check=True)
            print("✓ Installer created successfully!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Error creating installer with NSIS")
            return False
    else:
        print("⚠ NSIS not found. Installer script saved as 'installer.nsi'")
        print("  Download NSIS from: https://nsis.sourceforge.io/")
        print("  Then run: makensis installer.nsi")
        return False

def main():
    print("="*60)
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        return False
    
    # Clean previous builds
    clean_build_directories()
    
    # Build executable
    if not build_executable():
        print("\n✗ Build failed!")
        return False
    
    # Create installer
    create_installer()
    
    print("\n" + "="*60)
    print("Build completed!")
    print(f"Executable: dist/{APP_NAME}.exe")
    print(f"Installer: dist/{APP_NAME}-Setup.exe (if NSIS is installed)")
    print("="*60)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
