#!/usr/bin/env python3
"""
Bootstrap script to install ZelUtil and set up the Zel ecosystem.
Can be run directly from GitHub or locally.

Usage:
  curl -sSL https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py | python3
  or
  python3 bootstrap-zel.py [--install-dir PATH]
"""
import os
import sys
import subprocess
import platform
import tempfile
import shutil
import argparse
from pathlib import Path

def get_default_install_dir():
    """Get default installation directory"""
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel-tools"
    else:
        return Path.home() / ".local" / "share" / "zel-tools"

def get_venv_path():
    """Get platform-appropriate venv path"""
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel-env"
    else:
        return Path.home() / ".local" / "share" / "zel-env"

def clone_zelutil(install_dir):
    """Clone zelutil repository"""
    zelutil_url = "https://github.com/Zeldean/zelutil.git"
    zelutil_dir = install_dir / "zelutil"
    
    print(f"Cloning zelutil to {zelutil_dir}...")
    subprocess.run(["git", "clone", zelutil_url, str(zelutil_dir)], check=True)
    return zelutil_dir

def main():
    parser = argparse.ArgumentParser(description="Bootstrap Zel tools installation")
    parser.add_argument("--install-dir", type=Path, default=get_default_install_dir(),
                       help="Directory to install zel tools (default: ~/.local/share/zel-tools)")
    
    args = parser.parse_args()
    install_dir = args.install_dir
    
    print(f"Installing Zel tools to: {install_dir}")
    
    # Create install directory
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Clone zelutil
    zelutil_dir = clone_zelutil(install_dir)
    
    # Run zelutil install script
    install_script = zelutil_dir / "src" / "zelutil" / "install.py"
    print("Running zelutil install script...")
    subprocess.run([sys.executable, str(install_script)], check=True, cwd=str(zelutil_dir))
    
    print(f"\nZel tools installed successfully!")
    print(f"Installation directory: {install_dir}")
    print(f"Virtual environment: {get_venv_path()}")
    print("\nRestart your shell or run: source ~/.bashrc (or ~/.zshrc)")

if __name__ == "__main__":
    main()