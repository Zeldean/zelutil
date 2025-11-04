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

def get_install_dir():
    """Get installation directory"""
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel"
    else:
        return Path.home() / ".local" / "share" / "zel"

def get_venv_path():
    """Get platform-appropriate venv path"""
    return get_install_dir() / "venv"

def clone_zelutil(install_dir):
    """Clone or update zelutil repository"""
    zelutil_url = "https://github.com/Zeldean/zelutil.git"
    zelutil_dir = install_dir / "zelutil"
    
    if zelutil_dir.exists():
        print(f"Updating existing zelutil at {zelutil_dir}...")
        subprocess.run(["git", "pull"], cwd=str(zelutil_dir), check=True)
    else:
        print(f"Cloning zelutil to {zelutil_dir}...")
        subprocess.run(["git", "clone", zelutil_url, str(zelutil_dir)], check=True)
    return zelutil_dir

def main():
    parser = argparse.ArgumentParser(description="Bootstrap Zel tools installation")
    parser.add_argument("--install-dir", type=Path, default=get_install_dir(),
                       help="Directory to install zel tools (default: ~/.local/share/zel)")
    
    args = parser.parse_args()
    install_dir = args.install_dir
    
    print(f"Installing Zel tools to: {install_dir}")
    
    # Create install and state directories
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Create state directory
    if platform.system() == "Windows":
        state_dir = Path.home() / "AppData" / "Local" / "zel" / "state"
    else:
        state_dir = Path.home() / ".local" / "state" / "zel"
    state_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"State directory: {state_dir}")
    
    # Check if already in PATH
    venv_path = get_venv_path()
    if platform.system() == "Windows":
        bin_path = venv_path / "Scripts"
    else:
        bin_path = venv_path / "bin"
    
    path_env = os.environ.get("PATH", "")
    if str(bin_path) not in path_env:
        print(f"\nIMPORTANT: Add {bin_path} to your PATH to use zel commands.")
        if platform.system() == "Windows":
            print(f"Run: setx PATH \"%PATH%;{bin_path}\"")
            print("Or add it manually through System Properties > Environment Variables")
        else:
            shell = os.environ.get("SHELL", "")
            if "zsh" in shell:
                config_file = "~/.zshrc"
            elif "fish" in shell:
                config_file = "~/.config/fish/config.fish"
            else:
                config_file = "~/.bashrc"
            print(f"The install script should have added it to {config_file}")
            print(f"Restart your shell or run: source {config_file}")
    else:
        print("\nzel commands should be available in your PATH.")
    
    # Clone zelutil
    zelutil_dir = clone_zelutil(install_dir)
    
    # Run zelutil install script
    install_script = zelutil_dir / "src" / "zelutil" / "install.py"
    print("Running zelutil install script...")
    subprocess.run([sys.executable, str(install_script)], check=True, cwd=str(zelutil_dir))
    
    print(f"\nZel tools installed successfully!")
    print(f"Installation directory: {install_dir}")
    print(f"Virtual environment: {get_venv_path()}")
    print(f"\nTry running: zelutil --help")

if __name__ == "__main__":
    main()