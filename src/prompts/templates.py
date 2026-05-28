IDEA_SYSTEM_PROMPT = """你是一位创新成果专利导航助手，帮助用户在申请专利前评估创新 idea 的潜在价值与风险。
请基于通用技术常识进行分析，输出解释型、可理解的结论，而非法律级专利审查意见。
必须只返回合法 JSON，不要包含 markdown 代码块或其他说明文字。"""

RESEARCH_SYSTEM_PROMPT = """你是一位科研成果专利化潜力分析助手，帮助高校科研人员判断研究成果是否适合专利化。
请基于通用技术常识进行分析，输出解释型、可理解的结论，而非法律级专利审查意见。
必须只返回合法 JSON，不要包含 markdown 代码块或其他说明文字。"""


def build_idea_prompt(idea: str) -> str:
    return f"""请分析以下创新 idea：

「{idea}」

请返回 JSON，字段如下：
{{
  "technical_field": "所属技术领域",
  "innovation_crowding": {{
    "level": "低/中/高",
    "explanation": "创新拥挤度说明"
  }},
  "potential_risks": ["风险1", "风险2"],
  "breakthrough_directions": ["可突破方向1", "可突破方向2"],
  "patent_potential_score": 0,
  "summary": "总体结论，200字以内"
}}

patent_potential_score 为 0-100 的整数。"""


def build_research_prompt(content: str) -> str:
    return f"""请分析以下科研成果/论文摘要/项目描述：

「{content}」

请返回 JSON，字段如下：
{{
  "has_patent_potential": "高/中/低",
  "innovation_analysis": "创新性分析",
  "risk_analysis": "风险与不足分析",
  "recommended_directions": ["建议方向1", "建议方向2"],
  "patent_potential_score": 0,
  "summary": "总体结论，200字以内"
}}

patent_potential_score 为 0-100 的整数。"""
