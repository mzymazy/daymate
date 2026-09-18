"""聚合层：把原始痕迹转成结构化摘要。纯本地规则，不调用任何LLM"""
from collections import Counter
from datetime import datetime
from pathlib import Path


def aggregate(events: list) -> dict:
    """events: [(ts, kind, detail, meta)] → 结构化摘要"""
    shell_cmds = [e for e in events if e[1] == "shell"]
    file_events = [e for e in events if e[1] == "file"]
    window_events = [e for e in events if e[1] == "window"]

    window_counter = Counter(e[2] for e in window_events)
    dir_counter = Counter(_parent_dir(e[2]) for e in file_events)

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "counts": {
            "shell": len(shell_cmds),
            "files": len(file_events),
            "windows": len(window_events),
        },
        "top_windows": window_counter.most_common(10),
        "top_dirs": dir_counter.most_common(10),
        "recent_shell": [e[2] for e in shell_cmds[-20:]],
        "recent_files": [e[2] for e in file_events[-15:]],
        "total_events": len(events),
    }


def _parent_dir(path: str) -> str:
    p = Path(path)
    parent = str(p.parent)
    return parent if parent != str(p) else path
