# Zel App Architecture Standard

## Overview
Standardized architecture for all Zel productivity apps (zeltask, zeltimer, zeljournal, etc.) ensuring consistency, maintainability, and shared functionality.

## File Structure

### Standard Zel App Structure
```
src/zel{app}/
├── __init__.py              # Package initialization
├── cli.py                   # Main CLI entry point
├── core/                    # Business logic layer
│   ├── __init__.py
│   ├── models.py           # Data structures & types
│   ├── storage.py          # Data persistence layer
│   └── {app}_manager.py    # Main business logic
├── commands/               # CLI command modules
│   ├── __init__.py
│   ├── {feature}_commands.py
│   └── ...
└── ui/                     # User interface layer (optional)
    ├── __init__.py
    ├── tui/                # Terminal UI (TUI) components
    │   ├── __init__.py
    │   ├── screens.py      # TUI screen definitions
    │   ├── widgets.py      # Custom TUI widgets
    │   └── app.py          # Main TUI application
    └── web/                # Web interface components
        ├── __init__.py
        ├── routes.py       # Web routes/endpoints
        ├── templates/      # HTML templates
        └── static/         # CSS/JS assets
```

### ZelUtil Structure (Foundation)
```
src/zelutil/
├── __init__.py              # Package initialization & exports
├── cli.py                   # Main CLI entry point
├── core/                    # Business logic layer
│   ├── __init__.py
│   ├── installer.py        # Installation & setup logic
│   ├── registry.py         # App registry & module management
│   └── updater.py          # Update & maintenance logic
├── commands/               # CLI command modules
│   ├── __init__.py
│   ├── module_commands.py  # Module management (get, install, update)
│   └── manage_commands.py  # Configuration & status commands
├── utils/                  # Shared utilities (exported for other apps)
│   ├── __init__.py
│   ├── state.py           # State directory management
│   ├── paths.py           # Path resolution helpers
│   ├── config.py          # Configuration utilities
│   └── integration.py     # Cross-app integration helpers
└── data/                   # Static data
    └── zel-modules.json   # Module registry
```

## Layer Responsibilities

### CLI Layer (`cli.py`)
- **Purpose**: Main entry point and command routing
- **Responsibilities**:
  - Click group setup and command registration
  - High-level command orchestration
  - Quick access shortcuts (e.g., `zeltask list`)
- **Dependencies**: Commands modules only

### Commands Layer (`commands/`)
- **Purpose**: CLI command definitions and user interaction
- **Responsibilities**:
  - Click command definitions with arguments/options
  - User input validation and formatting
  - Output formatting and display
  - Calling core business logic
- **Dependencies**: Core layer, Click
- **Files**:
  - `{feature}_commands.py` - Feature-specific commands
  - Group related commands (e.g., task operations, blueprint management)

### UI Layer (`ui/`) - Optional
- **Purpose**: Alternative user interfaces beyond CLI
- **Responsibilities**:
  - Terminal User Interface (TUI) for interactive terminal control
  - Web interface for browser-based access
  - UI state management and event handling
  - Calling core business logic (same as CLI)
- **Dependencies**: Core layer, UI frameworks (Rich/Textual for TUI, Flask/FastAPI for web)
- **Components**:
  - **TUI (`ui/tui/`)**: Terminal-based interactive interface
    - `app.py` - Main TUI application entry point
    - `screens.py` - Screen layouts and navigation
    - `widgets.py` - Custom interactive components
  - **Web (`ui/web/`)**: Browser-based interface
    - `routes.py` - HTTP endpoints and API routes
    - `templates/` - HTML template files
    - `static/` - CSS, JavaScript, and asset files

### Core Layer (`core/`)
- **Purpose**: Business logic and data management
- **Responsibilities**:
  - Application-specific business rules
  - Data validation and processing
  - Orchestrating storage operations
  - Cross-cutting concerns (recurring tasks, etc.)
- **Dependencies**: Storage, Models, zelutil
- **Files**:
  - `models.py` - Data structures, dataclasses, types
  - `storage.py` - JSON file operations, data persistence
  - `{app}_manager.py` - Main business logic coordinator

### Utils Layer (`utils/`) - ZelUtil Only
- **Purpose**: Shared utilities exported for other Zel apps
- **Responsibilities**:
  - State directory resolution and management
  - Configuration loading and saving
  - Cross-app integration helpers
  - Path resolution utilities
- **Dependencies**: Minimal (pathlib, json)
- **Files**:
  - `state.py` - State directory management
  - `paths.py` - Path resolution helpers
  - `config.py` - Configuration utilities
  - `integration.py` - Cross-app integration helpers

## Shared Dependencies (zelutil)

### Path Management
```python
from zelutil.utils.state import resolve_state_dir
# Always use: resolve_state_dir() / "app_name"
```

### Configuration Management
```python
from zelutil.utils.config import load_config, save_config
# App-specific or global configuration
```

### Cross-App Integration
```python
from zelutil.utils.integration import get_installed_apps, get_app_data_dir
# Discover and interact with other Zel apps
```

### Common Utilities
- State directory resolution
- Configuration management
- Cross-app integration helpers
- Path resolution utilities

## Data Storage Standard

### File Structure
```
~/.local/state/zel/
├── {app}/
│   ├── active.json      # Current/working items
│   ├── completed.json   # Archived/finished items
│   └── blueprint.json   # Templates/configurations
└── shared/              # Cross-app data
```

### JSON Structure
- **active.json**: Current working items (tasks, timers, etc.)
- **completed.json**: Historical/archived items
- **blueprint.json**: Templates and configurations

## Implementation Benefits

### For Individual Apps
- **Consistent**: Same patterns across all Zel apps
- **Maintainable**: Clear separation of concerns
- **Testable**: Business logic isolated from CLI
- **Extensible**: Easy to add new commands/features

### For Zel Ecosystem
- **Shared utilities**: Common functionality in zelutil
- **Cross-integration**: Apps can easily interact
- **Unified data**: Standardized storage enables daily summaries
- **Scalable**: New apps follow established patterns

## Implementation Guidelines

### New Zel App Checklist
1. Create standard folder structure
2. Use zelutil for paths and state management
3. Implement core 3-layer architecture (CLI → Commands → Core)
4. Follow JSON storage standard (active/completed/blueprint)
5. Add to zelutil registry for cross-app integration
6. (Optional) Implement UI layer for enhanced user experience

### UI Implementation Guidelines

#### TUI Development (Terminal User Interface)
- Use libraries like Rich, Textual, or urwid for terminal control
- Implement real-time updates and interactive navigation
- Maintain responsive design for different terminal sizes
- Provide keyboard shortcuts and intuitive controls
- Example entry: `zeltask --tui` or `zeltask tui`

#### Web Interface Development
- Use lightweight frameworks (Flask, FastAPI) for API endpoints
- Implement RESTful API that mirrors CLI functionality
- Provide real-time updates via WebSockets if needed
- Ensure mobile-responsive design
- Example entry: `zeltask --web` or `zeltask serve`

#### UI Design Principles
- **Consistency**: Same data and operations across all interfaces
- **Separation**: UI layer only handles presentation, core handles logic
- **Flexibility**: Users can choose CLI, TUI, or web based on preference
- **Integration**: All interfaces share the same underlying data and business logic

### Command Design
- Group related functionality (e.g., `zeltask task create`)
- Provide shortcuts for common operations (e.g., `zeltask list`)
- Use consistent option naming across apps
- Validate inputs at command level, process in core

### Storage Design
- Use zelutil.utils.state for path resolution
- Implement app-specific storage class in core/storage.py
- Follow active/completed/blueprint pattern
- Handle file creation and error cases gracefully

## Interface Options

### CLI (Command Line Interface)
- **Best for**: Automation, scripting, quick operations
- **Usage**: `zeltask create "Fix bug" --priority high`

### TUI (Terminal User Interface)
- **Best for**: Interactive terminal sessions, real-time monitoring
- **Usage**: `zeltask --tui` (full-screen terminal application)

### Web Interface
- **Best for**: Remote access, team collaboration, visual dashboards
- **Usage**: `zeltask serve` (starts web server)

This architecture ensures all Zel apps are consistent, maintainable, and can integrate seamlessly for comprehensive productivity tracking across multiple interface paradigms.