# 🚀 Setup Guide — Fire Hazard Detection System

## ✅ Prerequisites (Do This First)

1. Install **Python 3.10 or 3.11** from [python.org/downloads](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT**: During installation, check **"Add Python to PATH"** before clicking Install.
2. Install **Git** from [git-scm.com](https://git-scm.com/downloads) *(only needed for Option 1)*.

---

## 📥 Option 1 — Download from GitHub

Use this method if the project is pushed to GitHub.

### Step 1: Clone the Repository

Open **Command Prompt** or **Terminal** and run:

```bash
git clone https://github.com/YOUR_USERNAME/mca_final_fire.git
cd mca_final_fire
```

> Replace `YOUR_USERNAME` with the actual GitHub username.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

*(You should see `(venv)` at the start of the terminal prompt)*

### Step 4: Install All Dependencies

```bash
pip install -r requirements.txt
```

> This takes a few minutes — PyTorch is a large download (~400–700 MB).

### Step 5: Run the App

```bash
python app.py
```

### Step 6: Open the Browser

Go to **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in any browser. Done! 🎉

---

## 💾 Option 2 — Copy from Pendrive (USB)

Use this method when there's no internet or no GitHub repository.

### Step 1: Copy the Folder

Copy the entire `mca_final_fire` folder from the USB drive to the laptop (e.g., onto the Desktop or in Documents).

> ⚠️ **Do NOT copy the `venv` folder** — it won't work on a different laptop. Instead, create a fresh one in Step 3.

### Step 2: Open Terminal in the Project Folder

1. Navigate into the `mca_final_fire` folder.
2. Hold `Shift` + Right-click inside the folder → **"Open PowerShell window here"** (Windows).

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 5: Install All Dependencies

```bash
pip install -r requirements.txt
```

> Internet is still needed here to download the packages. If no internet is available, see the **Offline Install** section below.

### Step 6: Run the App

```bash
python app.py
```

### Step 7: Open the Browser

Go to **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in any browser. Done! 🎉

---

## 📴 Offline Install (No Internet + USB)

If the target laptop has **no internet**, you need to carry the packages on the USB too.

**On the SOURCE laptop (your laptop), run:**

```bash
pip download -r requirements.txt -d ./packages
```

This saves all packages into a `packages/` folder. Copy this folder to the USB along with the project.

**On the TARGET laptop (new laptop), run:**

```bash
pip install --no-index --find-links=packages -r requirements.txt
```

---

## 🙋 Common Errors & Fixes

| Error | Fix |
|---|---|
| `python` not recognized | Python not added to PATH during install. Re-install Python and tick **"Add to PATH"**. |
| `pip install` fails | Check your internet connection. Try `pip install -r requirements.txt --timeout 120` |
| `ModuleNotFoundError: cv2` | Run `pip install opencv-python` inside the activated `venv`. |
| Camera not turning on | In the Web UI Settings tab, toggle Camera ID (try `0`, `1`, or `2`). |
| Port 5000 in use | Change port in `app.py` last line: `port=5001` |
