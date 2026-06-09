"""
Research Mode 仪表盘预览 — 独立模块，不依赖主应用。

用法（在项目根目录）:
    py -m streamlit run preview/research_dashboard_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ui.research_dashboard import (  # noqa: E402
    SAMPLE_RESEARCH_RESULT,
    render_research_dashboard,
)

st.set_page_config(
    page_title="Research Dashboard Preview",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <style>
    section.main > div.block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Research Mode · 科研专利化评估报告")
st.caption(
    "独立预览页（`src/ui/research_dashboard.py`）。主应用中 Research Mode 分析完成后已自动使用该报告布局。"
)

preset = st.selectbox(
    "示例研究主题",
    [
        "面向电动汽车的高效率固态电池电解质界面工程",
        "基于深度学习的医疗影像早期肿瘤筛查算法",
        "无人驾驶场景下的多传感器融合路径规划方法",
    ],
    index=0,
)

score_override = st.slider("调整 PPI 分数（预览用）", 35, 95, 76)

result = dict(SAMPLE_RESEARCH_RESULT)
result["patent_potential_score"] = score_override
if score_override >= 75:
    result["has_patent_potential"] = "高"
elif score_override >= 50:
    result["has_patent_potential"] = "中"
else:
    result["has_patent_potential"] = "低"

st.divider()
render_research_dashboard(
    result,
    topic_input=preset,
    mode_label="Research Mode",
)
