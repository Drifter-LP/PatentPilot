import json
import ssl
import urllib.error
import urllib.request
from typing import Any

from src.config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL


class DeepSeekClient:
    def __init__(self, api_key: str | None = None, api_url: str | None = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.api_url = api_url or DEEPSEEK_API_URL

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("未配置 API Key，请在侧边栏输入或设置环境变量 DEEPSEEK_API_KEY。")

        payload: dict[str, Any] = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        context = ssl._create_unverified_context()

        try:
            with urllib.request.urlopen(request, timeout=120, context=context) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API 请求失败 ({exc.code}): {detail}") from exc

        return data["choices"][0]["message"]["content"]
