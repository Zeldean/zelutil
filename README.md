# ZelUtil

Shared configuration, state management, and metadata for the Zel CLI suite.

## Why ZelUtil exists

- Provides a single state directory (`~/.local/state/zel`) used by tools like
  `zeljournal`, `zelmedia`, and `zeltimer`.
- Stores reusable path aliases in `paths.json` so every module can resolve your
  vaults, media folders, and timer logs consistently.
- Ships a registry (`zelutil.data/zel-modules.json`) describing the Zel module
  ecosystem, which powers simple install & discovery tooling.
- Exposes convenience helpers (`resolve_state_dir`, `get_path`, `set_path`,
  `get_available_paths`) for other packages to import.

## Installation

### Quick install (recommended)

Install to the default locations:
```bash
curl -sSL https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py | python3
```

### Custom install location

Target a specific directory:
```bash
curl -sSL https://raw.githubusercontent.com/Zeldean/zelutil/main/bootstrap-zel.py | python3 - --install-dir ~/my-zel-tools
```

### Default locations

**Installation directory**
- Linux/macOS: `~/.local/share/zel-tools`
- Windows: `%LOCALAPPDATA%\zel-tools`

**Shared virtual environment**
- Linux/macOS: `~/.local/share/zel-env`
- Windows: `%LOCALAPPDATA%\zel-env`

### Manual install from source

```bash
git clone https://github.com/Zeldean/zelutil.git
cd zelutil
python3 src/zelutil/install.py
```

## State layout

```text
~/.local/state/zel/
    paths.json        # key → absolute path registry shared by all modules
    timers.json       # example: created by zeltimer
    vault_index.json  # example: created by zeljournal
```

The path currently resolves to `~/.local/state/zel` on every platform. Override
it in your own tooling by calling `resolve_state_dir()` and storing files
relative to the returned directory.

## CLI reference

### `zelutil path …`

```bash
zelutil path available        # see documented keys such as "vault", "media"
zelutil path set vault /mnt/Vault/Second-Brain
zelutil path get vault        # prints the stored value or errors if missing
zelutil path list             # dump the current registry
```

Keys are described in `src/zelutil/registry.py` and include a short blurb,
example path, and which modules consume them.

### `zelutil install …`

```bash
zelutil install list          # show metadata from zel-modules.json
zelutil install all           # run the bundled install script (bootstrap)
zelutil install module zeltimer
```

`install module` currently prints what would be installed; GitHub clone logic is
stubbed while the module manifests are refined.

## Using ZelUtil from code

```python
from zelutil import resolve_state_dir, get_path, set_path

state_dir = resolve_state_dir()
logs = state_dir / "timers.json"

projects = get_path("projects", default="~/Projects")
set_path("media", "/mnt/media")
```

When bundled into other modules, these helpers keep every CLI grounded in the
same configuration without hard-coded paths.