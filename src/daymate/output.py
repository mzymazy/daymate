"""输出层：把生成的日记写入本地 Markdown 文件"""
from datetime import datetime
from pathlib import Path

from .config import DIARY_DIR


def save_diary(markdown: str, date_str: str | None = None) -> Path:
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    DIARY_DIR.mkdir(parents=True, exist_ok=True)
    path = DIARY_DIR / f"{date_str}.md"
    path.write_text(markdown, encoding="utf-8")
    return path
