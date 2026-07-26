# newpy

A self-contained Python project scaffolder that creates a ready-to-use Python project with a virtual environment, main.py, .gitignore, and Git initialization. Works on any system with Python 3 installed. No external dependencies required.

## Installation

### One-liner (curl)

```bash
curl -sSL https://raw.githubusercontent.com/benrialamounir/newpy/main/install.sh | bash
```

### One-liner (wget)

```bash
wget -qO- https://raw.githubusercontent.com/benrialamounir/newpy/main/install.sh | bash
```

### Manual

1. Download the script:
   ```bash
   curl -sSL https://raw.githubusercontent.com/benrialamounir/newpy/main/newpy -o newpy
   ```
2. Make it executable:
   ```bash
   chmod +x newpy
   ```
3. Move it to a directory in your PATH (e.g. `/usr/local/bin` or `~/.local/bin`):
   ```bash
   mv newpy ~/.local/bin/
   ```

## Usage

Just run:

```bash
newpy
```

The interactive wizard will guide you through:

1. **Target directory** - Where to create the project (defaults to your home directory)
2. **Project name** - Name of your Python project
3. **Setup** - Automatically creates:
   - Project directory
   - Python virtual environment (uses `uv` if available, falls back to `venv`)
   - `main.py` with a hello world template
   - `.gitignore` for Python projects
   - Git repository (if Git is installed)

## Requirements

- Python 3.x (stdlib only, no additional packages needed)
- Optional: `uv` for faster virtual environment creation
- Optional: Git (to initialize a repository)
- Optional: `curl` or `wget` (for one-liner installation)

## License

MIT