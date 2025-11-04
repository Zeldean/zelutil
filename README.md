# 🛠️ ZelUtil

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/Zeldean/zelutil)
![Issues](https://img.shields.io/github/issues/Zeldean/zelutil)
![Repo Size](https://img.shields.io/github/repo-size/Zeldean/zelutil)

The foundation of the Zel productivity suite - handles installation, configuration, and shared utilities for all Zel tools.

---

## 🚀 Quick Start

Install ZelUtil and set up the Zel ecosystem with one command:

**Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py | python3
```

**Windows PowerShell 5+:**
```powershell
irm https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py | python
```

That's it! This will:
- 📥 Download and set up ZelUtil
- 🐍 Create a dedicated Python environment for all Zel tools
- ⚡ Make the `zelutil` command available in your terminal

---

## 🎯 Custom Installation

Want to install somewhere specific? Download and run with `--install-dir`:

```bash
# Download first, then run with custom directory
wget https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py
python3 bootstrap-zel.py --install-dir ~/my-zel-tools
```

---

## 📁 What Gets Installed Where

After installation, you'll have two main directories:

### 🏠 Installation Files
**Location:** `~/.local/share/zel/` (Linux/macOS) or `%LOCALAPPDATA%\zel\` (Windows)

This contains:
- `venv/` - The Python environment for all Zel tools
- `zelutil/` - ZelUtil source code
- Future Zel tools will be installed here too

### 💾 Your Data
**Location:** `~/.local/state/zel/` (all platforms)

This is where your personal data lives:
- ⚙️ Settings and preferences
- ⏱️ Timer logs
- 📝 Journal entries
- 🔗 File paths and bookmarks

---

## ✅ Requirements

- 🐍 Python 3.8 or newer
- 📦 Git (for downloading tools)
- 🌐 Internet connection (for initial setup)

---

## 🗑️ Uninstalling

To remove everything:
1. Delete the installation directory: `~/.local/share/zel/`
2. Remove from your shell config (look for "# Zel tools" in `~/.bashrc` or `~/.zshrc`)
3. Optionally delete your data: `~/.local/state/zel/`