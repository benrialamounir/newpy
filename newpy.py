#!/usr/bin/env python3
"""
newpy - Python Project Scaffolder

Creates a ready-to-use Python project with virtual environment, main.py,
.gitignore, README, and initializes a Git repository.
Works on any system with Python 3. No external dependencies required.
"""

from __future__ import annotations

import os
import sys
import subprocess
import shutil
import re
import textwrap
import platform
from pathlib import Path

# ──────────────────────────────────────────────
# Terminal helpers (no external dependencies)
# ──────────────────────────────────────────────

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"
    GRAY = "\033[90m"


def supports_color() -> bool:
    """Return True if the terminal likely supports ANSI colors."""
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


USE_COLOR = supports_color()


def c(text: str, color: str) -> str:
    if not USE_COLOR:
        return text
    return f"{color}{text}{Colors.RESET}"


def clear() -> None:
    """Clear terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    """Print a styled header."""
    print(c(f" {title} ", Colors.BG_BLUE + Colors.WHITE + Colors.BOLD))
    print()


def print_help() -> None:
    """Print keyboard help bar."""
    print(c("[Enter]: Confirm  •  [Ctrl+C]: Cancel", Colors.GRAY))


def prompt_input(prompt_text: str, default: str = "", allow_empty: bool = False) -> str:
    """Prompt user for text input with optional default."""
    while True:
        if default:
            hint = c(default, Colors.YELLOW)
            user_input = input(f"{c('>>', Colors.CYAN)} {prompt_text} [{hint}]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{c('>>', Colors.CYAN)} {prompt_text}: ").strip()

        if not user_input and not allow_empty:
            print(c("Error: This field cannot be empty.", Colors.RED))
            continue
        return user_input


def prompt_yes_no(message: str, default_yes: bool = True) -> bool:
    """Prompt user with a yes/no question."""
    suffix = " [Y/n]" if default_yes else " [y/N]"
    while True:
        response = input(f"{c('?', Colors.YELLOW)} {message}{suffix}: ").strip().lower()
        if not response:
            return default_yes
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print(c("Please answer 'y' or 'n'.", Colors.RED))


def show_progress(message: str, percent: int) -> None:
    """Display a simple progress bar."""
    bar_length = 30
    filled = int(bar_length * percent / 100)
    bar = "█" * filled + "─" * (bar_length - filled)
    print(f"\r{c(bar, Colors.GREEN)} {percent:3d}%  {message}", end="", flush=True)


def show_error(msg: str) -> None:
    print(f"\n{c('Error:', Colors.RED)} {msg}")


def show_success(msg: str) -> None:
    print(f"{c('✓', Colors.GREEN)} {msg}")


def show_info(msg: str) -> None:
    print(f"{c('→', Colors.CYAN)} {msg}")


# ──────────────────────────────────────────────
# File templates
# ──────────────────────────────────────────────

def get_main_py(project_name: str) -> str:
    return textwrap.dedent(f'''\
        #!/usr/bin/env python3
        """{project_name} - main entry point."""


        def main() -> None:
            print("Hello from {project_name}!")


        if __name__ == "__main__":
            main()
    ''')


def get_gitignore() -> str:
    return textwrap.dedent('''\
        # Virtual environments
        .venv/
        venv/
        env/
        ENV/

        # Python
        __pycache__/
        *.py[cod]
        *$py.class
        *.so
        .Python
        build/
        develop-eggs/
        dist/
        downloads/
        eggs/
        .eggs/
        lib/
        lib64/
        parts/
        sdist/
        var/
        wheels/
        *.egg-info/
        .installed.cfg
        *.egg

        # Testing / coverage
        .pytest_cache/
        .coverage
        htmlcov/
        .tox/
        .nox/
        coverage.xml
        *.cover
        .hypothesis/

        # Type checkers / linters
        .mypy_cache/
        .ruff_cache/
        .pytype/

        # IDE / editors
        .idea/
        .vscode/
        *.swp
        *.swo
        *~

        # Environment / secrets
        .env
        .env.*
        !.env.example

        # OS
        .DS_Store
        Thumbs.db

        # Jupyter
        .ipynb_checkpoints/
    ''')


def get_readme(project_name: str) -> str:
    return textwrap.dedent(f'''\
        # {project_name}

        A short description of your project.

        ## Setup

        ```bash
        # Create & activate virtual environment (already done by newpy)
        source .venv/bin/activate   # Linux / macOS
        # .venv\\Scripts\\activate    # Windows

        # Install dependencies (if any)
        # pip install -r requirements.txt
        ```

        ## Usage

        ```bash
        python main.py
        ```

        ## License

        MIT
    ''')


def get_requirements() -> str:
    return textwrap.dedent('''\
        # Add your project dependencies here
        # Example:
        # requests>=2.31.0
    ''')


# ──────────────────────────────────────────────
# Core logic
# ──────────────────────────────────────────────

def create_venv(project_path: Path) -> bool:
    """Create a virtual environment. Prefer uv, fall back to stdlib venv."""
    venv_path = project_path / ".venv"

    if shutil.which("uv"):
        result = subprocess.run(
            ["uv", "venv", str(venv_path)],
            capture_output=True,
            text=True,
            cwd=project_path,
        )
        if result.returncode == 0:
            return True
        # fall through to venv if uv fails

    result = subprocess.run(
        [sys.executable, "-m", "venv", str(venv_path)],
        capture_output=True,
        text=True,
        cwd=project_path,
    )
    if result.returncode != 0:
        show_error(f"Failed to create virtual environment:\n{result.stderr.strip()}")
        return False
    return True


def init_git(project_path: Path, project_name: str) -> None:
    """Initialize git repo and make an initial commit if possible."""
    if not shutil.which("git"):
        show_info("Git not found — skipping repository initialization.")
        return

    try:
        subprocess.run(
            ["git", "init", "-q"],
            check=True,
            cwd=project_path,
            capture_output=True,
        )
        # Stage everything
        subprocess.run(
            ["git", "add", "."],
            check=True,
            cwd=project_path,
            capture_output=True,
        )
        # Initial commit (ignore failure if user.name/email not configured)
        result = subprocess.run(
            ["git", "commit", "-q", "-m", f"Initial commit: {project_name}"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            show_info("Git repo created (no initial commit — configure git user.name / user.email).")
        else:
            show_success("Git repository initialized with initial commit.")
    except subprocess.CalledProcessError:
        show_info("Could not fully initialize Git (continuing anyway).")


def activation_hint() -> str:
    """Return the correct activation command for the current OS."""
    if platform.system() == "Windows":
        return r".venv\Scripts\activate"
    return "source .venv/bin/activate"


def main() -> None:
    try:
        clear()
        print_header("newpy — Python Project Creator")
        print_help()
        print()

        # ── Step 1: Target Directory ──
        while True:
            target_dir = prompt_input(
                "Enter the target directory",
                default=str(Path.home()),
            )
            target_path = Path(target_dir).expanduser().resolve()

            if not target_path.is_dir():
                print(c(f"Directory does not exist: {target_path}", Colors.RED))
                continue
            if not os.access(target_path, os.W_OK):
                print(c(f"No write permission: {target_path}", Colors.RED))
                continue
            break

        # ── Step 2: Project Name ──
        while True:
            clear()
            print_header("newpy — Python Project Creator")
            print(f"Target: {c(str(target_path), Colors.YELLOW)}")
            print()

            project_name = prompt_input("Enter the project name", default="my_python_app")

            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", project_name):
                print(c(
                    "Invalid name! Must start with a letter and contain only "
                    "letters, numbers, hyphens, and underscores.",
                    Colors.RED,
                ))
                input("\nPress Enter to try again...")
                continue

            project_path = target_path / project_name

            if project_path.exists():
                if not project_path.is_dir():
                    print(c(f"A file named '{project_name}' already exists.", Colors.RED))
                    input("\nPress Enter to go back...")
                    continue

                if not prompt_yes_no(
                    f"Directory '{project_path}' already exists. Setup inside it?",
                    default_yes=False,
                ):
                    continue
            break

        # ── Optional extras ──
        clear()
        print_header("newpy — Python Project Creator")
        print(f"Project: {c(str(project_path), Colors.YELLOW)}\n")

        add_readme = prompt_yes_no("Create a README.md?", default_yes=True)
        add_requirements = prompt_yes_no("Create an empty requirements.txt?", default_yes=True)
        do_git = prompt_yes_no("Initialize a Git repository?", default_yes=True)

        # ── Step 3: Create project ──
        print()
        show_progress("Creating directory...", 10)
        project_path.mkdir(parents=True, exist_ok=True)

        show_progress("Creating virtual environment...", 30)
        if not create_venv(project_path):
            sys.exit(1)

        show_progress("Writing project files...", 55)

        # main.py
        (project_path / "main.py").write_text(get_main_py(project_name), encoding="utf-8")

        # .gitignore
        (project_path / ".gitignore").write_text(get_gitignore(), encoding="utf-8")

        if add_readme:
            (project_path / "README.md").write_text(get_readme(project_name), encoding="utf-8")

        if add_requirements:
            (project_path / "requirements.txt").write_text(get_requirements(), encoding="utf-8")

        show_progress("Finishing up...", 85)

        if do_git:
            init_git(project_path, project_name)

        show_progress("Done!", 100)
        print("\n")

        # ── Success message ──
        clear()
        print_header("newpy — Python Project Creator")
        print(f"\n{c('✓ Project created successfully!', Colors.GREEN)}\n")
        print(f"  Path: {c(str(project_path), Colors.YELLOW)}\n")
        print(c("  Quick Start:", Colors.CYAN))
        print(f"    cd {project_path}")
        print(f"    {activation_hint()}")
        print("    python main.py\n")

        if not shutil.which("uv"):
            print(c(
                "  Tip: Install 'uv' (https://github.com/astral-sh/uv) for much faster venvs next time.",
                Colors.GRAY,
            ))
            print()

        input("Press Enter to exit...")

    except KeyboardInterrupt:
        print(f"\n\n{c('Operation cancelled.', Colors.YELLOW)}")
        sys.exit(0)


if __name__ == "__main__":
    main()
