# Daymate — The AI companion that lives in your computer

> Your computer remembers everything you did today. Daymate reads those traces and writes you a story only the two of you understand.
>
> Run one command at the end of the day:

```
$ daymate analyze
Scanning your machine for traces...
Daymate is writing (37 commands, 12 file edits)...
Your diary is ready: ~/daymate-diary/2026-09-17.md
```

<p align="center">
  <img src="docs/demo.png" alt="Daymate in action" width="760">
</p>

## Why

You've probably seen this before:

- **A calendar** that turns your day into colored blocks.
- **A tracking app** that turns your life into a dashboard.
- **A "productivity report"** that grades you like a school.

Daymate is none of those. It reads the breadcrumbs your computer already keeps — shell commands, files you touched — aggregates them into a ~2KB summary on your machine, and asks a local LLM to write you 300–500 words about your day.

Not a work report. Not a productivity audit. It's a friend living in your terminal who actually looked at your day and has something honest to say about it.

## Why it's different

- **Zero-friction try**: `pip install daymate && daymate analyze`. No daemon, no config, no account.
- **Privacy by design**: all traces stay on your machine. The LLM only ever sees a ~2KB aggregated digest, never your raw logs.
- **No GPU required**: works with local Ollama *or* free-tier cloud APIs. `daymate setup` walks you through it in three steps.
- **Self-healing setup**: `daymate check` detects what's missing and tells you exactly what to do.

## Quick start

```bash
# 1. Install
pip install daymate

# 2. Pick a backend (local Ollama or any OpenAI-compatible API)
daymate setup

# 3. Health check (tells you what's missing)
daymate check

# 4. Write today's diary
daymate analyze
```

## Commands

| Command | What it does |
|---------|--------------|
| `daymate setup` | Interactive backend setup: local Ollama / OpenAI-compatible API |
| `daymate check` | Environment health check: backend, model, scan dirs |
| `daymate analyze` | Scan existing traces and write today's diary (try this first) |
| `daymate start` | Live companion mode: tracks window & file activity in background *(in development)* |
| `daymate wrap` | End the session and write the full diary *(in development)* |

## How it works

```
COLLECTION (local)         AGGREGATION (local)         GENERATION (local/cloud)
┌──────────────────┐      ┌──────────────────┐        ┌──────────────────┐
│ shell history    │      │                  │        │                  │
│ file mtimes      ├─────►│ rule-based       ├───────►│ LLM              │
│ window titles*   │      │ compress to ~2KB │        │ sees the digest  │
└──────────────────┘      └──────────────────┘        │ only             │
                                                       └──────────────────┘
```

Raw logs **never** reach the LLM. The aggregation layer runs local rules to compress a day into a structured digest (top windows, most-active dirs, recent commands), and the LLM writes from that digest alone.

## Honest limitations

- `analyze` mode reads your shell history file, which has **no timestamps** — it can't know exactly when a command ran, nor how long you stayed in a window. It takes the most recent commands as "today's traces."
- The full timeline experience — **live mode (`start`/`wrap`)** — is in development. That's Daymate's final form: polling the foreground window every 30s to see your real rhythm (deep work, interruptions, late-night grind).
- Scanning is strictly limited to your user directories, auto-skipping `node_modules`, `.git`, caches, and system dirs.

## Tech stack

Python 3.10+ · Typer · SQLite · Watchdog · Ollama / OpenAI-compatible API

## Roadmap

- [x] `analyze` mode: scan → aggregate → generate
- [x] `setup` / `check`: backend config & self-healing diagnostics
- [ ] `start` mode: live window/file tracking (30s polling)
- [ ] `wrap` mode: end-of-day full diary
- [ ] Weekly & monthly retrospectives
- [ ] Optional multi-device sync

## About the author

Built by a 40-year-old media professional who taught himself to code — no CS degree, no bootcamp, just stubbornness and late nights.

If you've ever felt *too old to start*, this project is the counterargument. Daymate exists because someone decided to learn at 40, not despite it.

## License

MIT
*（内容由AI生成，仅供参考）*
