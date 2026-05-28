"""Analysis progress overlay — teal modal + staged progress bar."""

from __future__ import annotations

import html
import threading
import time
from collections.abc import Callable
from typing import Any

import streamlit as st

TEAL = "#14b8a6"

PROGRESS_STAGES: list[tuple[int, str]] = [
    (12, "正在解析您的输入…"),
    (28, "正在连接 DeepSeek…"),
    (48, "正在分析技术领域与创新性…"),
    (68, "正在评估专利潜力与竞争态势…"),
    (86, "正在生成仪表盘数据…"),
    (96, "即将完成…"),
]


def inject_analysis_progress_styles() -> None:
    st.markdown(
        """
        <style>
        .pp-progress-host {
            margin: 0 !important;
            padding: 0 !important;
        }
        /* 遮罩须相对视口；祖先 transform（如 chat_area 入场动画）会截断 fixed */
        .stApp:has(.pp-progress-host) .st-key-chat_area,
        .stApp:has(.pp-progress-host) .st-key-input_card {
            transform: none !important;
        }

        .pp-progress-backdrop {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
            z-index: 999999;
            background: rgba(245, 245, 245, 0.72);
            backdrop-filter: blur(4px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            box-sizing: border-box;
        }
        .pp-progress-card {
            width: 100%;
            max-width: 380px;
            background: #ffffff;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.18);
            padding: 22px 24px 20px;
            box-sizing: border-box;
        }
        .pp-progress-brand {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: #0a0a0a;
            margin: 0 0 14px 0;
            line-height: 1.2;
        }
        .pp-progress-brand span { color: #14b8a6; }
        .pp-progress-track {
            height: 10px;
            background: #f3f4f6;
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .pp-progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #0d9488 0%, #14b8a6 55%, #2dd4bf 100%);
            transition: width 0.35s ease;
            box-shadow: 0 0 12px rgba(20, 184, 166, 0.45);
        }
        .pp-progress-pct {
            display: block;
            font-size: 1.4rem;
            font-weight: 800;
            color: #0a0a0a;
            line-height: 1;
            font-variant-numeric: tabular-nums;
            margin: 0 0 8px 0;
        }
        .pp-progress-steps {
            list-style: none;
            margin: 0;
            padding: 12px 0 0 0;
            border-top: 1px solid #f3f4f6;
        }
        .pp-progress-steps li {
            font-size: 0.78rem;
            color: #9ca3af;
            padding: 4px 0 4px 22px;
            position: relative;
        }
        .pp-progress-steps li::before {
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #e5e7eb;
        }
        .pp-progress-steps li.pp-step-done {
            color: #0d9488;
            font-weight: 500;
        }
        .pp-progress-steps li.pp-step-done::before {
            background: #14b8a6;
            box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2);
        }
        .pp-progress-steps li.pp-step-active {
            color: #0a0a0a;
            font-weight: 600;
        }
        .pp-progress-steps li.pp-step-active::before {
            background: #14b8a6;
            animation: pp-pulse 1.2s ease infinite;
        }
        @keyframes pp-pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(20, 184, 166, 0.5); }
            50% { box-shadow: 0 0 0 6px rgba(20, 184, 166, 0); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _step_class(step_cap: int, percent: float) -> str:
    if percent >= step_cap:
        return "pp-step-done"
    prev_caps = [c for c, _ in PROGRESS_STAGES]
    idx = prev_caps.index(step_cap)
    lower = prev_caps[idx - 1] if idx > 0 else 0
    if lower <= percent < step_cap:
        return "pp-step-active"
    return ""


def progress_overlay_html(percent: float) -> str:
    """HTML for full-screen progress overlay (0–100)."""
    pct = max(0.0, min(100.0, float(percent)))
    step_items = "".join(
        f'<li class="{_step_class(cap, pct)}">{html.escape(text)}</li>'
        for cap, text in PROGRESS_STAGES
    )
    return (
        f'<div class="pp-progress-host"><div class="pp-progress-backdrop">'
        f'<div class="pp-progress-card">'
        f'<p class="pp-progress-brand">Patent<span>Pilot</span></p>'
        f'<span class="pp-progress-pct">{pct:.0f}%</span>'
        f'<div class="pp-progress-track">'
        f'<div class="pp-progress-fill" style="width:{pct:.1f}%;"></div></div>'
        f'<ul class="pp-progress-steps">{step_items}</ul>'
        f"</div></div></div>"
    )


def render_analysis_progress(percent: float) -> None:
    """Render full-screen progress overlay. percent: 0–100."""
    st.markdown(progress_overlay_html(percent), unsafe_allow_html=True)


def run_with_progress(
    task: Callable[[], Any],
    *,
    placeholder: Any | None = None,
    tick_seconds: float = 0.35,
    cap_until_done: float = 92.0,
) -> Any:
    """
    Run blocking task while animating progress in one script run (no st.rerun).
    Updates a single st.empty() placeholder so the page does not fully refresh.
    Pass `placeholder` from main layout (outside chat_area) for full-viewport overlay.
    """
    inject_analysis_progress_styles()
    overlay = placeholder if placeholder is not None else st.empty()
    started = time.monotonic()
    progress = 0.0
    result: Any = None
    error: BaseException | None = None
    done = threading.Event()

    def worker() -> None:
        nonlocal result, error
        try:
            result = task()
        except BaseException as exc:
            error = exc
        finally:
            done.set()

    threading.Thread(target=worker, daemon=True).start()

    while not done.is_set():
        elapsed = time.monotonic() - started
        target = cap_until_done * (1.0 - pow(0.5, elapsed / 8.0))
        progress = min(cap_until_done, max(progress + 1.2, target))
        overlay.markdown(progress_overlay_html(progress), unsafe_allow_html=True)
        time.sleep(tick_seconds)

    overlay.markdown(progress_overlay_html(100.0), unsafe_allow_html=True)
    time.sleep(0.35)
    overlay.empty()

    if error is not None:
        raise error
    return result
