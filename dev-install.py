#!/usr/bin/env python3
"""
Local development install script for ZelUtil.
Run this from the cloned zelutil directory for local development.

Usage:
  python3 dev-install.py
"""
import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def get_dev_venv_path():
    """Get development venv path (in parent directory)"""
    return Path(__file__).parent.parent / "temp_venv"

def main():
    # Ensure we're in the zelutil directory
    if not (Path(__file__).parent / "src" / "zelutil").exists():
        print("Error: Run this script from the zelutil repository root")
        sys.exit(1)
    
    venv_path = get_dev_venv_path()
    
    print(f"Creating development virtual environment at {venv_path}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Get executables
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        bin_path = venv_path / "Scripts"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
        bin_path = venv_path / "bin"
    
    print("Installing zelutil in development mode...")
    subprocess.run([str(pip_exe), "install", "-e", "."], check=True)
    
    # Store install location in paths.json
    if platform.system() == "Windows":
        state_dir = Path.home() / "AppData" / "Local" / "zel" / "state"
    else:
        state_dir = Path.home() / ".local" / "state" / "zel"
    
    state_dir.mkdir(parents=True, exist_ok=True)
    paths_file = state_dir / "paths.json"
    
    paths_data = {}
    if paths_file.exists():
        with open(paths_file, 'r') as f:
            paths_data = json.load(f)
    
    # For dev install, use parent directory as install location
    install_dir = Path(__file__).parent.parent
    paths_data["install_dir"] = str(install_dir)
    
    with open(paths_file, 'w') as f:
        json.dump(paths_data, f, indent=2)
    
    print(f"\nDevelopment setup complete!")
    print(f"Virtual environment: {venv_path}")
    print(f"Executables: {bin_path}")
    print(f"\nTo use:")
    print(f"  {bin_path / 'zelutil'} --help")
    print(f"\nOr activate the environment:")
    if platform.system() == "Windows":
        print(f"  {bin_path / 'activate.bat'}")
    else:
        print(f"  source {bin_path / 'activate'}")

if __name__ == "__main__":
    main()