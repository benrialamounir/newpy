# newpy

A self-contained Python project scaffolder that creates a ready-to-use Python project with a virtual environment, `main.py`, solid `.gitignore`, optional README & requirements.txt, and Git initialization.

Works on any system with Python 3. **No external dependencies required.**

## Features

- Interactive wizard (clean terminal UI with colors)
- Creates project directory + virtual environment
  - Prefers [uv](https://github.com/astral-sh/uv) when available (much faster)
  - Falls back to the standard library `venv`
- Generates:
  - `main.py` (hello-world template with type hints)
  - Comprehensive `.gitignore` for Python projects
  - Optional `README.md`
  - Optional empty `requirements.txt`
- Initializes a Git repository + makes an initial commit (when Git is configured)
- Cross-platform activation instructions (Linux / macOS / Windows)
- Pure Python 3 + bash installer — zero runtime dependencies

## Installation

### One-liner (recommended)

```bash
curl -sSL https://raw.githubusercontent.com/benrialamounir/newpy/main/install.sh | bash
```

or with wget:

```bash
wget -qO- https://raw.githubusercontent.com/benrialamounir/newpy/main/install.sh | bash
```

### Manual

```bash
curl -sSL https://raw.githubusercontent.com/benrialamounir/newpy/main/newpy.py -o newpy
chmod +x newpy
mv newpy ~/.local/bin/   # or any directory in your PATH
```

Make sure `~/.local/bin` is in your `$PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

Just run:

```bash
newpy
```

The wizard will ask you for:

1. **Target directory** (defaults to your home directory)
2. **Project name**
3. Whether to create `README.md` and `requirements.txt`
4. Whether to initialize a Git repository

Then it creates everything automatically.

### Example session

```
$ newpy
 Target directory: ~/projects
 Project name: cool-app
 Create README.md? [Y/n]
 Create requirements.txt? [Y/n]
 Initialize Git? [Y/n]
 ...
 ✓ Project created successfully!

   Path: /home/you/projects/cool-app

   Quick Start:
     cd /home/you/projects/cool-app
     source .venv/bin/activate
     python main.py
```

## Requirements

- Python 3.8+ (stdlib only)
- Optional but recommended: [uv](https://github.com/astral-sh/uv) for fast virtual environments
- Optional: Git (for repository initialization)
- Optional: `curl` or `wget` (for the one-liner installer)

## License

MIT
