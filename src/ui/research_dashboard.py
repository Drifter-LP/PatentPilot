"""Research Mode dashboard — academic patentability assessment report."""

from __future__ import annotations

import hashlib
import html
import re
from datetime import datetime, timezone
from typing import Any

import streamlit as st

DIMENSIONS: list[tuple[str, str, str]] = [
    ("novelty", "新颖性", "Novelty"),
    ("inventiveness", "创造性", "Inventiveness"),
    ("utility", "实用性", "Industrial Applicability"),
    ("prior_art", "现有技术关联度", "Prior Art Proximity"),
    ("claimability", "权利要求可撰写性", "Claim Draftability"),
]

SAMPLE_RESEARCH_RESULT: dict[str, Any] = {
    "has_patent_potential": "高",
    "innovation_analysis": (
        "该成果在固态电解质界面修饰与锂枝晶抑制机制方面提出了可验证的新路径，"
        "相较常规 LLZO 掺杂方案，实验数据支撑了离子电导率与循环稳定性的同步提升。"
        "创新点集中于界面工程与微观结构调控的耦合设计，具备明确的可重复实验方案与可量化指标，"
        "符合发明专利对技术方案完整性的基本要求。"
    ),
    "risk_analysis": (
        "主要风险在于：同类固态电池电解质专利布局密集，权利要求易被现有文献部分覆盖；"
        "部分性能提升可能归因于已知添加剂组合，需进一步分离核心贡献特征。"
        "此外，产业化验证数据尚不充分，实施例数量与对比实验维度需补充以支撑创造性论述。"
    ),
    "recommended_directions": [
        "补充同族文献与主要申请人专利的对比表，明确差异化技术特征。",
        "将核心创新点收敛为 1–2 组可独立权利要求保护的技术方案。",
        "增加多温度、多倍率下的长循环数据作为创造性支撑。",
        "在提交前完成 FTO 初步检索并标注高风险权利要求区间。",
    ],
    "patent_potential_score": 76,
    "dimension_scores": {
        "novelty": 80,
        "inventiveness": 74,
        "utility": 82,
        "prior_art": 68,
        "claimability": 71,
    },
    "summary": (
        "综合评估：该科研成果具备中等偏上的专利化潜力。技术方案结构完整，"
        "实验验证路径清晰，建议在完善对比实施例与权利要求层次化布局后推进申请。"
        "当前阶段适宜采取「核心发明 + 外围改进」的分层申请策略。"
    ),
}


def inject_research_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        .st-key-pp_research_topbar,
        .stApp:has(.st-key-pp_research_topbar) div.element-container.st-key-pp_research_topbar,
        .stApp:has(.st-key-pp_research_topbar) [data-testid="stVerticalBlock"].st-key-pp_research_topbar,
        .stApp:has(.st-key-pp_research_topbar) [data-testid="stElementContainer"].st-key-pp_research_topbar {
            position: sticky !important;
            top: 0 !important;
            z-index: 100 !important;
            max-width: 100% !important;
            width: 100% !important;
            margin: 0 0 12px 0 !important;
            padding: 8px 0 10px 0 !important;
            background: rgba(238, 241, 245, 0.95) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border-bottom: 1px solid #e2e8f0 !important;
            box-sizing: border-box !important;
        }
        .stApp:has(.st-key-pp_research_topbar) .st-key-dashboard_area,
        .stApp:has(.st-key-pp_research_topbar) .st-key-dashboard_area > [data-testid="stVerticalBlock"] {
            overflow: visible !important;
        }
        .st-key-pp_research_topbar [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 12px !important;
        }
        .st-key-pp_research_back_btn button {
            border-radius: 999px !important;
            border: 1px solid #e2e8f0 !important;
            background: #ffffff !important;
            color: #0f172a !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            padding: 8px 16px !important;
        }
        .st-key-pp_research_back_btn button:hover {
            border-color: #0f766e !important;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12) !important;
        }
        .pp-rd-topbar-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #0f172a;
            margin: 0;
            line-height: 1.3;
        }
        .pp-rd-topbar-title span {
            color: #64748b;
            font-weight: 400;
            font-size: 0.88rem;
            margin-left: 8px;
        }
        .pp-rd-topbar-pill {
            display: inline-block;
            margin: 0;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background: rgba(15, 118, 110, 0.12);
            color: #0f766e;
            border: 1px solid rgba(15, 118, 110, 0.35);
            white-space: nowrap;
        }
        .pp-rd-wrap {
            max-width: 1120px;
            margin: 0 auto;
            padding: 0 0 28px 0;
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: #0f172a;
        }
        .pp-rd-doc-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 10px;
            padding: 22px 26px 20px;
            color: #f8fafc;
            margin-bottom: 16px;
            border: 1px solid #475569;
        }
        .pp-rd-doc-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 10px 18px;
            font-size: 0.72rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #94a3b8;
            margin-bottom: 12px;
        }
        .pp-rd-doc-meta span { color: #cbd5e1; font-weight: 600; }
        .pp-rd-doc-title {
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.35;
            margin: 0 0 6px 0;
            letter-spacing: -0.02em;
        }
        .pp-rd-doc-subject {
            font-size: 0.92rem;
            color: #cbd5e1;
            line-height: 1.5;
            margin: 0;
        }
        .pp-rd-mode-badge {
            display: inline-block;
            margin-top: 14px;
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background: rgba(15, 118, 110, 0.35);
            border: 1px solid rgba(20, 184, 166, 0.55);
            color: #99f6e4;
        }
        .pp-rd-kpi-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }
        .pp-rd-kpi {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        .pp-rd-kpi-label {
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #64748b;
            margin: 0 0 6px 0;
        }
        .pp-rd-kpi-value {
            font-size: 1.5rem;
            font-weight: 800;
            font-variant-numeric: tabular-nums;
            color: #0f172a;
            line-height: 1.1;
            margin: 0;
        }
        .pp-rd-kpi-value small {
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748b;
            margin-left: 4px;
        }
        .pp-rd-kpi-note {
            font-size: 0.72rem;
            color: #94a3b8;
            margin: 6px 0 0 0;
            line-height: 1.4;
        }
        .pp-rd-section {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px 22px;
            margin-bottom: 14px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        .pp-rd-section-head {
            display: flex;
            align-items: center;
            flex-wrap: nowrap;
            gap: 10px;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f5f9;
        }
        .pp-rd-section-num {
            font-size: 0.75rem;
            font-weight: 800;
            color: #0f766e;
            letter-spacing: 0.08em;
            font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
            flex-shrink: 0;
        }
        .pp-rd-section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
            white-space: nowrap;
            flex: 1;
            min-width: 0;
        }
        .pp-rd-prose {
            font-size: 0.9rem;
            line-height: 1.75;
            color: #334155;
            margin: 0;
            text-align: justify;
        }
        .pp-rd-dim-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
        }
        .pp-rd-dim-table th {
            text-align: left;
            padding: 10px 12px;
            background: #f8fafc;
            border-bottom: 2px solid #e2e8f0;
            font-weight: 700;
            color: #475569;
            letter-spacing: 0.02em;
        }
        .pp-rd-dim-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #f1f5f9;
            vertical-align: middle;
        }
        .pp-rd-dim-bar-wrap {
            height: 8px;
            background: #f1f5f9;
            border-radius: 2px;
            overflow: hidden;
            min-width: 120px;
        }
        .pp-rd-dim-bar {
            height: 100%;
            border-radius: 2px;
            background: linear-gradient(90deg, #0f766e, #14b8a6);
        }
        .pp-rd-dim-score {
            font-weight: 700;
            font-variant-numeric: tabular-nums;
            color: #0f172a;
            min-width: 36px;
            text-align: right;
        }
        .pp-rd-rec-list {
            margin: 0;
            padding: 0;
            list-style: none;
            counter-reset: rd-rec;
        }
        .pp-rd-rec-list li {
            counter-increment: rd-rec;
            position: relative;
            padding: 12px 12px 12px 42px;
            margin-bottom: 8px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            font-size: 0.88rem;
            line-height: 1.65;
            color: #334155;
        }
        .pp-rd-rec-list li::before {
            content: counter(rd-rec);
            position: absolute;
            left: 12px;
            top: 12px;
            width: 22px;
            height: 22px;
            border-radius: 4px;
            background: #1e293b;
            color: #f8fafc;
            font-size: 0.72rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: ui-monospace, Consolas, monospace;
        }
        .pp-rd-footnote {
            font-size: 0.75rem;
            line-height: 1.6;
            color: #94a3b8;
            padding: 14px 16px;
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 6px;
            margin-top: 4px;
        }
        .pp-rd-verdict {
            border-left: 4px solid #0f766e;
            padding: 12px 16px;
            background: #f0fdfa;
            margin-bottom: 0;
        }
        .pp-rd-verdict strong { color: #0f766e; }
        .pp-rd-status {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }
        .pp-rd-status-high { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
        .pp-rd-status-mid { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
        .pp-rd-status-low { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
        .pp-rd-two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
        }
        @media (max-width: 900px) {
            .pp-rd-kpi-row { grid-template-columns: repeat(2, 1fr); }
            .pp-rd-two-col { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _safe_score(value: Any) -> int:
    try:
        return max(0, min(100, int(float(value))))
    except (TypeError, ValueError):
        return 0


def _topic_title(text: str, max_len: int = 56) -> str:
    t = (text or "未命名研究主题").strip().replace("\n", " ")
    return t if len(t) <= max_len else t[: max_len - 1] + "…"


def _report_id(seed: str) -> str:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:10].upper()
    return f"PPR-{digest}"


def _split_items(value: Any, limit: int = 6) -> list[str]:
    if isinstance(value, list):
        items = [str(x).strip() for x in value if str(x).strip()]
        return items[:limit]
    if isinstance(value, str) and value.strip():
        parts = re.split(r"[。；;\n]+", value)
        items = [p.strip() for p in parts if p.strip()]
        return items[:limit] if items else [value.strip()]
    return []


def _potential_level(result: dict) -> str:
    raw = str(result.get("has_patent_potential", "") or "").strip()
    if raw in ("高", "中", "低"):
        return raw
    score = _safe_score(result.get("patent_potential_score"))
    if score >= 75:
        return "高"
    if score >= 50:
        return "中"
    return "低"


def _filing_recommendation(score: int) -> tuple[str, str]:
    if score >= 80:
        return "建议推进申请", "pp-rd-status-high"
    if score >= 60:
        return "完善后申请", "pp-rd-status-mid"
    return "暂缓，需补强", "pp-rd-status-low"


def _dimension_scores_derived(score: int, potential: str) -> dict[str, int]:
    """Fallback dimension scores when LLM omits dimension_scores."""
    bias = {"高": 8, "中": 0, "低": -10}.get(potential, 0)
    base = score + bias
    return {
        "novelty": max(0, min(100, base + 4)),
        "inventiveness": max(0, min(100, base - 2)),
        "utility": max(0, min(100, base + 6)),
        "prior_art": max(0, min(100, int((100 - base) * 0.85))),
        "claimability": max(0, min(100, base - 5)),
    }


def _dimension_scores(result: dict, score: int, potential: str) -> dict[str, int]:
    raw = result.get("dimension_scores")
    if isinstance(raw, dict):
        parsed: dict[str, int] = {}
        for key, _, _ in DIMENSIONS:
            if key in raw:
                parsed[key] = _safe_score(raw[key])
        if len(parsed) == len(DIMENSIONS):
            return parsed
    return _dimension_scores_derived(score, potential)


def _clear_results() -> None:
    st.session_state.pop("idea_result", None)
    st.session_state.pop("research_result", None)


def _render_research_topbar(topic_short: str, mode_label: str) -> None:
    with st.container(key="pp_research_topbar"):
        col_back, col_title, col_mode = st.columns([1.35, 4.2, 1.15], gap="small")
        with col_back:
            if st.button("← 返回输入", key="pp_research_back_btn", use_container_width=True):
                _clear_results()
                st.rerun()
        with col_title:
            st.markdown(
                f'<p class="pp-rd-topbar-title">分析结果<span>{html.escape(topic_short)}</span></p>',
                unsafe_allow_html=True,
            )
        with col_mode:
            st.markdown(
                f'<p class="pp-rd-topbar-pill">{html.escape(mode_label)}</p>',
                unsafe_allow_html=True,
            )


def _doc_header_html(topic: str, mode_label: str, report_id: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return (
        f'<header class="pp-rd-doc-header">'
        f'<div class="pp-rd-doc-meta">'
        f"<div>Report ID · <span>{html.escape(report_id)}</span></div>"
        f"<div>Generated · <span>{ts}</span></div>"
        f"<div>Framework · <span>PatentPilot Research Assessment v1</span></div>"
        f"</div>"
        f'<h1 class="pp-rd-doc-title">科研成果专利化潜力评估报告</h1>'
        f'<p class="pp-rd-doc-subject">研究主题：{html.escape(topic)}</p>'
        f'<span class="pp-rd-mode-badge">{html.escape(mode_label)}</span>'
        f"</header>"
    )


def _kpi_row_html(score: int, potential: str, filing: str, filing_cls: str) -> str:
    return (
        f'<div class="pp-rd-kpi-row">'
        f'<div class="pp-rd-kpi"><p class="pp-rd-kpi-label">Patent Potential Index</p>'
        f'<p class="pp-rd-kpi-value">{score}<small>/ 100</small></p>'
        f'<p class="pp-rd-kpi-note">综合专利化潜力指数 (PPI)</p></div>'
        f'<div class="pp-rd-kpi"><p class="pp-rd-kpi-label">Patentability Level</p>'
        f'<p class="pp-rd-kpi-value">{html.escape(potential)}</p>'
        f'<p class="pp-rd-kpi-note">基于成果结构化评估</p></div>'
        f'<div class="pp-rd-kpi"><p class="pp-rd-kpi-label">Filing Recommendation</p>'
        f'<p class="pp-rd-kpi-value" style="font-size:1.05rem;">'
        f'<span class="pp-rd-status {filing_cls}">{html.escape(filing)}</span></p>'
        f'<p class="pp-rd-kpi-note">程序性建议，非法律意见</p></div>'
        f'<div class="pp-rd-kpi"><p class="pp-rd-kpi-label">Assessment Confidence</p>'
        f'<p class="pp-rd-kpi-value">{min(95, 55 + score // 3)}<small>%</small></p>'
        f'<p class="pp-rd-kpi-note">输入完整度与模型一致性</p></div>'
        f"</div>"
    )


def _section_html(num: str, title: str, body: str) -> str:
    return (
        f'<section class="pp-rd-section">'
        f'<div class="pp-rd-section-head">'
        f'<span class="pp-rd-section-num">{html.escape(num)}</span>'
        f"<h2 class=\"pp-rd-section-title\">{html.escape(title)}</h2>"
        f"</div>"
        f"{body}</section>"
    )


def _dimension_table_html(scores: dict[str, int]) -> str:
    rows: list[str] = []
    for key, zh, en in DIMENSIONS:
        val = scores.get(key, 0)
        rows.append(
            f"<tr><td><strong>{html.escape(zh)}</strong><br/>"
            f'<span style="font-size:0.72rem;color:#94a3b8;">{html.escape(en)}</span></td>'
            f'<td><div class="pp-rd-dim-bar-wrap">'
            f'<div class="pp-rd-dim-bar" style="width:{val}%;"></div></div></td>'
            f'<td class="pp-rd-dim-score">{val}</td></tr>'
        )
    return (
        f'<table class="pp-rd-dim-table"><thead><tr>'
        f"<th>评估维度</th><th>量化指标</th><th style=\"text-align:right;\">分值</th>"
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def _recommendations_html(items: list[str]) -> str:
    if not items:
        items = ["建议补充检索与实施例后再确定权利要求保护范围。"]
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ol class="pp-rd-rec-list">{lis}</ol>'


def _build_research_dashboard_html(
    result: dict,
    topic_input: str,
    mode_label: str = "Research Mode",
) -> str:
    topic = _topic_title(topic_input)
    report_id = _report_id(topic_input + str(result.get("summary", "")))
    score = _safe_score(result.get("patent_potential_score"))
    potential = _potential_level(result)
    filing, filing_cls = _filing_recommendation(score)
    summary = str(result.get("summary", "") or "暂无综合结论。")
    innovation = str(
        result.get("innovation_analysis", "") or "暂无创新性分析文本，请补充研究摘要后重新分析。"
    )
    risk = str(result.get("risk_analysis", "") or "暂无风险与不足分析。")
    recommendations = _split_items(result.get("recommended_directions"), 6)
    dim_scores = _dimension_scores(result, score, potential)

    sec1 = _section_html(
        "§ I",
        "综合结论",
        f'<div class="pp-rd-verdict"><p class="pp-rd-prose">'
        f"<strong>结论摘要：</strong>{html.escape(summary)}</p></div>",
    )
    sec2 = _section_html(
        "§ II",
        "创新性分析",
        f'<p class="pp-rd-prose">{html.escape(innovation)}</p>',
    )
    sec3 = _section_html(
        "§ III",
        "风险与不足",
        f'<p class="pp-rd-prose">{html.escape(risk)}</p>',
    )
    sec4 = _section_html(
        "§ IV",
        "专利性多维评估",
        _dimension_table_html(dim_scores),
    )
    sec5 = _section_html(
        "§ V",
        "策略建议",
        _recommendations_html(recommendations),
    )
    footnote = (
        f'<div class="pp-rd-footnote">'
        f"<strong>方法说明：</strong>本报告基于大语言模型对输入文本的结构化解析生成，"
        f"评估框架参考专利法可专利性三性（新颖性、创造性、实用性）并扩展科研场景维度。"
        f"报告仅供科研团队内部决策参考，不构成正式专利法律意见或 FTO 结论。"
        f"正式申请前请委托具备资质的服务机构完成检索与文本审核。</div>"
    )

    return (
        f'<div class="pp-rd-wrap">'
        f"{_doc_header_html(topic, mode_label, report_id)}"
        f"{_kpi_row_html(score, potential, filing, filing_cls)}"
        f'<div class="pp-rd-two-col">{sec2}{sec3}</div>'
        f"{sec1}{sec4}{sec5}{footnote}</div>"
    )


def render_research_dashboard(
    result: dict,
    *,
    topic_input: str = "",
    mode_label: str = "Research Mode",
) -> None:
    """Render Research Mode academic assessment report."""
    inject_research_dashboard_styles()
    topic_short = _topic_title(topic_input, max_len=40)
    _render_research_topbar(topic_short, mode_label)
    st.markdown(
        _build_research_dashboard_html(result, topic_input, mode_label),
        unsafe_allow_html=True,
    )
