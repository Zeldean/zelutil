#!/usr/bin/env python3
"""
Bootstrap script to install ZelCandy and set up the Zel ecosystem.
Can be run directly from GitHub or locally.

Usage:
  curl -sSL https://raw.githubusercontent.com/Zeldean/zelcandy/main/bootstrap-zel.py | python3
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

def clone_zelcandy(install_dir):
    """Clone zelcandy repository"""
    zelcandy_url = "https://github.com/Zeldean/zelcandy.git"
    zelcandy_dir = install_dir / "zelcandy"
    
    print(f"Cloning zelcandy to {zelcandy_dir}...")
    subprocess.run(["git", "clone", zelcandy_url, str(zelcandy_dir)], check=True)
    return zelcandy_dir

def main():
    parser = argparse.ArgumentParser(description="Bootstrap Zel tools installation")
    parser.add_argument("--install-dir", type=Path, default=get_default_install_dir(),
                       help="Directory to install zel tools (default: ~/.local/share/zel-tools)")
    
    args = parser.parse_args()
    install_dir = args.install_dir
    
    print(f"Installing Zel tools to: {install_dir}")
    
    # Create install directory
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Clone zelcandy
    zelcandy_dir = clone_zelcandy(install_dir)
    
    # Run zelcandy install script
    install_script = zelcandy_dir / "src" / "zelcandy" / "install.py"
    print("Running zelcandy install script...")
    subprocess.run([sys.executable, str(install_script)], check=True, cwd=str(zelcandy_dir))
    
    print(f"\nZel tools installed successfully!")
    print(f"Installation directory: {install_dir}")
    print(f"Virtual environment: {get_venv_path()}")
    print("\nRestart your shell or run: source ~/.bashrc (or ~/.zshrc)")

if __name__ == "__main__":
    main()
