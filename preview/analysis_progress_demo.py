"""
进度条小组件演示 — 独立运行，不依赖主应用。

用法（在项目根目录）:
    py -m streamlit run preview/analysis_progress_demo.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ui.analysis_progress import (  # noqa: E402
    inject_analysis_progress_styles,
    render_analysis_progress,
    run_with_progress,
)

st.set_page_config(page_title="分析进度条预览", layout="centered")

st.markdown(
    """
    <style>
    section.main > div.block-container { max-width: 720px; padding-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 分析进度条 · 组件预览")
st.caption("模拟点击「发送」后的全屏进度弹层；进度条满后进入分析结果（本页用成功提示模拟仪表盘跳转）。")

inject_analysis_progress_styles()

demo_mode = st.radio(
    "预览方式",
    ["静态快照（可调进度）", "模拟完整流程（约 5–6 秒）"],
    horizontal=True,
)

if demo_mode == "静态快照（可调进度）":
    pct = st.slider("进度", 0, 100, 42)
    render_analysis_progress(float(pct))
    st.info("拖动滑块查看不同进度下的样式。")
else:
    if st.session_state.get("demo_finished"):
        st.success("✓ 分析完成 — 主应用中将自动显示仪表盘界面。")
        if st.button("重新演示"):
            st.session_state.pop("demo_finished", None)
            st.rerun()
    else:
        st.markdown("点击下方按钮，体验发送后的进度弹层。")
        if st.button("▶ 模拟点击发送", type="primary", use_container_width=True):

            def fake_deepseek_call() -> dict:
                time.sleep(5.0)
                return {"patent_potential_score": 78}

            try:
                run_with_progress(fake_deepseek_call, tick_seconds=0.4)
                st.session_state.demo_finished = True
                st.rerun()
            except Exception as exc:
                st.error(f"模拟失败：{exc}")
