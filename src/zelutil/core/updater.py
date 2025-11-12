import subprocess
from .installer import get_install_dir
from .registry import load_modules


def update_modules():
    """Update all installed zel modules"""
    install_dir = get_install_dir()
    modules = load_modules()
    
    if not modules:
        return [], [], "No modules configured"
    
    updated = []
    failed = []
    
    for module in modules.keys():
        module_dir = install_dir / module
        if module_dir.exists():
            result = subprocess.run(
                ["git", "pull"], 
                cwd=module_dir, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                updated.append(module)
            else:
                failed.append((module, result.stderr))
    
    return updated, failed, None