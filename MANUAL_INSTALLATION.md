# Manual Installation Guide

**Note**: We strongly recommend using Docker for most users. Manual installation requires more technical knowledge and troubleshooting skills. Only proceed if you have specific requirements that prevent you from using Docker.

## Prerequisites

### System Requirements
- **Python 3.10** (other versions may cause compatibility issues)
- **NGSpice circuit simulator**
- **Git** (for cloning the repository)
- **4GB+ RAM** (for larger simulations)
- **1GB free disk space**

### Check Your Python Version
```bash
python --version  # Should show Python 3.10.x
# If not available, try:
python3 --version
python3.10 --version
```

## Step-by-Step Installation

### 1. Install Python 3.10

#### Windows:
1. Download Python 3.10 from [python.org](https://www.python.org/downloads/windows/)
2. During installation, **check "Add Python to PATH"**
3. Choose "Install for all users" if you have admin rights
4. Verify: Open Command Prompt and type `python --version`

#### macOS:
```bash
# Using Homebrew (install Homebrew first if needed)
brew install python@3.10

# Or download from python.org
# After installation, you may need to use python3.10 instead of python
```

#### Linux (Ubuntu/Debian):
```bash
# Install Python 3.10
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-pip

# Make sure it's available
python3.10 --version
```

#### Linux (CentOS/RHEL/Fedora):
```bash
# Fedora
sudo dnf install python3.10 python3.10-pip

# CentOS/RHEL (may need EPEL repository)
sudo yum install python3.10 python3.10-pip
```

### 2. Install NGSpice

#### Windows:
1. Download from [NGSpice Downloads](http://ngspice.sourceforge.net/download.html)
2. Choose the Windows installer (ngspice-XX-win64.zip or .exe)
3. Extract/install to a folder (e.g., `C:\ngspice`)
4. Add to PATH:
   - Open "Environment Variables" in Windows settings
   - Add the NGSpice bin folder to your PATH
   - Restart command prompt
5. Test: `ngspice -v`

#### macOS:
```bash
# Using Homebrew
brew install ngspice

# Test installation
ngspice -v
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ngspice

# CentOS/RHEL/Fedora
sudo yum install ngspice  # or dnf install ngspice

# Test installation
ngspice -v
```

### 3. Get the Application Code

#### Option A: Download ZIP
1. Go to the [GitHub repository](https://github.com/ignaciopineyro/memristor_simulation)
2. Click "Code" → "Download ZIP"
3. Extract to your desired folder

#### Option B: Clone with Git
```bash
git clone https://github.com/ignaciopineyro/memristor_simulation.git
cd memristor_simulation
```

### 4. Set Up Python Environment

#### Create Virtual Environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3.10 -m venv venv
source venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

#### Install Dependencies:
```bash
# Make sure you're in the project folder and virtual environment is active
pip install --upgrade pip
pip install -r requirements.txt

# This may take 5-10 minutes
```

### 5. Configure Django

```bash
# Set up database
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create admin user (optional)
python manage.py createsuperuser
```

### 6. Run the Application

```bash
# Start the development server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
```

### 7. Access the Application

Open your browser and go to: http://localhost:8000

## Troubleshooting

### Python Issues
```bash
# If python command not found
# Try these alternatives:
python3 --version
python3.10 --version
py -3.10 --version  # Windows only

# If multiple Python versions conflict
# Use full path:
/usr/bin/python3.10 -m venv venv  # Linux/Mac
```

### NGSpice Issues
```bash
# Check if NGSpice is in PATH
ngspice -v

# If not found, find installation:
# Windows: Check C:\Program Files\ngspice or C:\ngspice
# Linux: which ngspice
# macOS: which ngspice

# Add to PATH manually if needed
```

### Dependency Issues
```bash
# If pip install fails
# Try upgrading pip first:
pip install --upgrade pip setuptools wheel

# If specific package fails
# Install individually:
pip install numpy==1.24.3
pip install pandas==2.0.2
# etc.

# If C compiler errors on Linux
sudo apt-get install build-essential python3.10-dev
```

### Permission Issues
```bash
# Linux/macOS: If permission denied
# Don't use sudo with pip in virtual environment
# Make sure virtual environment is activated

# Windows: Run Command Prompt as Administrator if needed
```

### Common Problems and Solutions

#### "ModuleNotFoundError" after installation
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version: `python --version`

#### NGSpice not found
- Verify installation: `ngspice -v`
- Check PATH environment variable
- Restart terminal after PATH changes

#### Django migration errors
- Delete `db.sqlite3` file and run `python manage.py migrate` again
- Check file permissions in project directory

#### Port 8000 already in use
```bash
# Find what's using the port
# Windows
netstat -ano | findstr :8000
# macOS/Linux
lsof -i :8000

# Use different port
python manage.py runserver 8001
```

## Installation Notes

- **Virtual environment is crucial** - don't skip this step
- **Exact Python 3.10 required** - 3.11+ may cause issues
- **NGSpice must be in PATH** - test with `ngspice -v`
- **Internet required** for pip installs
- **Antivirus may interfere** - add Python folder to exceptions if needed

## Need Help?

If you encounter issues with manual installation:

1. **Try Docker first** - it's much more reliable
2. **Check our [main README](README.md)** for Docker instructions
3. **Search for your specific error message** online
4. **Contact the developer**: ignaciopineyroo@gmail.com

## Why We Recommend Docker

Manual installation can be challenging because:
- Different operating systems have different requirements
- Python versions and dependencies can conflict
- NGSpice installation varies by system
- Environment variables and PATH issues are common

Docker eliminates all these issues by providing a consistent environment.