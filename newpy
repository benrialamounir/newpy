#!/usr/bin/env python3
"""
newpy - Python Project Scaffolder

Creates a Python project with virtual environment, main.py, .gitignore,
and initializes a Git repository. Works on any system with Python 3.
No external dependencies required.
"""

import os
import sys
import subprocess
import shutil
import re
import textwrap

# ──────────────────────────────────────────────
# Terminal helpers (no external dependencies)
# ──────────────────────────────────────────────

def clear():
    """Clear terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_header(title):
    """Print a colored-ish header using terminal escape codes."""
    print(f"\033[44;97m {title} \033[0m\n")


def print_help():
    """Print keyboard help bar."""
    print("\033[90m[Enter]: Confirm  •  [Ctrl+C]: Cancel  •  [Tab]: (not used, just type)\033[0m")


def prompt_input(prompt_text, default="", allow_empty=False):
    """Prompt user for text input with optional default."""
    while True:
        if default:
            user_input = input(f"\033[96m>>\033[0m {prompt_text} [\033[93m{default}\033[0m]: ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"\033[96m>>\033[0m {prompt_text}: ").strip()
        
        if not user_input and not allow_empty:
            print("\033[91mError: This field cannot be empty.\033[0m")
            continue
        return user_input


def prompt_yes_no(message, default_yes=True):
    """Prompt user with a yes/no question."""
    suffix = " [Y/n]" if default_yes else " [y/N]"
    while True:
        response = input(f"\033[33m?\033[0m {message}{suffix}: ").strip().lower()
        if not response:
            return default_yes
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("\033[91mPlease answer 'y' or 'n'.\033[0m")


def show_progress(message, percent):
    """Display a progress bar."""
    bar_length = 40
    filled = int(bar_length * percent / 100)
    bar = '█' * filled + '─' * (bar_length - filled)
    print(f"\r\033[92m{bar}\033[0m {percent:3d}%  {message}", end='', flush=True)


def show_error(msg):
    """Show error message."""
    print(f"\n\033[91mError: {msg}\033[0m")


def show_success(msg):
    """Show success message."""
    print(f"\033[92m✓\033[0m {msg}")


# ──────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────

def main():
    try:
        clear()
        print_header(" Python Project Creator ")
        print_help()
        print()

        # ── Step 1: Target Directory ──
        while True:
            target_dir = prompt_input("Enter the target directory", default=os.path.expanduser("~"))
            target_dir = os.path.abspath(os.path.expanduser(target_dir))

            if not os.path.isdir(target_dir):
                print(f"\033[91mDirectory does not exist: {target_dir}\033[0m")
                continue

            if not os.access(target_dir, os.W_OK):
                print(f"\033[91mNo write permission: {target_dir}\033[0m")
                continue
            break

        # ── Step 2: Project Name ──
        while True:
            clear()
            print_header(" Python Project Creator ")
            print(f"Target: \033[93m{target_dir}\033[0m")
            print()

            project_name = prompt_input("Enter the project name", default="my_python_app")

            if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
                print("\033[91mInvalid name! Use letters, numbers, hyphens, and underscores only.\033[0m")
                input("\nPress Enter to try again...")
                continue

            full_path = os.path.join(target_dir, project_name)

            # Check if directory exists
            if os.path.exists(full_path):
                if not os.path.isdir(full_path):
                    print(f"\033[91mA file named '{project_name}' already exists at that location.\033[0m")
                    input("\nPress Enter to go back...")
                    continue

                exists = prompt_yes_no(
                    f"Directory '{full_path}' already exists. Setup inside it?",
                    default_yes=True
                )
                if not exists:
                    continue
            break

        # ── Step 3: Create project ──
        print()
        show_progress("Creating directory...", 10)
        os.makedirs(full_path, exist_ok=True)

        show_progress("Creating virtual environment...", 30)

        # Try uv first, fall back to venv
        use_uv = shutil.which('uv') is not None
        venv_path = os.path.join(full_path, '.venv')
        
        if use_uv:
            result = subprocess.run(
                ['uv', 'venv', venv_path],
                capture_output=True, text=True, cwd=full_path
            )
        else:
            result = subprocess.run(
                [sys.executable, '-m', 'venv', venv_path],
                capture_output=True, text=True, cwd=full_path
            )

        if result.returncode != 0:
            show_error(f"Failed to create virtual environment:\n{result.stderr}")
            sys.exit(1)

        show_progress("Generating project files...", 55)

        # Write main.py
        main_py = textwrap.dedent(f'''\
            #!/usr/bin/env python3

            def main():
                print("Hello from {project_name}!")


            if __name__ == "__main__":
                main()
        ''')
        with open(os.path.join(full_path, 'main.py'), 'w') as f:
            f.write(main_py)

        show_progress("Creating .gitignore...", 70)

        gitignore = textwrap.dedent('''\
            .venv/
            __pycache__/
            *.pyc
            .env
        ''')
        with open(os.path.join(full_path, '.gitignore'), 'w') as f:
            f.write(gitignore)

        show_progress("Initializing Git repository...", 85)

        # Initialize Git
        if shutil.which('git') is not None:
            subprocess.run(
                ['git', 'init', '-q'],
                capture_output=True, cwd=full_path
            )
            show_progress("Git repository initialized.", 95)

        show_progress("Done!", 100)
        print("\n")

        # ── Success message ──
        clear()
        print_header(" Python Project Creator ")
        print(f"\n\033[92m✓ Project initialized successfully!\033[0m\n")
        print(f"  Path: \033[93m{full_path}\033[0m\n")
        print(f"  \033[96mQuick Start:\033[0m")
        print(f"    cd {full_path}")
        print(f"    source .venv/bin/activate")
        print(f"    python main.py\n")

        input("Press Enter to exit...")

    except KeyboardInterrupt:
        print("\n\n\033[93mOperation cancelled. No changes were made.\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()