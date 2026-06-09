IDEA_SYSTEM_PROMPT = """你是一位创新成果专利导航助手，帮助用户在申请专利前评估创新 idea 的潜在价值与风险。
请基于通用技术常识进行分析，输出解释型、可理解的结论，而非法律级专利审查意见。
必须只返回合法 JSON，不要包含 markdown 代码块或其他说明文字。"""

RESEARCH_SYSTEM_PROMPT = """你是一位面向高校与科研机构的技术转移（TTO）顾问，擅长评估科研成果的专利化潜力。
请用严谨、客观、可验证的语言撰写分析，避免营销化或过度简化的表述。
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
  "innovation_analysis": "创新性分析（300字以内，需指出技术贡献点、与现有研究的差异及可验证性）",
  "risk_analysis": "风险与不足分析（300字以内，需涵盖现有技术、创造性支撑与实施例完整性）",
  "recommended_directions": ["具体可执行建议1", "具体可执行建议2", "具体可执行建议3"],
  "patent_potential_score": 0,
  "summary": "总体结论（200字以内，给出是否建议申请及关键前提）",
  "dimension_scores": {{
    "novelty": 0,
    "inventiveness": 0,
    "utility": 0,
    "prior_art": 0,
    "claimability": 0
  }}
}}

说明：
- patent_potential_score 为 0-100 的整数，表示综合专利化潜力指数 (PPI)。
- dimension_scores 各维度为 0-100 整数：novelty 新颖性、inventiveness 创造性、utility 实用性、
  prior_art 现有技术关联度（越高表示与现有技术越接近、风险越大）、claimability 权利要求可撰写性。
- recommended_directions 至少 3 条，面向科研团队后续行动。"""
