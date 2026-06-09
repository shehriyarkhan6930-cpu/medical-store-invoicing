# 🖥️ How to Use Medical Store Invoicing System on Your PC

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Accessing the System](#accessing-the-system)
5. [First Time Setup](#first-time-setup)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

---

## ✅ System Requirements

### Minimum Requirements:
- **Operating System**: Windows 7 or higher (Windows 10/11 recommended)
- **RAM**: 2 GB minimum (4 GB recommended)
- **Disk Space**: 500 MB free
- **Python**: Version 3.8 or higher
- **Internet**: Required only for initial setup (then works offline)

### Check Your Windows Version:
1. Press `Windows Key + R`
2. Type `winver` and press Enter
3. Check the version number

---

## 📥 Installation Steps

### Step 1: Install Python

#### Download Python:
1. Go to https://www.python.org/downloads/
2. Click on **"Download Python 3.11"** (or latest 3.x version)
3. The download will start automatically

#### Install Python:
1. Double-click the downloaded installer (e.g., `python-3.11.exe`)
2. **⚠️ IMPORTANT**: Check the box **"Add Python to PATH"**
3. Click **"Install Now"**
4. Wait for installation to complete (2-3 minutes)
5. Click **"Close"** when done

#### Verify Python Installation:
1. Press `Windows Key + R`
2. Type `cmd` and press Enter (Command Prompt will open)
3. Type: `python --version`
4. Press Enter
5. You should see: `Python 3.x.x`

**If it shows 'python' is not recognized:**
- Reinstall Python and make sure to check "Add Python to PATH"

---

### Step 2: Download the Project

#### Option A: Using Git (Recommended)

1. **Install Git** (if you don't have it):
   - Go to https://git-scm.com/download/win
   - Download and install (use default settings)

2. **Clone the Repository**:
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - Type: `git clone https://github.com/shehriyarkhan6930-cpu/medical-store-invoicing.git`
   - Press Enter
   - Wait for download (1-2 minutes)

#### Option B: Download as ZIP

1. Go to https://github.com/shehriyarkhan6930-cpu/medical-store-invoicing
2. Click **"Code"** (green button)
3. Click **"Download ZIP"**
4. Extract the ZIP file to a folder (e.g., `C:\Users\YourName\Documents\`)
5. Rename the folder to `medical-store-invoicing` (optional)

---

### Step 3: Open Project Folder in Command Prompt

1. Open the folder where you downloaded the project
2. Click on the address bar (where it shows the folder path)
3. Select all text and copy it
4. Press `Windows Key + R`
5. Type `cmd` and press Enter
6. Type: `cd ` (with a space)
7. Right-click and paste the path
8. Press Enter

**Example:**
```
cd C:\Users\YourName\Documents\medical-store-invoicing
```

---

### Step 4: Create Virtual Environment

A virtual environment is like a separate workspace for this project.

1. In Command Prompt, type:
```bash
python -m venv venv
```
2. Press Enter and wait (takes 1-2 minutes)

---

### Step 5: Activate Virtual Environment

1. Type:
```bash
venv\Scripts\activate
```
2. Press Enter
3. You should see `(venv)` before your command prompt

**Example:**
```
(venv) C:\Users\YourName\Documents\medical-store-invoicing>
```

---

### Step 6: Install Dependencies

Now install all required Python libraries:

1. Type:
```bash
pip install -r requirements.txt
```
2. Press Enter
3. Wait for installation (5-10 minutes, depending on internet speed)
4. When done, you'll see: `Successfully installed ...`

---

## ▶️ Running the Application

### Start the Application:

1. Make sure you're in the project folder with virtual environment activated
2. Type:
```bash
python app/main.py
```
3. Press Enter
4. You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## 🌐 Accessing the System

### Open in Web Browser:

1. Open any web browser (Chrome, Edge, Firefox, etc.)
2. Type in the address bar: `http://localhost:5000`
3. Press Enter
4. The login page will appear

### Default Login Credentials:

```
Username: admin
Password: admin
```

---

## 🔧 First Time Setup

### Step 1: Login

1. Enter username: `admin`
2. Enter password: `admin`
3. Click **"Login"**

### Step 2: Change Default Password (IMPORTANT)

1. Click on your username at top-right
2. Select **"Change Password"**
3. Enter:
   - **Old Password**: `admin`
   - **New Password**: (your new password)
   - **Confirm Password**: (repeat your new password)
4. Click **"Update"**
5. Re-login with new password

### Step 3: Update Company Details

1. Click **Settings** (if available in menu)
2. Update:
   - Company Name
   - Address
   - Phone Number
   - Email
   - GST Number
3. Save

---

## 📊 Common Tasks

### Task 1: Add a New Medicine/Product

1. Click **"Inventory"** in menu
2. Click **"Add Product"**
3. Fill in details:
   - **Product Name**: e.g., "Aspirin 500mg"
   - **SKU**: e.g., "ASP-001"
   - **Category**: e.g., "Pain Relief"
   - **Quantity**: e.g., "100"
   - **Cost Price**: e.g., "5.00"
   - **Selling Price**: e.g., "10.00"
   - **Manufacturer**: e.g., "ABC Pharma"
   - **Expiry Date**: e.g., "2025-12-31"
4. Click **"Add Product"**

### Task 2: Add a New Customer

1. Click **"Customers"** in menu
2. Click **"Add Customer"**
3. Fill in details:
   - **Name**: e.g., "John Doe"
   - **Phone**: e.g., "9876543210"
   - **Email**: e.g., "john@example.com"
   - **Address**: e.g., "123 Main Street"
   - **City**: e.g., "Mumbai"
   - **State**: e.g., "Maharashtra"
   - **Pincode**: e.g., "400001"
4. Click **"Add Customer"**

### Task 3: Create an Invoice

1. Click **"Invoices"** in menu
2. Click **"Create Invoice"**
3. Select customer from dropdown
4. Add items:
   - Click **"Add Row"** to add more items
   - Select product
   - Enter quantity
   - Price auto-fills
5. Set tax percentage (e.g., 18%)
6. Add discount (if any)
7. Click **"Create Invoice"**
8. View invoice and click **"Print"** or **"Export PDF"**

### Task 4: Create a Quotation

1. Click **"Quotations"** in menu
2. Click **"Create Quotation"**
3. Select customer
4. Add products and quantities
5. Set prices and taxes
6. Click **"Create & Send"**
7. Customer can view quotation

### Task 5: Create Purchase Order

1. Click **"Purchase Orders"** in menu
2. Click **"Create Purchase Order"**
3. Select supplier
4. Add items to order
5. Set cost prices
6. Add shipping cost and tax
7. Click **"Create & Send"**

### Task 6: View Reports

1. Click **"Reports"** in menu
2. Choose:
   - **Sales Report**: View invoices and revenue
   - **Inventory Report**: Check stock levels and expiry dates
3. Filter by date range if needed
4. Print or export

### Task 7: Access Admin Dashboard

1. Click your username at top-right
2. Select **"Admin Dashboard"** (only visible to admins)
3. Here you can:
   - **Manage Users**: Add staff, managers, admins
   - **Manage Suppliers**: Add supplier details
   - **Backup Database**: Create backups
   - **View Logs**: See system activity

---

## 🆘 Troubleshooting

### Problem: "Python not found"

**Solution:**
1. Reinstall Python from https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Try `python --version` again

---

### Problem: "pip install fails" or "No module named pip"

**Solution:**
1. Open Command Prompt as Administrator:
   - Search for "cmd"
   - Right-click and select "Run as Administrator"
2. Type:
```bash
python -m pip install --upgrade pip
```
3. Try installing requirements again:
```bash
pip install -r requirements.txt
```

---

### Problem: "Port 5000 already in use"

**Solution:**
Another application is using port 5000. Try one of:

**Option 1:** Close other applications

**Option 2:** Use different port
1. Edit `app/main.py`
2. Find: `app.run(host='127.0.0.1', port=5000, ...)`
3. Change `5000` to `5001` or `8000`
4. Save and run again

---

### Problem: "Cannot access http://localhost:5000"

**Solution:**
1. Make sure application is running (you see the Flask message)
2. Try refreshing browser (press F5)
3. Try different browser (Chrome, Edge, Firefox)
4. Check if firewall is blocking:
   - Open Windows Defender Firewall
   - Click "Allow app through firewall"
   - Find "Python" and allow it

---

### Problem: "Database error" or "Cannot create database"

**Solution:**
1. Delete the database file:
   - Look for `medical_store.db` in project folder
   - Delete it
2. Restart the application
3. Fresh database will be created
4. Login with `admin/admin`

---

### Problem: "Login fails even with correct password"

**Solution:**
1. Delete `medical_store.db` from project folder
2. Restart application (it will create fresh database)
3. Login with:
   - Username: `admin`
   - Password: `admin`

---

### Problem: "Virtual environment not found"

**Solution:**
Recreate virtual environment:
```bash
rm -r venv          # Delete old venv
python -m venv venv # Create new
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🛑 Stopping the Application

1. In Command Prompt window running the application
2. Press `CTRL + C`
3. Application will stop

---

## ▶️ Restarting the Application

Next time you want to use the system:

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Navigate to project folder:
   ```bash
   cd C:\path\to\medical-store-invoicing
   ```
4. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
5. Run application:
   ```bash
   python app/main.py
   ```
6. Open browser: `http://localhost:5000`
7. Login and use!

---

## 💾 Backing Up Your Data

### Automatic Backup:
- System creates automatic backups (check "Backup & Restore" in Admin Dashboard)

### Manual Backup:
1. Navigate to project folder
2. Copy file `medical_store.db` to safe location
3. Keep multiple copies on external drive

### To Restore:
1. Admin Dashboard → "Backup & Restore" tab
2. Click "Restore Backup"
3. Select your backup file
4. Click "Restore"

---

## 🎓 Video Tutorials

Watch these tutorial links (create your own or find similar):
- Python Installation: https://www.youtube.com/results?search_query=install+python+windows
- Flask Basics: https://www.youtube.com/results?search_query=flask+tutorial

---

## 📞 Getting Help

If you encounter issues:

1. **Check Troubleshooting** section above
2. **Read error messages carefully** - they often tell you what's wrong
3. **Check console output** for detailed error information
4. **Search online** for the error message
5. **Post issue on GitHub** with:
   - Error message
   - Steps you took
   - Your Windows version
   - Python version

---

## ✨ Tips & Tricks

### Tip 1: Create Desktop Shortcut
Create a batch file (`start.bat`) in project folder:
```batch
@echo off
cd /d "%~dp0"
venv\Scripts\activate
python app/main.py
pause
```
Double-click this file to start application.

### Tip 2: Backup Before Updates
Always backup database before updating code

### Tip 3: Use Chrome for Best Experience
Chrome has the best compatibility with this application

### Tip 4: Keyboard Shortcuts
- `Ctrl + P`: Print current page
- `Ctrl + S`: Save (in some forms)
- `Tab`: Move to next field
- `Enter`: Submit form

---

## 🎉 You're All Set!

Your Medical Store Invoicing System is ready to use!

**Next Steps:**
1. ✅ Install Python
2. ✅ Download project
3. ✅ Install dependencies
4. ✅ Run application
5. ✅ Login and start using!

**Happy invoicing!** 📊

---

**For Updates:** Check GitHub repository regularly for new features and improvements.
