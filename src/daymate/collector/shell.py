"""终端历史采集：读取本机已有的 Shell 历史，不注入、不修改"""
import os
from pathlib import Path


def read_powershell_history(limit: int = 500) -> list:
    """PowerShell PSReadLine 历史文件"""
    hist = (
        Path(os.environ.get("APPDATA", ""))
        / "Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt"
    )
    if not hist.exists():
        return []
    lines = [
        l.strip()
        for l in hist.read_text(encoding="utf-8", errors="ignore").splitlines()
        if l.strip()
    ]
    return lines[-limit:]


def read_bash_history(limit: int = 500) -> list:
    """Bash / Git Bash 历史"""
    hist = Path.home() / ".bash_history"
    if not hist.exists():
        return []
    lines = [
        l.strip()
        for l in hist.read_text(encoding="utf-8", errors="ignore").splitlines()
        if l.strip()
    ]
    return lines[-limit:]


def read_shell_history(limit: int = 500) -> list:
    """自动选择可用的历史来源"""
    cmds = read_powershell_history(limit) or read_bash_history(limit)
    return cmds
