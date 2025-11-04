#!/usr/bin/env python3
import json
import os
import platform
import subprocess
import sys
from importlib import resources
from pathlib import Path

def get_venv_path():
    """Get platform-appropriate venv path"""
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel-env"
    else:
        return Path.home() / ".local" / "share" / "zel-env"

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
        print(f"Add to PATH manually: {bin_path}")
        print("Or run: setx PATH \"%PATH%;{bin_path}\"")
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
            modules_file = Path(__file__).parent / "data" / "zel-modules.json"
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
    # Find parent directory with all zel components
    parent_dir = Path(__file__).parent.parent.parent.parent
    venv_path = get_venv_path()
    modules = load_modules()
    components = list(modules.keys())

    if not components:
        print("No module metadata available; nothing to install.")
        return
    
    print(f"Creating zel virtual environment at {venv_path}...")
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
    
    print("Installing zel components...")
    for component in components:
        component_path = parent_dir / component
        if component_path.exists():
            print(f"Installing {component}...")
            subprocess.run([str(pip_exe), "install", "-e", str(component_path)], check=True)
        else:
            print(f"Skipping {component} (not found)")
    
    print("Adding to PATH...")
    add_to_path(bin_path)
    
    print("\nDone! All available zel tools installed.")
    print(f"Virtual environment: {venv_path}")

if __name__ == "__main__":
    main()
