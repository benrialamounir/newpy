#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import re
import textwrap
import termios
import tty
from pathlib import Path

def clear():
    os.system("clear")

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def ask(text, default=""):
    if default:
        ans = input(f"{text} [{default}]: ").strip()
        if not ans:
            return default
        return ans
    while True:
        ans = input(f"{text}: ").strip()
        if ans:
            return ans
        print("cannot be empty")

def yesno(text, default=True):
    options = ["yes", "no"]
    idx = 0 if default else 1
    while True:
        sys.stdout.write("\r\033[K")
        parts = []
        for i, opt in enumerate(options):
            if i == idx:
                parts.append(f"[{opt}]")
            else:
                parts.append(f" {opt} ")
        sys.stdout.write(f"{text}  {'  '.join(parts)}   (tab/arrows, enter)")
        sys.stdout.flush()
        key = getch()
        if key in ("\t", "\x1b[C", "\x1b[D", "\x1b[A", "\x1b[B"):
            idx = 1 - idx
        elif key in ("\r", "\n"):
            sys.stdout.write("\n")
            return idx == 0
        elif key.lower() == "y":
            sys.stdout.write("\n")
            return True
        elif key.lower() == "n":
            sys.stdout.write("\n")
            return False
        elif key == "\x03":
            raise KeyboardInterrupt

def main():
    try:
        clear()
        print("newpy")
        print()

        while True:
            target = ask("target directory", str(Path.home()))
            target = Path(target).expanduser().resolve()
            if not target.is_dir():
                print("directory does not exist")
                continue
            if not os.access(target, os.W_OK):
                print("no write permission")
                continue
            break

        while True:
            clear()
            print("newpy")
            print(f"target: {target}")
            print()
            name = ask("project name", "my_python_app")
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
                print("invalid name")
                input("press enter")
                continue
            path = target / name
            if path.exists():
                if not path.is_dir():
                    print("a file with that name already exists")
                    input("press enter")
                    continue
                if not yesno(f"{path} already exists, setup inside it?", False):
                    continue
            break

        clear()
        print("newpy")
        print(f"project: {path}")
        print()

        add_readme = yesno("create README.md?", True)
        do_git = yesno("init git?", True)

        print()
        print("creating...")

        path.mkdir(parents=True, exist_ok=True)

        venv = path / ".venv"
        ok = False
        if shutil.which("uv"):
            r = subprocess.run(["uv", "venv", str(venv)], capture_output=True, text=True, cwd=path)
            if r.returncode == 0:
                ok = True
        if not ok:
            r = subprocess.run([sys.executable, "-m", "venv", str(venv)], capture_output=True, text=True, cwd=path)
            if r.returncode != 0:
                print("failed to create venv")
                print(r.stderr)
                sys.exit(1)

        main_py = textwrap.dedent(f'''\
            #!/usr/bin/env python3

            def main():
                print("Hello from {name}!")

            if __name__ == "__main__":
                main()
        ''')
        (path / "main.py").write_text(main_py, encoding="utf-8")

        gitignore = textwrap.dedent('''\
            .venv/
            venv/
            env/
            __pycache__/
            *.py[cod]
            *$py.class
            *.so
            build/
            dist/
            *.egg-info/
            .pytest_cache/
            .coverage
            htmlcov/
            .mypy_cache/
            .ruff_cache/
            .idea/
            .vscode/
            .env
            .DS_Store
        ''')
        (path / ".gitignore").write_text(gitignore, encoding="utf-8")

        (path / "requirements.txt").write_text("", encoding="utf-8")

        if add_readme:
            readme = textwrap.dedent(f'''\
                # {name}

                ## Setup

                ```bash
                source .venv/bin/activate
                ```

                ## Run

                ```bash
                python main.py
                ```
            ''')
            (path / "README.md").write_text(readme, encoding="utf-8")

        if do_git and shutil.which("git"):
            subprocess.run(["git", "init", "-q"], cwd=path, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=path, capture_output=True)
            subprocess.run(["git", "commit", "-q", "-m", f"init {name}"], cwd=path, capture_output=True)

        clear()
        print("done")
        print()
        print(f"path: {path}")
        print()
        print("quick start:")
        print(f"  cd {path}")
        print("  source .venv/bin/activate")
        print("  python main.py")
        print()
        input("press enter to exit")

    except KeyboardInterrupt:
        print("\ncancelled")
        sys.exit(0)

if __name__ == "__main__":
    main()
