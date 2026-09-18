"""配置管理：所有用户选择集中保存在 ~/.daymate/config.yaml"""
from pathlib import Path
import yaml

CONFIG_DIR = Path.home() / ".daymate"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DATA_DIR = CONFIG_DIR / "data"
DIARY_DIR = Path.home() / "daymate-diary"

DEFAULT_CONFIG = {
    "provider": {
        "backend": "ollama",          # ollama | openai
        "model": "qwen2.5:7b",
        "base_url": "http://localhost:11434",
        "api_key": "",
    },
    "collector": {
        "scan_dirs": ["~/Documents", "~/Desktop", "~/Downloads", "~/dev", "~/code"],
        "window_poll_interval": 30,
    },
}


def ensure_config() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DIARY_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)


def load_config() -> dict:
    ensure_config()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        cfg = {}
    merged = {**DEFAULT_CONFIG, **cfg}
    merged["provider"] = {**DEFAULT_CONFIG["provider"], **merged.get("provider", {})}
    merged["collector"] = {**DEFAULT_CONFIG["collector"], **merged.get("collector", {})}
    return merged


def save_config(cfg: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
