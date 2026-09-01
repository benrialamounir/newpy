#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import re
import termios
import tty
from pathlib import Path


def clear():
    os.system("clear")


def raw_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            rest = sys.stdin.read(2)
            return ch + rest
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def form(prompt, default=""):
    text = default
    cursor = len(text)
    btn = 0
    while True:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write("newpy\n\n")
        sys.stdout.write(prompt + "\n")
        sys.stdout.write(text)
        sys.stdout.write("\n\n")
        if btn == 0:
            sys.stdout.write("[next]   cancel")
        else:
            sys.stdout.write(" next   [cancel]")
        sys.stdout.write("\n")
        row = 4
        col = cursor + 1
        sys.stdout.write("\033[" + str(row) + ";" + str(col) + "H")
        sys.stdout.flush()
        key = raw_key()
        if key == "\x03":
            raise KeyboardInterrupt
        if key == "\t":
            btn = 1 - btn
            continue
        if key in ("\r", "\n"):
            if btn == 1:
                raise KeyboardInterrupt
            return text
        if key in ("\x1b[A", "\x1b[B"):
            continue
        if key == "\x1b[D":
            if cursor > 0:
                cursor -= 1
            continue
        if key == "\x1b[C":
            if cursor < len(text):
                cursor += 1
            continue
        if key in ("\x7f", "\b"):
            if cursor > 0:
                text = text[:cursor - 1] + text[cursor:]
                cursor -= 1
            continue
        if len(key) == 1 and key.isprintable():
            text = text[:cursor] + key + text[cursor:]
            cursor += 1


def make_venv(path):
    venv = path / ".venv"
    if shutil.which("uv"):
        r = subprocess.run(["uv", "venv", str(venv)], capture_output=True, text=True, cwd=path)
        if r.returncode == 0:
            return True
    r = subprocess.run([sys.executable, "-m", "venv", str(venv)], capture_output=True, text=True, cwd=path)
    if r.returncode != 0:
        print("failed to create venv")
        print(r.stderr)
        return False
    return True


def main():
    try:
        while True:
            target = form("target directory", str(Path.home())).strip()
            target = Path(target).expanduser().resolve()
            if not target.is_dir():
                print("directory does not exist")
                raw_key()
                continue
            if not os.access(target, os.W_OK):
                print("no write permission")
                raw_key()
                continue
            break

        while True:
            name = form("project name", "my_python_app").strip()
            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
                print("invalid name")
                raw_key()
                continue
            path = target / name
            if path.exists() and not path.is_dir():
                print("a file with that name already exists")
                raw_key()
                continue
            break

        path.mkdir(parents=True, exist_ok=True)
        print("creating .venv ...")
        if not make_venv(path):
            sys.exit(1)

        (path / "main.py").write_text(
            "def main():\n    print(\"hello\")\n\n\nif __name__ == \"__main__\":\n    main()\n",
            encoding="utf-8",
        )
        (path / "requirements.txt").write_text("", encoding="utf-8")
        (path / ".gitignore").write_text(".venv/\n__pycache__/\n*.pyc\n.env\n", encoding="utf-8")

        clear()
        print("done")
        print()
        print(path)
        print()
        print("cd " + str(path))
        print("source .venv/bin/activate")
        print("python main.py")
        print()

    except KeyboardInterrupt:
        print("\ncancelled")
        sys.exit(0)


if __name__ == "__main__":
    main()
