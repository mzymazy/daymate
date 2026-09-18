"""文件活动采集：按修改时间扫描用户目录（限定范围，跳过缓存/依赖目录）"""
import os
import time
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".cache", ".venv", "venv",
    "AppData", "$RECYCLE.BIN", "System Volume Information",
    "Program Files", "Program Files (x86)", "Windows", ".m2", ".gradle",
}


def scan_modified_files(dirs: list, since_ts: float, limit: int = 300) -> list:
    """返回 [(mtime, abs_path)]，按修改时间倒序"""
    results = []
    for d in dirs:
        root = Path(d).expanduser()
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [x for x in dirnames if x not in SKIP_DIRS]
            for fn in filenames:
                fp = Path(dirpath) / fn
                try:
                    mtime = fp.stat().st_mtime
                except OSError:
                    continue
                if mtime >= since_ts:
                    results.append((mtime, str(fp)))
                if len(results) >= limit:
                    break
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break
    results.sort(reverse=True)
    return results


def day_start_ts() -> float:
    """今天零点的时间戳"""
    now = time.localtime()
    return time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0, 0, 0, -1))
