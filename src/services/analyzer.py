import json
import re
from typing import Any

from src.api.client import DeepSeekClient
from src.prompts.templates import (
    IDEA_SYSTEM_PROMPT,
    RESEARCH_SYSTEM_PROMPT,
    build_idea_prompt,
    build_research_prompt,
)


class PatentAnalyzer:
    def __init__(self, api_key: str | None = None):
        self.client = DeepSeekClient(api_key=api_key)

    def analyze_idea(self, idea: str) -> dict[str, Any]:
        raw = self.client.chat(IDEA_SYSTEM_PROMPT, build_idea_prompt(idea))
        return self._parse_json(raw)

    def analyze_research(self, content: str) -> dict[str, Any]:
        raw = self.client.chat(RESEARCH_SYSTEM_PROMPT, build_research_prompt(content))
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        text = raw.strip()
        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if fenced:
            text = fenced.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            return {
                "parse_error": True,
                "summary": "模型返回格式异常，以下为原始内容：",
                "raw_response": raw,
                "error": str(exc),
            }
