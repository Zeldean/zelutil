import json
import os
import platform
import subprocess
import sys
from pathlib import Path

from ..utils.state import resolve_state_dir


def get_install_dir():
    """Get installation directory from stored paths or default"""
    state_dir = resolve_state_dir()
    paths_file = state_dir / "paths.json"
    
    if paths_file.exists():
        try:
            with open(paths_file, 'r') as f:
                paths_data = json.load(f)
                if "install_dir" in paths_data:
                    return Path(paths_data["install_dir"])
        except (json.JSONDecodeError, KeyError):
            pass
    
    if platform.system() == "Windows":
        return Path.home() / "AppData" / "Local" / "zel"
    else:
        return Path.home() / ".local" / "share" / "zel"


def get_venv_path():
    """Get platform-appropriate venv path"""
    install_dir = get_install_dir()
    temp_venv = install_dir / "temp_venv"
    if temp_venv.exists():
        return temp_venv
    return install_dir / "venv"


def add_to_path(bin_path):
    """Add to PATH based on platform"""
    if platform.system() == "Windows":
        print(f"\n=== WINDOWS PATH SETUP ===")
        print(f"To use 'zelutil' command, add this to your PATH:")
        print(f"  {bin_path}")
        return
    
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        shell_config = Path.home() / ".zshrc"
    elif "fish" in shell:
        shell_config = Path.home() / ".config" / "fish" / "config.fish"
    else:
        shell_config = Path.home() / ".bashrc"
    
    path_line = f'export PATH="{bin_path}:$PATH"'
    
    if shell_config.exists():
        content = shell_config.read_text()
        if str(bin_path) in content:
            print("Already in PATH")
            return
    
    with open(shell_config, "a") as f:
        f.write(f"\n# Zel tools\n{path_line}\n")
    
    print(f"Added to {shell_config}")


def install_modules(modules):
    """Install zel modules to virtual environment"""
    install_dir = get_install_dir()
    venv_path = get_venv_path()
    
    if not venv_path.exists():
        print(f"Creating zel virtual environment at {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        bin_path = venv_path / "Scripts"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
        bin_path = venv_path / "bin"
    
    print("Installing zel components...")
    for component in modules.keys():
        component_path = install_dir / component
        if component_path.exists():
            print(f"Installing {component}...")
            subprocess.run([str(pip_exe), "install", "-e", str(component_path)], check=True)
    
    add_to_path(bin_path)
    return True


def clone_module(module_name, repo_url):
    """Clone a module to the installation directory"""
    install_dir = get_install_dir()
    target_dir = install_dir / module_name
    
    install_dir.mkdir(parents=True, exist_ok=True)
    
    if target_dir.exists():
        return False, f"Module '{module_name}' already exists at {target_dir}"
    
    result = subprocess.run([
        "git", "clone", repo_url, str(target_dir)
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return True, f"Successfully cloned {module_name}"
    else:
        return False, f"Failed to clone {module_name}: {result.stderr}"