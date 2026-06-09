# Medical Store Invoicing System

A complete offline desktop application for managing medical store invoicing, inventory, and customer records with an installable Windows .exe.

## 🎯 Features

- **Invoice Management**: Generate, print, and manage invoices
- **Inventory Tracking**: Track medicines, supplies, and product stock
- **Customer Management**: Maintain customer details and purchase history
- **Sales Reports**: Generate detailed sales and revenue reports
- **Offline Functionality**: Works completely offline with SQLite database
- **User Authentication**: Secure login system
- **PDF Export**: Print and export invoices as PDF
- **Database Backup/Restore**: Automatic and manual backups
- **Search & Filter**: Quickly find products and invoices
- **Discount Management**: Apply discounts and manage pricing

## 🖥️ System Requirements

- **OS**: Windows 7 or higher
- **RAM**: 2 GB minimum
- **Storage**: 500 MB free space
- **Display**: 1024x768 minimum resolution

## 📦 Installation

1. Download `MedicalStoreInvoicing-Setup.exe`
2. Run the installer
3. Follow the installation wizard
4. Launch the application from Desktop shortcut or Start menu

## 🚀 Quick Start

1. **Login**: Use default credentials (admin/admin) on first run
2. **Add Products**: Go to Inventory → Add Medicine
3. **Create Invoice**: Click "New Invoice" → Add items → Save
4. **View Reports**: Check Sales Reports for analytics

## 📂 Project Structure

```
medical-store-invoicing/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── invoices.html
│       ├── inventory.html
│       ├── customers.html
│       └── reports.html
├── requirements.txt
├── setup.py
├── build_exe.py
└── installer.nsi
```

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone repository
git clone https://github.com/shehriyarkhan6930-cpu/medical-store-invoicing.git
cd medical-store-invoicing

# Create virtual environment
python -m venv venv
Source venv\\Scripts\\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app/main.py
```

## 📦 Building the .exe Installer

### Step 1: Install Build Dependencies
```bash
pip install pyinstaller
```

### Step 2: Build Executable
```bash
python build_exe.py
```

### Step 3: Create Installer
The build script automatically creates the Windows installer.

### Output
- Executable: `dist/MedicalStoreInvoicing.exe`
- Installer: `dist/MedicalStoreInvoicing-Setup.exe`

## 🗄️ Database

The application uses SQLite3 for offline data storage.

## 📝 Default Login Credentials

**First Run:**
- Username: `admin`
- Password: `admin`

⚠️ **Important**: Change the default password after first login!

## 📄 License

This project is provided as-is for medical store management purposes.

---

**Last Updated**: June 2026