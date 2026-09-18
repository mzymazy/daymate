"""Daymate CLI：start / wrap / analyze / setup / check"""
from datetime import datetime

import typer

from .aggregate import aggregate
from .collector import read_shell_history, scan_modified_files
from .collector.files import day_start_ts
from .config import load_config, save_config
from .narrate import prompt as prompt_tpl
from .narrate.provider import build_provider, check_provider
from .output import save_diary
from .store import add_events_batch, events_by_date

app = typer.Typer(add_completion=False)


@app.command()
def check():
    """环境体检：检测后端、模型、扫描目录是否就绪"""
    cfg = load_config()
    ok, msg = check_provider(cfg)
    if ok:
        typer.secho(f"[OK] {msg}", fg=typer.colors.GREEN)
    else:
        typer.secho(f"[FAIL] {msg}", fg=typer.colors.RED)
    dirs = [d for d in cfg["collector"]["scan_dirs"]]
    typer.secho(f"[INFO] 扫描目录: {', '.join(dirs)}", fg=typer.colors.CYAN)
    typer.secho(f"[INFO] 日记输出: ~/daymate-diary", fg=typer.colors.CYAN)
    if not ok:
        typer.secho("提示：运行 daymate setup 完成后端配置", fg=typer.colors.YELLOW)


@app.command()
def setup():
    """配置后端：本地 Ollama 或 OpenAI 兼容 API"""
    typer.secho("Daymate 需要一个大模型来写日记，选一个后端：", fg=typer.colors.CYAN)
    backend = typer.prompt("后端 (ollama / openai)", default="ollama")
    cfg = load_config()

    if backend == "ollama":
        base_url = typer.prompt("Ollama 地址", default="http://localhost:11434")
        model = typer.prompt("模型名", default="qwen2.5:7b")
        cfg["provider"] = {"backend": "ollama", "base_url": base_url, "model": model, "api_key": ""}
    else:
        base_url = typer.prompt("API 地址（OpenAI 兼容，如 https://api.deepseek.com/v1）")
        api_key = typer.prompt("API Key", hide_input=True)
        model = typer.prompt("模型名")
        cfg["provider"] = {"backend": "openai", "base_url": base_url, "api_key": api_key, "model": model}

    save_config(cfg)
    typer.secho("配置已保存。运行 daymate check 验证连接。", fg=typer.colors.GREEN)


@app.command()
def analyze(
    date: str = typer.Option(None, help="分析某天，格式 YYYY-MM-DD，默认今天"),
):
    """分析已有痕迹，生成一天的日记（零后台依赖，快速体验）"""
    cfg = load_config()
    date_str = date or datetime.now().strftime("%Y-%m-%d")

    typer.secho("正在扫描本机痕迹...", fg=typer.colors.CYAN)

    # 1. 采集：终端历史（历史文件无时间戳，取最近命令，如实对待）+ 文件修改（按今天0点过滤）
    cmds = read_shell_history(300)
    files = scan_modified_files(cfg["collector"]["scan_dirs"], day_start_ts(), limit=300)

    rows = []
    for c in cmds:
        rows.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "shell", c, ""))
    for mtime, path in files:
        ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        rows.append((ts, "file", path, ""))
    add_events_batch(rows)

    events = events_by_date(date_str)
    if not events:
        typer.secho("今天没有找到任何痕迹，先动起来再来见我。", fg=typer.colors.YELLOW)
        raise typer.Exit(0)

    # 2. 聚合（纯本地）
    summary = aggregate(events)

    # 3. 生成
    ok, msg = check_provider(cfg)
    if not ok:
        typer.secho(f"[FAIL] {msg}", fg=typer.colors.RED)
        typer.secho("运行 daymate setup 配置后端，或 daymate check 查看诊断。", fg=typer.colors.YELLOW)
        raise typer.Exit(1)

    typer.secho(f"正在请 Daymate 写作（{summary['counts']['shell']} 条命令，{summary['counts']['files']} 次文件活动）...", fg=typer.colors.CYAN)
    provider = build_provider(cfg)
    try:
        diary = provider.chat(prompt_tpl.SYSTEM_PROMPT, prompt_tpl.build_user_prompt(summary))
    except Exception as e:
        typer.secho(f"生成失败: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    path = save_diary(diary.strip(), date_str)
    typer.secho(f"今日日记已写好: {path}", fg=typer.colors.GREEN)


@app.command()
def start():
    """启动实时陪伴模式（后台记录窗口/文件活动，后续 wrap 生成日记）"""
    typer.secho("实时陪伴模式（start）正在开发中。", fg=typer.colors.YELLOW)
    typer.secho("当前可用：daymate analyze —— 直接分析已有痕迹生成日记。", fg=typer.colors.CYAN)


@app.command()
def wrap():
    """结束实时陪伴，生成今天的日记"""
    typer.secho("实时陪伴模式（wrap）正在开发中。", fg=typer.colors.YELLOW)
    typer.secho("当前可用：daymate analyze —— 直接分析已有痕迹生成日记。", fg=typer.colors.CYAN)


if __name__ == "__main__":
    app()
