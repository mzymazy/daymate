"""提示词模板：让 LLM 只消费聚合摘要，永远不碰原始日志"""

SYSTEM_PROMPT = """你是一个住在用户电脑里的AI伙伴，名字叫Daymate。
你的任务：阅读用户一天的数字化痕迹摘要，把这一天写成一篇文章，让用户觉得"这一天被认真看见了"。

写作要求：
1. 用第二人称"你"称呼用户
2. 语气像朋友，具体、真实、有洞察；不煽情、不肉麻、不喊口号
3. 引用真实细节（文件名、命令、软件名），不空谈大词
4. 能看出一天里的节奏：专注时段、被打断的瞬间、深夜加班，自然带出即可
5. 结尾给一句真诚的话（提醒或肯定），不超过一句话
6. 全文 300-500 字，分 3-5 段，每段一个重点
7. 用中文写作"""


def build_user_prompt(summary: dict) -> str:
    return f"""以下是用户今天的数字足迹摘要：

日期：{summary['date']}
事件统计：终端命令 {summary['counts']['shell']} 条，文件活动 {summary['counts']['files']} 次

最常停留的窗口：
{_fmt_list(summary['top_windows'])}

最活跃的目录：
{_fmt_list(summary['top_dirs'])}

最近的终端命令：
{_fmt_lines(summary['recent_shell'])}

最近修改的文件：
{_fmt_lines(summary['recent_files'])}

请根据以上内容，写一篇关于用户今天的短文。"""


def _fmt_list(items: list) -> str:
    if not items:
        return "（无数据）"
    return "\n".join(f"- {k}（{v}次）" for k, v in items)


def _fmt_lines(items: list) -> str:
    if not items:
        return "（无数据）"
    return "\n".join(f"- {x}" for x in items)
