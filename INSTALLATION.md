# Installation Guide

Complete step-by-step installation instructions for ExplainX.

## Table of Contents

- [System Requirements](#system-requirements)
- [Pre-Installation](#pre-installation)
- [Installation Steps](#installation-steps)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Post-Installation](#post-installation)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 7/8/10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8, 3.9, 3.10, or 3.11
- **RAM**: 2 GB (4 GB recommended)
- **Disk Space**: 500 MB
- **Internet**: Required for initial setup

### Recommended Configuration
- **OS**: Windows 10/11, macOS 12+, or Ubuntu 20.04 LTS
- **Python**: 3.10 or 3.11
- **RAM**: 4 GB or more
- **Disk Space**: 1 GB
- **Processor**: Multi-core processor
- **Browser**: Chrome/Firefox/Edge (Latest version)

---

## Pre-Installation

### 1. Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew
brew install python3

# Or download from python.org
# Then verify:
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
python3 --version
```

### 2. Install Git (Optional but Recommended)

- Download from [git-scm.com](https://git-scm.com/)
- Follow the installation wizard
- Verify: `git --version`

### 3. Verify Python & pip

```bash
python --version  # Should be 3.8 or higher
pip --version     # Should show pip version
```

---

## Installation Steps

### Step 1: Clone/Download the Repository

**Using Git (Recommended)**
```bash
git clone <repository-url>
cd ExplainX_final_PAI
```

**Or Download ZIP**
1. Download ZIP from GitHub
2. Extract to a folder
3. Open command prompt/terminal in that folder

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from system Python.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**Expected output**: Your command prompt/terminal should now show `(venv)` prefix.

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**This will install:**
- Flask (web framework)
- Pandas (data processing)
- Joblib (model loading)
- SHAP (explainability)
- Matplotlib (visualization)
- spaCy (NLP)
- NLTK (text processing)

**Installation time**: 3-10 minutes depending on internet speed

### Step 5: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

**Size**: ~40 MB

### Step 6: Verify Installation

```bash
python -c "import flask, pandas, shap, nltk; print('All libraries imported successfully!')"
```

---

## Verification

### Quick Verification Checklist

```bash
# 1. Check Python version
python --version

# 2. Check all packages installed
pip list

# 3. Test imports
python -c "from flask import Flask; from shap import Explainer; print('OK')"

# 4. Check database can be created
python db.py

# 5. Check model file exists
ls best_model.pkl  # or dir best_model.pkl on Windows
```

### Test Application Startup

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production.
```

Then open browser to `http://localhost:5000`

---

## Troubleshooting

### Issue 1: Python Not Found

**Problem**: `python: command not found` or `python is not recognized`

**Solution**:
- Ensure Python is added to PATH
- Use `python3` instead of `python` on macOS/Linux
- Reinstall Python with "Add Python to PATH" checked

### Issue 2: pip Not Found

**Problem**: `pip: command not found`

**Solution**:
```bash
# On Windows
python -m pip install --upgrade pip

# On macOS/Linux
python3 -m pip install --upgrade pip
```

### Issue 3: Virtual Environment Not Activating

**Problem**: `(venv)` prefix not showing

**Solution**:
- Check the path to venv folder
- Deactivate current venv: `deactivate`
- Recreate venv: `python -m venv venv`
- Reactivate

### Issue 4: spaCy Model Not Found

**Problem**: `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

If still failing:
```bash
pip install --upgrade spacy
python -m spacy download en_core_web_sm
```

### Issue 5: ImportError for SHAP or Other Libraries

**Problem**: `ModuleNotFoundError: No module named 'shap'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 6: Port 5000 Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Option 1: Kill the process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Option 2: Change Flask port in app.py
# Modify the line: app.run(debug=True, port=5001)
```

### Issue 7: Database Error

**Problem**: `OperationalError: database is locked`

**Solution**:
```bash
# Delete the old database
rm explainx.db  # macOS/Linux
# or
del explainx.db  # Windows

# Restart the application
python app.py
```

### Issue 8: Model File Not Found

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'best_model.pkl'`

**Solution**:
- Ensure `best_model.pkl` exists in the project root
- Check file path in `app.py`
- Make sure you're running from the correct directory

---

## Post-Installation

### 1. Verify Everything Works

```bash
# Start the application
python app.py

# Open in browser
# http://localhost:5000
```

### 2. Create First Prediction

1. Go to home page
2. Click "Make a Prediction"
3. Fill in sample data
4. Submit and verify results display correctly

### 3. Check Database

```bash
python
>>> import sqlite3
>>> conn = sqlite3.connect('explainx.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT COUNT(*) FROM predictions")
>>> print(cursor.fetchone())
```

### 4. Create Shortcut to Run (Optional)

#### Windows Batch File (run.bat)
```batch
@echo off
venv\Scripts\activate
python app.py
```

#### macOS/Linux Shell Script (run.sh)
```bash
#!/bin/bash
source venv/bin/activate
python app.py
```

Then run: `chmod +x run.sh` and `./run.sh`

---

## Environment Variables (Optional)

Create `.env` file in project root:

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_PATH=explainx.db
MODEL_PATH=best_model.pkl
LOG_LEVEL=INFO
```

Load in `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Docker Installation (Advanced)

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "app.py"]
```

### Build and Run

```bash
docker build -t explainx .
docker run -p 5000:5000 explainx
```

---

## Production Deployment

For production, use a proper WSGI server:

```bash
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Next Steps

1. Read the [README.md](README.md) for project overview
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for endpoint details
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. Start making predictions!

---

## Getting Help

- Check [README.md](README.md) for general information
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check GitHub Issues for common problems
- Read error messages carefully and search online

---

<div align="center">

**Happy installing! 🎉**

[⬆ back to installation guide](#installation-guide)

</div>
