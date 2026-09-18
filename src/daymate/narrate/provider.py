"""LLM Provider 抽象：本地 Ollama 与 OpenAI 兼容 API 双后端"""
import requests


class OllamaProvider:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, system: str, user: str) -> str:
        resp = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "stream": False,
            },
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]


class OpenAIProvider:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def chat(self, system: str, user: str) -> str:
        url = (
            self.base_url
            if self.base_url.endswith("/chat/completions")
            else self.base_url + "/chat/completions"
        )
        resp = requests.post(
            url,
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def build_provider(cfg: dict):
    p = cfg["provider"]
    if p["backend"] == "ollama":
        return OllamaProvider(p["base_url"], p["model"])
    return OpenAIProvider(p["base_url"], p.get("api_key", ""), p["model"])


def check_provider(cfg: dict) -> tuple:
    """环境体检：返回 (ok: bool, message: str)"""
    p = cfg["provider"]
    if p["backend"] == "ollama":
        try:
            resp = requests.get(p["base_url"].rstrip("/") + "/api/tags", timeout=5)
            if resp.status_code != 200:
                return False, f"Ollama 服务未就绪（HTTP {resp.status_code}）"
            models = [m["name"] for m in resp.json().get("models", [])]
            if not any(p["model"] in m for m in models):
                return (
                    False,
                    f"模型 {p['model']} 未安装，请运行: ollama pull {p['model']}",
                )
            return True, f"Ollama 就绪（{p['model']}）"
        except Exception:
            return False, "无法连接 Ollama，请先启动: ollama serve"
    # openai 兼容后端
    if not p.get("api_key"):
        return False, "API Key 未配置，请运行 daymate setup"
    return True, f"云端 API 就绪（{p['model']}）"
