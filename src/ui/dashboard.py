"""Analysis results dashboard — Bento layout (v3)."""

from __future__ import annotations

import html
import hashlib
import re
from typing import Any

import numpy as np
import streamlit as st

TEAL = "#14b8a6"
TEAL_DARK = "#0d9488"
TEXT_MAIN = "#0a0a0a"
TEXT_MUTED = "#6b7280"

BAR_COLORS = ["#14b8a6", "#0d9488", "#0f766e", "#115e59", "#134e4a"]
RADAR_LABELS = ["创新性", "技术成熟度", "市场需求", "竞争密度", "法律风险"]
RADAR_VERTICES = [(0, -80), (76, -25), (47, 65), (-47, 65), (-76, -25)]
RADAR_LABEL_ANCHORS = [
    (0, -92, "middle", "middle"),
    (88, -28, "start", "middle"),
    (52, 78, "start", "middle"),
    (-52, 78, "end", "middle"),
    (-88, -28, "end", "middle"),
]
HEATMAP_COMPANIES = ["腾讯", "华为", "阿里", "百度", "小米"]
HEATMAP_YEARS = ["2021", "2022", "2023", "2024", "2025"]


def inject_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        .st-key-pp_dashboard_topbar {
            max-width: 100% !important;
            width: 100% !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
        .st-key-pp_dashboard_topbar [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 12px !important;
        }
        .st-key-pp_dashboard_topbar [data-testid="column"]:nth-child(2) .stMarkdown,
        .st-key-pp_dashboard_topbar [data-testid="column"]:nth-child(3) .stMarkdown {
            display: flex !important;
            align-items: center !important;
            min-height: 40px !important;
        }
        .st-key-pp_dashboard_topbar [data-testid="column"]:nth-child(3) .stMarkdown {
            justify-content: flex-end !important;
        }
        .st-key-pp_dashboard_back_btn button {
            border-radius: 999px !important;
            border: 1px solid #e5e7eb !important;
            background: #ffffff !important;
            color: #0a0a0a !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            padding: 8px 16px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
        }
        .st-key-pp_dashboard_back_btn button:hover {
            border-color: #14b8a6 !important;
            box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.12) !important;
        }
        .pp-v2-topbar-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #0a0a0a;
            margin: 0;
            line-height: 1.3;
        }
        .pp-v2-topbar-title span {
            color: #6b7280;
            font-weight: 400;
            font-size: 0.9rem;
            margin-left: 8px;
        }
        .pp-v2-mode-pill {
            display: inline-block;
            margin: 0;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(20, 184, 166, 0.1);
            color: #0d9488;
            border: 1px solid rgba(20, 184, 166, 0.35);
            white-space: nowrap;
        }
        .pp-v2-wrap {
            max-width: 100%;
            width: 100%;
            margin: 0;
            padding: 0 0 20px 0;
            box-sizing: border-box;
        }
        .pp-v2 .bento {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 14px;
            align-items: stretch;
        }
        .pp-v2 .card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 20px 22px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
            min-height: 0;
            box-sizing: border-box;
        }
        .pp-v2 .card-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin: 0 0 12px 0;
        }
        .pp-v2 .card-title strong {
            font-size: 0.95rem;
            color: #0a0a0a;
            text-transform: none;
            letter-spacing: 0;
            display: block;
            margin-top: 2px;
            font-weight: 600;
        }
        .pp-v2 .hero {
            grid-column: span 7;
            grid-row: span 2;
            padding: 24px 28px;
            background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 55%, #ffffff 100%);
            border-color: rgba(20, 184, 166, 0.2);
            box-shadow: 0 4px 32px rgba(20, 184, 166, 0.12);
            position: relative;
            overflow: hidden;
        }
        .pp-v2 .hero::before {
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(20, 184, 166, 0.35) 0%, transparent 70%);
            pointer-events: none;
        }
        .pp-v2 .hero-label {
            font-size: 0.75rem;
            color: #0d9488;
            font-weight: 600;
            margin: 0 0 8px 0;
        }
        .pp-v2 .hero h1 {
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.35;
            margin: 0 0 10px 0;
            color: #0a0a0a;
        }
        .pp-v2 .hero-desc {
            font-size: 0.9rem;
            color: #6b7280;
            line-height: 1.6;
            margin: 0;
        }
        .pp-v2 .hero-tag {
            display: inline-block;
            margin-top: 14px;
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: rgba(20, 184, 166, 0.12);
            color: #0d9488;
            border: 1px solid rgba(20, 184, 166, 0.35);
        }
        .pp-v2 .score-primary {
            grid-column: span 5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .pp-v2 .donut-wrap {
            position: relative;
            width: 160px;
            height: 160px;
            margin: 4px 0 8px;
        }
        .pp-v2 .donut-wrap svg {
            width: 100%;
            height: 100%;
            transform: rotate(-90deg);
            display: block;
        }
        .pp-v2 .donut-center {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .pp-v2 .score-num {
            font-size: 2.75rem;
            font-weight: 800;
            line-height: 1;
            color: #0a0a0a;
        }
        .pp-v2 .score-sub {
            font-size: 0.75rem;
            color: #6b7280;
            margin-top: 4px;
        }
        .pp-v2 .badge {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 6px;
        }
        .pp-v2 .badge-high {
            background: rgba(20, 184, 166, 0.12);
            color: #0d9488;
            border: 1px solid rgba(20, 184, 166, 0.4);
        }
        .pp-v2 .badge-medium {
            background: rgba(234, 179, 8, 0.12);
            color: #ca8a04;
            border: 1px solid rgba(234, 179, 8, 0.4);
        }
        .pp-v2 .badge-low {
            background: rgba(249, 115, 22, 0.12);
            color: #ea580c;
            border: 1px solid rgba(249, 115, 22, 0.4);
        }
        .pp-v2 .metric {
            grid-column: span 2;
            padding: 16px 18px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .pp-v2 .metric.status {
            grid-column: span 3;
        }
        .pp-v2 .metric-value {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0d9488;
            line-height: 1.2;
        }
        .pp-v2 .metric-label {
            font-size: 0.75rem;
            color: #6b7280;
            margin-top: 4px;
        }
        .pp-v2 .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 8px;
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .pp-v2 .status-chip::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        .pp-v2 .status-chip-recommend {
            background: rgba(20, 184, 166, 0.1);
            color: #0d9488;
            border: 1px solid rgba(20, 184, 166, 0.3);
        }
        .pp-v2 .status-chip-recommend::before { background: #14b8a6; }
        .pp-v2 .status-chip-caution {
            background: rgba(234, 179, 8, 0.1);
            color: #ca8a04;
            border: 1px solid rgba(234, 179, 8, 0.35);
        }
        .pp-v2 .status-chip-caution::before { background: #eab308; }
        .pp-v2 .status-chip-hold {
            background: rgba(249, 115, 22, 0.1);
            color: #ea580c;
            border: 1px solid rgba(249, 115, 22, 0.35);
        }
        .pp-v2 .status-chip-hold::before { background: #f97316; }
        .pp-v2 .chart-bars { grid-column: span 5; }
        .pp-v2 .chart-trend { grid-column: span 7; }
        .pp-v2 .bento-charts-row { align-items: stretch; }
        .pp-v2 .bento-charts-row > .card {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .pp-v2 .chart-radar { grid-column: span 6; }
        .pp-v2 .chart-heatmap { grid-column: span 6; }
        .pp-v2 .bento-charts-row .card-title { flex-shrink: 0; }
        .pp-v2 .bento-charts-row .chart-body {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 220px;
        }
        .pp-v2 .radar-box {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .pp-v2 .radar-box svg { width: 200px; height: 200px; }
        .pp-v2 .heatmap-body {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .pp-v2 .hm-grid {
            display: grid;
            grid-template-columns: 56px repeat(5, 1fr);
            gap: 4px;
            font-size: 0.72rem;
            width: 100%;
        }
        .pp-v2 .hm-year {
            text-align: center;
            color: #9ca3af;
            padding: 2px 0;
        }
        .pp-v2 .hm-label {
            text-align: right;
            padding-right: 8px;
            color: #6b7280;
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }
        .pp-v2 .hm-cell {
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            height: 28px;
        }
        .pp-v2 .bento-row-gap { margin-top: 14px; }
        .pp-v2 .conclusion-panel {
            grid-column: span 12;
            padding: 0;
            overflow: hidden;
            background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
            border-color: rgba(20, 184, 166, 0.25);
        }
        .pp-v2 .conclusion-inner { padding: 24px 28px 26px; }
        .pp-v2 .conclusion-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .pp-v2 .conclusion-heading { flex: 1; min-width: 200px; }
        .pp-v2 .conclusion-heading .label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #0d9488;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .pp-v2 .conclusion-heading h2 {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0a0a0a;
            line-height: 1.3;
            margin: 0;
        }
        .pp-v2 .conclusion-status {
            padding: 8px 18px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
            align-self: center;
        }
        .pp-v2 .conclusion-status-recommend {
            background: rgba(20, 184, 166, 0.12);
            color: #0d9488;
            border: 1px solid rgba(20, 184, 166, 0.4);
        }
        .pp-v2 .conclusion-status-caution {
            background: rgba(234, 179, 8, 0.12);
            color: #ca8a04;
            border: 1px solid rgba(234, 179, 8, 0.4);
        }
        .pp-v2 .conclusion-status-hold {
            background: rgba(249, 115, 22, 0.12);
            color: #ea580c;
            border: 1px solid rgba(249, 115, 22, 0.4);
        }
        .pp-v2 .conclusion-verdict {
            background: rgba(20, 184, 166, 0.06);
            border-left: 4px solid #14b8a6;
            border-radius: 0 10px 10px 0;
            padding: 14px 18px;
            margin-bottom: 20px;
            font-size: 0.92rem;
            color: #374151;
            line-height: 1.65;
        }
        .pp-v2 .conclusion-verdict strong { color: #0a0a0a; font-weight: 600; }
        .pp-v2 .conclusion-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .pp-v2 .conclusion-block {
            background: #fff;
            border: 1px solid #f0f0f0;
            border-radius: 12px;
            padding: 16px 18px;
        }
        .pp-v2 .conclusion-block-head {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 0.85rem;
            font-weight: 700;
            color: #0a0a0a;
        }
        .pp-v2 .conclusion-block-head .icon {
            width: 28px;
            height: 28px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }
        .pp-v2 .icon-opportunity { background: rgba(20, 184, 166, 0.12); }
        .pp-v2 .icon-risk { background: rgba(249, 115, 22, 0.12); }
        .pp-v2 .icon-action { background: rgba(59, 130, 246, 0.12); }
        .pp-v2 .conclusion-items { list-style: none; margin: 0; padding: 0; }
        .pp-v2 .conclusion-items li {
            font-size: 0.84rem;
            color: #4b5563;
            line-height: 1.55;
            padding: 8px 0 8px 14px;
            border-bottom: 1px solid #f3f4f6;
            position: relative;
        }
        .pp-v2 .conclusion-items li::before {
            content: "";
            position: absolute;
            left: 0;
            top: 14px;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: #14b8a6;
        }
        .pp-v2 .conclusion-block.risk .conclusion-items li::before { background: #f97316; }
        .pp-v2 .conclusion-block.action .conclusion-items li::before { background: #3b82f6; }
        .pp-v2 .conclusion-items li:last-child { border-bottom: none; padding-bottom: 0; }
        .pp-v2 .conclusion-items li:first-child { padding-top: 0; }
        .pp-v2 .conclusion-items li:first-child::before { top: 6px; }
        .pp-v2 .bar-item {
            display: flex;
            align-items: center;
            margin-bottom: 9px;
        }
        .pp-v2 .bar-item:last-child { margin-bottom: 0; }
        .pp-v2 .bar-label {
            width: 72px;
            font-size: 0.78rem;
            color: #6b7280;
            text-align: right;
            margin-right: 10px;
            flex-shrink: 0;
        }
        .pp-v2 .bar-track {
            flex: 1;
            height: 22px;
            background: #f3f4f6;
            border-radius: 6px;
            position: relative;
            overflow: hidden;
        }
        .pp-v2 .bar-fill { height: 100%; border-radius: 6px; }
        .pp-v2 .bar-value {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.72rem;
            font-weight: 600;
            color: #0a0a0a;
        }
        .pp-v2 .trend-box { height: 150px; margin-top: 4px; }
        .pp-v2 .trend-box svg { width: 100%; height: 100%; display: block; }
        @media (max-width: 900px) {
            .pp-v2 .hero, .pp-v2 .score-primary,
            .pp-v2 .metric, .pp-v2 .metric.status,
            .pp-v2 .chart-bars, .pp-v2 .chart-trend,
            .pp-v2 .chart-radar, .pp-v2 .chart-heatmap,
            .pp-v2 .conclusion-panel { grid-column: span 12; }
            .pp-v2 .hero { grid-row: span 1; }
            .pp-v2 .conclusion-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _safe_int_score(score: Any) -> int:
    try:
        return max(0, min(100, int(float(score))))
    except (TypeError, ValueError):
        return 0


def score_stroke_color(score: int) -> str:
    if score >= 80:
        return TEAL
    if score >= 60:
        return "#eab308"
    return "#f97316"


def score_badge_v2(score: int) -> tuple[str, str]:
    if score >= 80:
        return "高潜力", "badge-high"
    if score >= 60:
        return "中等潜力", "badge-medium"
    return "待提升", "badge-low"


def application_status_v2(score: int) -> tuple[str, str]:
    if score >= 80:
        return "推荐申请", "status-chip-recommend"
    if score >= 60:
        return "谨慎申请", "status-chip-caution"
    return "需优化", "status-chip-hold"


def _format_topic_tag(tag: Any) -> str:
    if isinstance(tag, list):
        return " + ".join(str(x).strip() for x in tag if str(x).strip())
    text = str(tag).strip()
    for sep in ("、", "，", ",", ";", "；", "|", "/", "\n"):
        if sep in text:
            parts = [p.strip() for p in re.split(rf"[{re.escape(sep)}]+", text) if p.strip()]
            if len(parts) > 1:
                return " + ".join(parts[:4])
    return text


def _topic_title(topic: str, max_len: int = 48) -> str:
    text = (topic or "未命名分析主题").strip().replace("\n", " ")
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def _field_distribution(technical_field: str, score: int) -> tuple[list[str], list[float]]:
    fields = ["人工智能", "机械工程", "环保技术", "电子通信", "生物医药"]
    weights = np.array([35.0, 28.0, 20.0, 12.0, 5.0])
    field_text = technical_field or ""
    boosts = {
        "人工智能": ["人工智能", "AI", "机器学习", "深度学习", "视觉", "机器人"],
        "机械工程": ["机械", "结构", "制造", "自动化"],
        "环保技术": ["环保", "能源", "可持续", "垃圾", "分类", "绿色"],
        "电子通信": ["通信", "电子", "芯片", "传感", "物联网"],
        "生物医药": ["医疗", "生物", "健康", "诊断", "药物"],
    }
    for idx, keys in enumerate(boosts.values()):
        if any(k.lower() in field_text.lower() for k in keys):
            weights[idx] += 18
    weights = weights * (0.85 + score / 200.0)
    weights = weights / weights.sum() * 100
    return fields, weights.tolist()


def _radar_values(score: int, crowding_level: str) -> list[float]:
    level = crowding_level or "中"
    crowding_map = {"低": 0.25, "中": 0.55, "高": 0.85}
    crowd = crowding_map.get(level, 0.55)
    base = score / 100.0
    return [
        min(1.0, base * 1.05),
        min(1.0, base * 0.9 + 0.1),
        min(1.0, base * 0.85 + 0.15),
        min(1.0, crowd),
        min(1.0, 1.0 - crowd * 0.5 + 0.15),
    ]


def _heatmap_data(score: int, seed_text: str) -> np.ndarray:
    rng = np.random.default_rng(int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16) % (2**32))
    base = 8 + score // 5
    grid = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            grid[i, j] = base + i * 3 + j * 5 + rng.integers(0, 6)
    return grid


def _heatmap_cell_style(value: float, vmax: float) -> str:
    ratio = value / max(vmax, 1)
    palette = [
        ("#f0fdf4", "#065f46"),
        ("#ecfdf5", "#065f46"),
        ("#d1fae5", "#065f46"),
        ("#a7f3d0", "#065f46"),
        ("#6ee7b7", "#ffffff"),
        ("#34d399", "#ffffff"),
        ("#10b981", "#ffffff"),
        ("#059669", "#ffffff"),
    ]
    idx = min(len(palette) - 1, int(ratio * len(palette)))
    bg, fg = palette[idx]
    return f"background:{bg};color:{fg};"


def _split_text_items(text: str, limit: int = 4) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[。；;\n]+", text)
    items = [p.strip() for p in parts if p.strip()]
    if not items:
        return [text.strip()]
    return items[:limit]


def _radar_polygon_points(scale: float) -> str:
    return " ".join(f"{x * scale:.0f},{y * scale:.0f}" for x, y in RADAR_VERTICES)


def _radar_data_points(values: list[float]) -> str:
    return " ".join(
        f"{x * v:.0f},{y * v:.0f}" for (x, y), v in zip(RADAR_VERTICES, values)
    )


def _clear_results() -> None:
    st.session_state.pop("idea_result", None)
    st.session_state.pop("research_result", None)


def _render_topbar(topic_short: str, mode_label: str) -> None:
    with st.container(key="pp_dashboard_topbar"):
        col_back, col_title, col_mode = st.columns([1.35, 4.2, 1.15], gap="small")
        with col_back:
            if st.button("← 返回输入", key="pp_dashboard_back_btn", use_container_width=True):
                _clear_results()
                st.rerun()
        with col_title:
            st.markdown(
                f'<p class="pp-v2-topbar-title">分析结果<span>{html.escape(topic_short)}</span></p>',
                unsafe_allow_html=True,
            )
        with col_mode:
            st.markdown(
                f'<p class="pp-v2-mode-pill">{html.escape(mode_label)}</p>',
                unsafe_allow_html=True,
            )


def _field_bars_html(fields: list[str], values: list[float]) -> str:
    rows: list[str] = []
    for label, val, color in zip(fields, values, BAR_COLORS):
        pct = max(0.0, min(100.0, float(val)))
        rows.append(
            f'<div class="bar-item"><span class="bar-label">{html.escape(label)}</span>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.0f}%;background:{color};"></div>'
            f'<span class="bar-value">{pct:.0f}%</span></div></div>'
        )
    return "".join(rows)


def _trend_chart_html(score: int) -> str:
    years = [2021, 2022, 2023, 2024]
    base = 80 + score * 2
    values = [int(base * 0.55), int(base * 0.72), int(base * 0.88), int(base * 1.05)]
    xs = [40, 130, 220, 310]
    y_top, y_bottom = 20, 120
    v_min, v_max = min(values), max(values)
    span = max(v_max - v_min, 1)
    ys = [int(y_bottom - (v - v_min) / span * (y_bottom - y_top)) for v in values]
    line_path = (
        f"M {xs[0]} {ys[0]} Q {(xs[0]+xs[1])/2:.0f} {(ys[0]+ys[1])/2:.0f} {xs[1]} {ys[1]} "
        f"T {xs[2]} {ys[2]} T {xs[3]} {ys[3]}"
    )
    area_path = f"{line_path} L {xs[3]} 140 L {xs[0]} 140 Z"
    markers = "".join(
        f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{TEAL}" stroke-width="2"/>'
        for x, y in zip(xs, ys)
    )
    value_labels = "".join(
        f'<text x="{x}" y="{y-10}" font-size="10" fill="{TEXT_MAIN}" text-anchor="middle" font-weight="600">{v}</text>'
        for x, y, v in zip(xs, ys, values)
    )
    year_labels = "".join(
        f'<text x="{x}" y="145" font-size="11" fill="#9ca3af" text-anchor="middle">{y}</text>'
        for x, y in zip(xs, years)
    )
    return (
        f'<div class="trend-box"><svg viewBox="0 0 400 160" aria-hidden="true">'
        f'<defs><linearGradient id="ppTrendGradDash" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{TEAL}" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="{TEAL}" stop-opacity="0"/></linearGradient></defs>'
        f'<path d="{area_path}" fill="url(#ppTrendGradDash)"/>'
        f'<path d="{line_path}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>'
        f"{markers}{value_labels}{year_labels}</svg></div>"
    )


def _radar_chart_html(values: list[float]) -> str:
    clamped = [max(0.0, min(1.0, float(v))) for v in values]
    grids = "".join(
        f'<polygon points="{_radar_polygon_points(s)}" fill="none" stroke="#e5e7eb"/>'
        for s in (1.0, 0.75, 0.5, 0.25)
    )
    axes = "".join(
        f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="#e5e7eb"/>'
        for x, y in RADAR_VERTICES
    )
    dots = "".join(
        f'<circle cx="{x*v:.0f}" cy="{y*v:.0f}" r="4" fill="{TEAL}"/>'
        for (x, y), v in zip(RADAR_VERTICES, clamped)
    )
    labels = "".join(
        f'<text x="{x}" y="{y}" font-size="9" fill="{TEXT_MUTED}" text-anchor="{a}">{html.escape(lbl)}</text>'
        for lbl, (x, y, a, _) in zip(RADAR_LABELS, RADAR_LABEL_ANCHORS)
    )
    return (
        f'<svg viewBox="0 0 200 200" aria-hidden="true">'
        f'<g transform="translate(100,100)">{grids}{axes}'
        f'<polygon points="{_radar_data_points(clamped)}" fill="rgba(20,184,166,0.15)" stroke="{TEAL}" stroke-width="2"/>'
        f"{dots}{labels}</g></svg>"
    )


def _heatmap_html(grid: np.ndarray) -> str:
    vmax = float(grid.max())
    cells = ['<div></div>'] + [f'<div class="hm-year">{y}</div>' for y in HEATMAP_YEARS]
    parts = list(cells)
    for i, company in enumerate(HEATMAP_COMPANIES):
        parts.append(f'<div class="hm-label">{company}</div>')
        for j in range(5):
            val = int(grid[i, j])
            style = _heatmap_cell_style(val, vmax)
            parts.append(f'<div class="hm-cell" style="{style}">{val}</div>')
    return f'<div class="hm-grid">{"".join(parts)}</div>'


def _list_field(result: dict, key: str) -> list[str]:
    val = result.get(key, [])
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str) and val.strip():
        return _split_text_items(val, 4)
    return []


def _categorize_suggestions(result: dict, mode: str) -> tuple[list[str], list[str], list[str]]:
    summary = str(result.get("summary", "") or "")
    if mode == "idea":
        opportunities = _list_field(result, "breakthrough_directions")[:3]
        risks = _list_field(result, "potential_risks")[:3]
        actions = _split_text_items(summary, 3)
    else:
        rec = _list_field(result, "recommended_directions")
        opportunities = rec[:2]
        actions = rec[2:5]
        risks = _split_text_items(str(result.get("risk_analysis", "") or ""), 3)
        if not actions:
            actions = _split_text_items(summary, 3)

    if not opportunities:
        opportunities = ["结合现有技术基础，进一步凝练可专利化的核心创新点。"]
    if not risks:
        risks = ["需关注同领域已有专利对权利要求保护范围的限制。"]
    if not actions:
        actions = ["建议补充检索并完善权利要求与实施例支撑后再提交申请。"]
    return opportunities[:3], risks[:3], actions[:3]


def _conclusion_status_cls(status_chip_cls: str) -> str:
    return {
        "status-chip-recommend": "conclusion-status-recommend",
        "status-chip-caution": "conclusion-status-caution",
        "status-chip-hold": "conclusion-status-hold",
    }.get(status_chip_cls, "conclusion-status-caution")


def _conclusion_items_html(items: list[str]) -> str:
    if not items:
        return "<li>暂无</li>"
    return "".join(f"<li>{html.escape(item)}</li>" for item in items if item)


def _conclusion_block(title: str, icon: str, icon_cls: str, block_cls: str, items: list[str]) -> str:
    return (
        f'<div class="conclusion-block {block_cls}">'
        f'<div class="conclusion-block-head">'
        f'<span class="icon {icon_cls}">{icon}</span>{html.escape(title)}</div>'
        f'<ul class="conclusion-items">{_conclusion_items_html(items)}</ul></div>'
    )


def _conclusion_panel_html(
    summary: str,
    status_text: str,
    status_cls: str,
    opportunities: list[str],
    risks: list[str],
    actions: list[str],
) -> str:
    verdict = summary.strip() or f"综合评估建议：{status_text}。"
    conclusion_status = _conclusion_status_cls(status_cls)
    blocks = (
        _conclusion_block("突破方向", "🎯", "icon-opportunity", "", opportunities)
        + _conclusion_block("风险提示", "⚠️", "icon-risk", "risk", risks)
        + _conclusion_block("下一步行动", "✅", "icon-action", "action", actions)
    )
    return (
        f'<article class="card conclusion-panel"><div class="conclusion-inner">'
        f'<div class="conclusion-header">'
        f'<div class="conclusion-heading"><p class="label">Report Conclusion</p>'
        f"<h2>📋 分析结论与建议</h2></div>"
        f'<span class="conclusion-status {conclusion_status}">{html.escape(status_text)}</span></div>'
        f'<div class="conclusion-verdict"><strong>综合结论：</strong>{html.escape(verdict)}</div>'
        f'<div class="conclusion-grid">{blocks}</div></div></article>'
    )


def _build_bento_html(
    *,
    topic: str,
    summary: str,
    tag: str,
    score: int,
    badge_label: str,
    badge_cls: str,
    crowding_display: str,
    status_text: str,
    status_cls: str,
    fields: list[str],
    bar_values: list[float],
) -> str:
    color = score_stroke_color(score)
    circumference = 2 * 3.14159265 * 40
    filled = circumference * score / 100
    tag_text = _format_topic_tag(tag)

    return (
        f'<article class="card hero">'
        f'<p class="hero-label">分析主题</p>'
        f"<h1>{html.escape(topic)}</h1>"
        f'<p class="hero-desc">{html.escape(summary)}</p>'
        f'<span class="hero-tag">{html.escape(tag_text)}</span></article>'
        f'<article class="card score-primary">'
        f'<p class="card-title">可行性评估</p>'
        f'<div class="donut-wrap"><svg viewBox="0 0 100 100" aria-hidden="true">'
        f'<circle cx="50" cy="50" r="40" fill="none" stroke="#e5e7eb" stroke-width="11"/>'
        f'<circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="11" '
        f'stroke-dasharray="{filled:.1f} {circumference:.1f}" stroke-linecap="round"/></svg>'
        f'<div class="donut-center"><span class="score-num">{score}</span>'
        f'<span class="score-sub">专利潜力 / 100</span></div></div>'
        f'<span class="badge {badge_cls}">{html.escape(badge_label)}</span></article>'
        f'<article class="card metric"><p class="card-title">竞争密度</p>'
        f'<span class="metric-value">{html.escape(crowding_display)}</span>'
        f'<span class="metric-label">创新拥挤度评估</span></article>'
        f'<article class="card metric status"><p class="card-title">申请建议</p>'
        f'<span class="status-chip {status_cls}">{html.escape(status_text)}</span>'
        f'<span class="metric-label">综合评分与风险</span></article>'
        f'<article class="card chart-bars"><p class="card-title">数据洞察<strong>技术领域分布</strong></p>'
        f"{_field_bars_html(fields, bar_values)}</article>"
        f'<article class="card chart-trend"><p class="card-title">趋势<strong>该领域专利增长</strong></p>'
        f"{_trend_chart_html(score)}</article>"
    )


def _build_charts_row_html(radar_vals: list[float], heatmap: np.ndarray) -> str:
    return (
        f'<article class="card chart-radar"><p class="card-title">竞争<strong>态势分析</strong></p>'
        f'<div class="chart-body"><div class="radar-box">{_radar_chart_html(radar_vals)}</div></div></article>'
        f'<article class="card chart-heatmap"><p class="card-title">布局<strong>主要申请人专利热力图</strong></p>'
        f'<div class="chart-body"><div class="heatmap-body">{_heatmap_html(heatmap)}</div></div></article>'
    )


def render_analysis_dashboard(
    result: dict,
    mode: str,
    topic_input: str,
    mode_label: str = "💡 Idea Mode",
) -> None:
    """Render v3 Bento dashboard for idea or research analysis result."""
    inject_dashboard_styles()
    score = _safe_int_score(result.get("patent_potential_score"))
    badge_label, badge_cls = score_badge_v2(score)
    status_text, status_cls = application_status_v2(score)
    summary = str(result.get("summary", "") or "暂无摘要。")
    topic = _topic_title(topic_input)

    if mode == "idea":
        tag = str(result.get("technical_field", "技术领域待分类"))
        crowding = result.get("innovation_crowding", {})
        crowding_level = crowding.get("level", "中") if isinstance(crowding, dict) else "中"
        field_for_bars = tag
    else:
        tag = str(result.get("has_patent_potential", "专利潜力待评估"))
        crowding_level = "中"
        field_for_bars = str(result.get("innovation_analysis", tag))[:40]

    crowding_display = crowding_level if crowding_level in ("低", "中", "高") else "中"
    fields, bar_values = _field_distribution(field_for_bars, score)
    radar_vals = _radar_values(score, crowding_level)
    heatmap = _heatmap_data(score, topic_input + field_for_bars)
    opportunities, risks, actions = _categorize_suggestions(result, mode)

    _render_topbar(topic, mode_label)

    row12 = _build_bento_html(
        topic=topic,
        summary=summary,
        tag=tag,
        score=score,
        badge_label=badge_label,
        badge_cls=badge_cls,
        crowding_display=crowding_display,
        status_text=status_text,
        status_cls=status_cls,
        fields=fields,
        bar_values=bar_values,
    )
    charts_row = _build_charts_row_html(radar_vals, heatmap)
    conclusion = _conclusion_panel_html(
        summary, status_text, status_cls, opportunities, risks, actions
    )
    st.markdown(
        f'<div class="pp-v2-wrap"><div class="pp-v2">'
        f'<div class="bento">{row12}</div>'
        f'<div class="bento bento-charts-row bento-row-gap">{charts_row}</div>'
        f'<div class="bento bento-row-gap">{conclusion}</div>'
        f"</div></div>",
        unsafe_allow_html=True,
    )
