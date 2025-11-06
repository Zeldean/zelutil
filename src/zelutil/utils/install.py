#!/usr/bin/env python3
import json
import os
import platform
import subprocess
import sys
from importlib import resources
from pathlib import Path

def get_install_dir():
    """Get installation directory from stored paths or default"""
    # Try to get stored install location
    if platform.system() == "Windows":
        state_dir = Path.home() / "AppData" / "Local" / "zel" / "state"
    else:
        state_dir = Path.home() / ".local" / "state" / "zel"
    
    paths_file = state_dir / "paths.json"
    if paths_file.exists():
        try:
            with open(paths_file, 'r') as f:
                paths_data = json.load(f)
                if "install_dir" in paths_data:
                    return Path(paths_data["install_dir"])
        except (json.JSONDecodeError, KeyError):
            pass
    
    # Fall back to default location
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel"
    else:
        return Path.home() / ".local" / "share" / "zel"

def get_venv_path():
    """Get platform-appropriate venv path"""
    install_dir = get_install_dir()
    
    # Check if we're in development mode (temp_venv exists)
    temp_venv = install_dir / "temp_venv"
    if temp_venv.exists():
        return temp_venv
    
    return install_dir / "venv"

def get_shell_config():
    """Get shell config file path"""
    if platform.system() == "Windows":
        return None  # Windows uses registry/environment variables
    
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return Path.home() / ".zshrc"
    elif "fish" in shell:
        return Path.home() / ".config" / "fish" / "config.fish"
    else:
        return Path.home() / ".bashrc"

def add_to_path(bin_path):
    """Add to PATH based on platform"""
    if platform.system() == "Windows":
        print(f"\n=== WINDOWS PATH SETUP ===")
        print(f"To use 'zelutil' command, add this to your PATH:")
        print(f"  {bin_path}")
        print(f"\nOption 1 - PowerShell (run as Administrator):")
        print(f'  setx PATH "$env:PATH;{bin_path}" /M')
        print(f"\nOption 2 - Current session only:")
        print(f'  $env:PATH += ";{bin_path}"')
        print(f"\nOption 3 - System Properties:")
        print(f"  1. Win+R → sysdm.cpl → Advanced → Environment Variables")
        print(f"  2. Edit PATH → Add: {bin_path}")
        print(f"\nAfter adding, restart PowerShell and try: zelutil --help")
        return
    
    shell_config = get_shell_config()
    if not shell_config:
        print(f"Add to PATH manually: {bin_path}")
        return
    
    path_line = f'export PATH="{bin_path}:$PATH"'
    
    if shell_config.exists():
        content = shell_config.read_text()
        if str(bin_path) in content:
            print("Already in PATH")
            return
    
    with open(shell_config, "a") as f:
        f.write(f"\n# Zel tools\n{path_line}\n")
    
    print(f"Added to {shell_config}")
    print(f"Restart shell or run: source {shell_config}")

def load_modules():
    """Load module configuration from packaged metadata or local file."""
    try:
        # Try to load from installed package first
        with resources.open_text("zelutil.data", "zel-modules.json", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (FileNotFoundError, ModuleNotFoundError):
        # Fall back to local file when package not installed
        try:
            modules_file = Path(__file__).parent.parent / "data" / "zel-modules.json"
            with open(modules_file, encoding="utf-8") as fh:
                payload = json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            print(f"Warning: failed to load module metadata: {exc}")
            return {}
    except json.JSONDecodeError as exc:
        print(f"Warning: failed to parse module metadata: {exc}")
        return {}

    return payload.get("modules", {})

def main():
    # Use install directory to find zel components
    install_dir = get_install_dir()
    venv_path = get_venv_path()
    modules = load_modules()
    components = list(modules.keys())

    if not components:
        print("No module metadata available; nothing to install.")
        return
    
    if not venv_path.exists():
        print(f"Creating zel virtual environment at {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    else:
        print(f"Using existing virtual environment at {venv_path}...")
    
    # Get executables
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        bin_path = venv_path / "Scripts"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
        bin_path = venv_path / "bin"
    
    print("Installing zel components...")
    for component in components:
        component_path = install_dir / component
        if component_path.exists():
            print(f"Installing {component}...")
            subprocess.run([str(pip_exe), "install", "-e", str(component_path)], check=True)
        else:
            print(f"Skipping {component} (not found at {component_path})")
    
    print("Adding to PATH...")
    add_to_path(bin_path)
    
    print("\nDone! All available zel tools installed.")
    print(f"Installation directory: {install_dir}")
    print(f"Virtual environment: {venv_path}")

if __name__ == "__main__":
    main()
