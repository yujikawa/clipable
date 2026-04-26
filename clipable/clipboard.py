from __future__ import annotations

import subprocess
import sys


def _run(cmd: list[str], input: str | None = None) -> str:
    result = subprocess.run(
        cmd,
        input=input,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise OSError(f"{cmd[0]}: {result.stderr.strip()}")
    return result.stdout


def _is_wsl() -> bool:
    try:
        with open("/proc/version") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def paste() -> str:
    if sys.platform == "darwin":
        return _run(["pbpaste"])

    if sys.platform == "win32":
        return _run(["powershell.exe", "-NoProfile", "-command", "Get-Clipboard"]).rstrip("\r\n")

    # Linux / WSL2
    if _is_wsl():
        return _run(["powershell.exe", "-NoProfile", "-command", "Get-Clipboard"]).rstrip("\r\n")

    for cmd in [
        ["xclip", "-selection", "clipboard", "-o"],
        ["xsel", "--clipboard", "--output"],
        ["wl-paste", "--no-newline"],
    ]:
        try:
            return _run(cmd)
        except (OSError, FileNotFoundError):
            continue

    raise OSError(
        "No clipboard command found. Install xclip, xsel, or wl-clipboard."
    )


def copy(text: str) -> None:
    if sys.platform == "darwin":
        _run(["pbcopy"], input=text)
        return

    if sys.platform == "win32":
        _run(["clip.exe"], input=text)
        return

    # Linux / WSL2
    if _is_wsl():
        _run(["clip.exe"], input=text)
        return

    for cmd in [
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["wl-copy"],
    ]:
        try:
            _run(cmd, input=text)
            return
        except (OSError, FileNotFoundError):
            continue

    raise OSError(
        "No clipboard command found. Install xclip, xsel, or wl-clipboard."
    )
