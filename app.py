"""PatentPilot — AI 创新成果专利导航系统"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

SPLASH_HTML_PATH = Path(__file__).parent / "web" / "patentpilot_splash.html"
# 开场主内容区距视口顶部的距离（vh）；通过 fixed 定位生效
SPLASH_TOP_OFFSET_VH = 29
st.set_page_config(
    page_title="PatentPilot",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "app_started" not in st.session_state:
    st.session_state.app_started = False
def _load_splash_html_for_streamlit() -> str:
    """读取原始 HTML，运行时注入 Streamlit 兼容样式（不修改磁盘文件）。"""
    splash_html = SPLASH_HTML_PATH.read_text(encoding="utf-8")
    streamlit_overrides = """
<style>
/* iframe 内仅保留品牌 + Slogan；按钮与底部小字由 Streamlit 层渲染 */
@keyframes splashFadeInUp {
    from { transform: translateY(30px); }
    to { transform: translateY(0); }
}
body {
    min-height: auto !important;
    height: auto !important;
    display: block !important;
    background: transparent !important;
    overflow: hidden !important;
}
.bg-decoration,
.footer-text,
.cta-button {
    display: none !important;
}
.splash-container {
    padding: 0 20px !important;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}
.brand {
    /* 固定 rem，避免 iframe 宽度变化时 12vw 导致点击瞬间变大 */
    font-size: 6rem !important;
    line-height: 1.1 !important;
    margin-bottom: 12px !important;
    opacity: 1 !important;
    animation: splashFadeInUp 1s ease-out 0.2s both !important;
}
.slogan {
    font-size: 1.35rem !important;
    line-height: 1.55 !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    max-width: 640px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    opacity: 1 !important;
    margin-bottom: 0 !important;
    animation: splashFadeInUp 1s ease-out 0.6s both !important;
}
</style>
"""
    return splash_html.replace("</head>", streamlit_overrides + "</head>")


def render_splash_page() -> None:
    """首屏开场页：HTML 展示品牌区，st.button 样式对齐参考稿 CTA。"""
    st.markdown(
        '<div class="pp-splash-mode" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        footer {
            display: none !important;
        }

        .stApp {
            background-color: #f5f5f5 !important;
        }

        .pp-splash-mode {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

        .stApp:has(.pp-splash-mode) .st-key-splash_stack,
        .stApp:has(.pp-splash-mode) .st-key-splash_footer,
        .stApp:has(.pp-splash-mode) .pp-splash-footer {
            transition: opacity 0.4s ease !important;
        }

        /* 开场页：固定一屏，禁止上下滚动 */
        .stApp:has(.pp-splash-mode) {
            height: 100dvh !important;
            max-height: 100dvh !important;
            overflow: hidden !important;
            overscroll-behavior: none !important;
        }

        .stApp:has(.pp-splash-mode) [data-testid="stAppViewContainer"],
        .stApp:has(.pp-splash-mode) section.main,
        .stApp:has(.pp-splash-mode) [data-testid="stMainBlockContainer"],
        .stApp:has(.pp-splash-mode) section.main > div.block-container {
            height: 100dvh !important;
            max-height: 100dvh !important;
            min-height: 0 !important;
            overflow: hidden !important;
            overscroll-behavior: none !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        .stApp:has(.pp-splash-mode) [data-testid="stMainBlockContainer"] > div {
            overflow: hidden !important;
            max-height: 100dvh !important;
            min-height: 0 !important;
        }

        .stApp::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            pointer-events: none;
            z-index: 0;
            background: radial-gradient(
                circle at 30% 30%,
                rgba(20, 184, 166, 0.04) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 70% 70%,
                rgba(20, 184, 166, 0.03) 0%,
                transparent 50%
            );
            animation: ppSplashSlowRotate 30s linear infinite;
        }

        .stApp::after {
            content: '';
            position: fixed;
            pointer-events: none;
            z-index: 0;
            border-radius: 50%;
            background: rgba(20, 184, 166, 0.08);
            width: 200px;
            height: 200px;
            top: 10%;
            left: 10%;
            animation: ppSplashFloat 6s ease-in-out infinite;
        }

        .pp-splash-dot-b,
        .pp-splash-dot-c {
            position: fixed;
            pointer-events: none;
            z-index: 0;
            border-radius: 50%;
            background: rgba(20, 184, 166, 0.08);
            animation: ppSplashFloat 6s ease-in-out infinite;
        }

        .pp-splash-dot-b {
            width: 150px;
            height: 150px;
            top: 60%;
            right: 15%;
            animation-delay: 2s;
        }

        .pp-splash-dot-c {
            width: 100px;
            height: 100px;
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes ppSplashSlowRotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        @keyframes ppSplashFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-20px) scale(1.05); }
        }

        section.main {
            position: relative;
            z-index: 1;
        }

        section.main [data-testid="stVerticalBlock"]:has(.st-key-splash_get_started) {
            width: 100% !important;
            align-items: stretch !important;
        }

        section.main [data-testid="stHorizontalBlock"]:has(.st-key-splash_get_started) {
            width: 100% !important;
            justify-content: center !important;
        }

        section.main [data-testid="stElementContainer"]:has(
            iframe[title="streamlit_components_v1.components.html"]
        ),
        section.main [data-testid="stElementContainer"]:has(iframe[title="st.iframe"]) {
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe[title="streamlit_components_v1.components.html"],
        iframe[title="st.iframe"] {
            width: 100%;
            height: 215px;
            min-height: unset;
            border: none;
            display: block;
            margin: 0 auto;
        }

        section.main [data-testid="column"]:has(.st-key-splash_get_started) {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }

        .stApp:has(.pp-splash-mode) .st-key-splash_stack {
            gap: 0 !important;
            row-gap: 0 !important;
            align-items: center !important;
        }

        .st-key-splash_get_started {
            margin-top: 24px !important;
            width: 100% !important;
            padding: 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        .st-key-splash_get_started [data-testid="stVerticalBlock"],
        .st-key-splash_get_started [data-testid="stElementContainer"] {
            width: auto !important;
            margin: 0 auto !important;
            padding: 0 !important;
            display: flex !important;
            justify-content: center !important;
        }

        .st-key-splash_get_started [data-testid="stButton"] {
            margin: 0 auto !important;
            display: flex !important;
            justify-content: center !important;
            width: auto !important;
        }

        .st-key-splash_get_started [data-testid="stButton"] > button {
            margin: 0 auto !important;
        }

        .st-key-splash_get_started button,
        .st-key-splash_get_started button[kind="primary"],
        .st-key-splash_get_started button[kind="secondary"] {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            width: auto !important;
            min-height: unset !important;
            background: #171717 !important;
            background-color: #171717 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 16px 40px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
        }

        .st-key-splash_get_started button p,
        .st-key-splash_get_started button span,
        .st-key-splash_get_started button div {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #ffffff !important;
        }

        .st-key-splash_get_started button::after {
            content: "";
            display: inline-block;
            width: 18px;
            height: 18px;
            flex-shrink: 0;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23ffffff' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M17 8l4 4m0 0l-4 4m4-4H3'/%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            transition: transform 0.3s ease;
        }

        .st-key-splash_get_started button:hover,
        .st-key-splash_get_started button:focus-visible {
            background: #14b8a6 !important;
            background-color: #14b8a6 !important;
            border: none !important;
            color: #ffffff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(20, 184, 166, 0.3) !important;
        }

        .st-key-splash_get_started button:hover::after,
        .st-key-splash_get_started button:focus-visible::after {
            transform: translateX(4px);
        }

        .st-key-splash_get_started button:active {
            background: #14b8a6 !important;
            background-color: #14b8a6 !important;
            transform: translateY(0) !important;
            box-shadow: 0 4px 16px rgba(20, 184, 166, 0.25) !important;
        }

        .pp-splash-footer {
            width: 100%;
            margin: 0;
            padding: 0;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            font-size: 0.85rem;
            line-height: 1.55;
            color: #9ca3af;
            pointer-events: none;
        }

        .stApp:has(.pp-splash-mode) [data-testid="stVerticalBlock"].st-key-splash_footer,
        .stApp:has(.pp-splash-mode) .stVerticalBlock.st-key-splash_footer {
            position: fixed !important;
            bottom: 40px !important;
            left: 50% !important;
            right: auto !important;
            transform: translateX(-50%) !important;
            width: min(640px, calc(100vw - 2rem)) !important;
            max-width: 640px !important;
            margin: 0 !important;
            padding: 0 16px !important;
            z-index: 10 !important;
            box-sizing: border-box !important;
            pointer-events: none !important;
            text-align: center !important;
        }

        .stApp:has(.pp-splash-mode) .st-key-splash_footer [data-testid="stElementContainer"],
        .stApp:has(.pp-splash-mode) .st-key-splash_footer .stMarkdown,
        .stApp:has(.pp-splash-mode) .st-key-splash_footer [data-testid="stMarkdownContainer"] {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: center !important;
            display: block !important;
        }

        @media (max-width: 640px) {
            iframe[title="streamlit_components_v1.components.html"],
            iframe[title="st.iframe"] {
                height: 185px;
            }

            .st-key-splash_get_started button {
                padding: 14px 32px !important;
                font-size: 0.95rem !important;
            }

            .stApp:has(.pp-splash-mode) [data-testid="stVerticalBlock"].st-key-splash_footer,
            .stApp:has(.pp-splash-mode) .stVerticalBlock.st-key-splash_footer {
                bottom: 24px !important;
                font-size: 0.78rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pp-splash-dot-b" aria-hidden="true"></div>'
        '<div class="pp-splash-dot-c" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    with st.container(key="splash_stack"):
        try:
            components.html(_load_splash_html_for_streamlit(), height=215, scrolling=False)
        except Exception as exc:
            st.error(f"开场页加载失败：{exc}")
            st.stop()

        _, btn_col, _ = st.columns([1, 1, 1], gap="small")
        with btn_col:
            if st.button(
                "Get Started",
                key="splash_get_started",
                use_container_width=False,
                type="primary",
            ):
                st.session_state.app_started = True
                st.rerun()

    with st.container(key="splash_footer"):
        st.markdown(
            '<p class="pp-splash-footer">面向小白创新者与专业科研人员的专利潜力初筛工具 · 非正式法律意见</p>',
            unsafe_allow_html=True,
        )

    top_vh = SPLASH_TOP_OFFSET_VH
    mobile_top_vh = max(14, top_vh - 2)
    st.markdown(
        f"""
        <style>
        /* 整块 fixed：key 在 stVerticalBlock 上，非 element-container */
        .stApp:has(.pp-splash-mode) [data-testid="stVerticalBlock"].st-key-splash_stack,
        .stApp:has(.pp-splash-mode) .stVerticalBlock.st-key-splash_stack {{
            position: fixed !important;
            top: {top_vh}vh !important;
            left: 50% !important;
            right: auto !important;
            transform: translateX(-50%) !important;
            width: min(800px, calc(100vw - 2rem)) !important;
            max-width: 800px !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 10 !important;
            pointer-events: auto !important;
            box-sizing: border-box !important;
        }}

        .stApp:has(.pp-splash-mode) .st-key-splash_get_started button {{
            pointer-events: auto !important;
            cursor: pointer !important;
        }}

        @media (max-width: 640px) {{
            .stApp:has(.pp-splash-mode) [data-testid="stVerticalBlock"].st-key-splash_stack,
            .stApp:has(.pp-splash-mode) .stVerticalBlock.st-key-splash_stack {{
                top: {mobile_top_vh}vh !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


def inject_main_app_styles() -> None:
    """主应用样式 — 严格对齐 patentpilot_main_preview.html。"""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5f5 !important;
            color: #0a0a0a;
        }

        @keyframes ppMainEnter {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .stApp:not(:has(.pp-splash-mode)) [data-testid="stSidebar"],
        .stApp:not(:has(.pp-splash-mode)) .st-key-chat_area,
        .stApp:not(:has(.pp-splash-mode)) .st-key-input_card {
            animation: ppMainEnter 0.45s ease both;
        }

        [data-testid="stSidebar"] {
            background-color: #1a1a1a !important;
            border-right: none !important;
            min-width: 260px !important;
            max-width: 260px !important;
            width: 260px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background-color: #1a1a1a !important;
            padding: 16px !important;
        }

        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .pp-section-title {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #9ca3af !important;
            margin: 0 0 12px 0;
            padding-left: 8px;
        }

        [data-testid="stSidebar"] .pp-sidebar-brand {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff !important;
            margin-bottom: 24px;
            padding: 8px 0;
        }

        [data-testid="stSidebar"] .pp-sidebar-brand span {
            color: #14b8a6 !important;
        }

        [data-testid="stSidebar"] .pp-sidebar-footer {
            font-size: 0.75rem;
            color: #6b7280 !important;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        [data-testid="stSidebar"] .pp-history-item {
            font-size: 0.85rem;
            color: #d1d5db !important;
            padding: 6px 8px;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .st-key-new_analysis_btn button {
            background: #14b8a6 !important;
            background-color: #14b8a6 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            box-sizing: border-box !important;
            padding: 0 16px !important;
            min-height: 36px !important;
            max-height: 36px !important;
            height: 36px !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
            width: 100% !important;
            margin-bottom: 24px !important;
        }

        .st-key-new_analysis_btn button:hover {
            background: #0d9488 !important;
            background-color: #0d9488 !important;
            border: none !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"],
        [data-testid="stSidebar"] .st-key-analysis_mode,
        [data-testid="stSidebar"] .st-key-analysis_mode [data-testid="stRadio"] {
            width: 100% !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] > label {
            display: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] > div {
            display: flex !important;
            flex-direction: column !important;
            gap: 3px !important;
            width: 100% !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {
            display: flex !important;
            align-items: center !important;
            gap: 10px;
            width: 100% !important;
            box-sizing: border-box !important;
            padding: 0 16px !important;
            min-height: 36px !important;
            max-height: 36px !important;
            height: 36px !important;
            border-radius: 10px !important;
            margin: 0 !important;
            background: transparent !important;
            background-color: transparent !important;
            color: #ffffff !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            line-height: 1.2 !important;
            border: none !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] span,
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] div {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            background: transparent !important;
            background-color: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
            font-size: 0.9rem !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            background: rgba(255, 255, 255, 0.06) !important;
            background-color: rgba(255, 255, 255, 0.06) !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
            background: rgba(20, 184, 166, 0.15) !important;
            background-color: rgba(20, 184, 166, 0.15) !important;
            border: none !important;
            color: #14b8a6 !important;
            box-shadow: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked):hover {
            background: rgba(20, 184, 166, 0.22) !important;
            background-color: rgba(20, 184, 166, 0.22) !important;
            color: #14b8a6 !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span,
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) div {
            color: #14b8a6 !important;
            -webkit-text-fill-color: #14b8a6 !important;
            background: transparent !important;
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] .st-key-analysis_mode {
            width: 100% !important;
        }

        [data-testid="stSidebar"] .st-key-analysis_mode .stElementContainer {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] .st-key-analysis_mode [data-testid="stRadio"] > div[role="radiogroup"],
        [data-testid="stSidebar"] .st-key-analysis_mode [data-testid="stRadio"] > div {
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            overflow: hidden !important;
            visibility: hidden !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        section.main,
        section.main > div.block-container,
        section.main [data-testid="stMainBlockContainer"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        section.main > div.block-container {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-bottom: 2rem !important;
        }

        section.main [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        section.main [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        section.main .stElementContainer {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        .st-key-chat_area {
            max-width: 900px !important;
            margin: 0 auto !important;
            padding: 16px 24px 40px 24px !important;
            width: 100% !important;
        }

        .st-key-dashboard_area,
        .element-container.st-key-dashboard_area,
        .element-container.st-key-dashboard_area > [data-testid="stVerticalBlock"] {
            max-width: 100% !important;
            margin: 0 !important;
            padding: 8px 12px 24px 12px !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .st-key-dashboard_area [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        section.main:has(.st-key-dashboard_area) [data-testid="stMainBlockContainer"] {
            padding-left: 12px !important;
            padding-right: 12px !important;
        }

        /* 仪表盘页：左侧栏固定，仅主内容区滚动 */
        .stApp:has(.st-key-dashboard_area) {
            height: 100dvh !important;
            max-height: 100dvh !important;
            overflow: hidden !important;
        }
        .stApp:has(.st-key-dashboard_area) [data-testid="stSidebar"] {
            height: 100dvh !important;
            max-height: 100dvh !important;
            overflow: hidden !important;
        }
        .stApp:has(.st-key-dashboard_area) [data-testid="stSidebar"] > div:first-child {
            height: 100% !important;
            overflow: hidden !important;
        }
        .stApp:has(.st-key-dashboard_area) section.main {
            height: 100dvh !important;
            max-height: 100dvh !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }
        .stApp:has(.st-key-dashboard_area) [data-testid="stMainBlockContainer"] {
            max-height: none !important;
            overflow: visible !important;
        }

        .st-key-chat_area .stMarkdown:has(.pp-welcome-brand),
        .st-key-chat_area .stMarkdown:has(.pp-welcome-subtitle) {
            width: 100% !important;
            text-align: center !important;
        }

        p.pp-welcome-brand,
        .pp-welcome-brand {
            font-size: 4rem !important;
            font-weight: 700 !important;
            color: #0a0a0a !important;
            margin: 0 0 8px 0 !important;
            letter-spacing: -0.02em !important;
            text-align: center !important;
            width: 100% !important;
            display: block !important;
            line-height: 1.1 !important;
        }

        p.pp-welcome-brand span,
        .pp-welcome-brand span {
            color: #14b8a6 !important;
        }

        p.pp-welcome-subtitle,
        .pp-welcome-subtitle {
            font-size: 1.5rem !important;
            color: #6b7280 !important;
            margin: 0 0 48px 0 !important;
            font-weight: 400 !important;
            text-align: center !important;
            width: 100% !important;
            display: block !important;
        }

        .st-key-input_card,
        .element-container.st-key-input_card > [data-testid="stVerticalBlockBorderWrapper"],
        .element-container.st-key-input_card > [data-testid="stVerticalBlock"] {
            background: #ffffff !important;
            border: 1px solid #e5e5e5 !important;
            border-radius: 16px !important;
            padding: 16px 20px 10px 20px !important;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04) !important;
            margin-bottom: 32px !important;
        }

        .st-key-input_card .st-key-main_input [data-testid="stVerticalBlockBorderWrapper"],
        .st-key-input_card .st-key-main_input > div {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .st-key-input_card [data-testid="stTextAreaRootElement"] > div {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .st-key-input_card [data-testid="stTextArea"] label {
            display: none !important;
        }

        .st-key-input_card [data-testid="stTextArea"] > div {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        .st-key-input_card [data-testid="stTextArea"] textarea {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            resize: none !important;
            min-height: 80px !important;
            font-size: 1rem !important;
            color: #0a0a0a !important;
            padding: 0 !important;
        }

        .st-key-input_card [data-testid="stTextArea"] textarea:focus {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }

        .st-key-input_card [data-testid="stTextArea"] textarea::placeholder {
            color: #9ca3af !important;
        }

        /* 仅 footer 主行分隔线，不包含 Idea/Research 内层 columns */
        .st-key-input_card [data-testid="stHorizontalBlock"]:not(
            [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"]
        ) {
            display: flex !important;
            align-items: center !important;
            margin-top: 8px !important;
            padding: 8px 0 2px 0 !important;
            border-top: 1px solid #f0f0f0 !important;
            gap: 8px !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] {
            border-top: none !important;
            margin-top: 0 !important;
            padding: 0 !important;
            gap: 8px !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="column"] {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            align-self: center !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child {
            justify-content: flex-end !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child .stElementContainer,
        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stMarkdownContainer"],
        .st-key-input_card [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child p {
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] .stElementContainer {
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-input_card .st-key-footer_tag_idea,
        .st-key-input_card .st-key-footer_tag_research {
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-input_card .st-key-footer_tag_idea button,
        .st-key-input_card .st-key-footer_tag_research button {
            width: 100% !important;
            min-height: 36px !important;
            height: 36px !important;
            border-radius: 20px !important;
            font-size: 0.85rem !important;
            padding: 0 16px !important;
            line-height: 1 !important;
            box-shadow: none !important;
            cursor: pointer !important;
            background-image: none !important;
        }

        .st-key-input_card .st-key-footer_tag_idea button:hover,
        .st-key-input_card .st-key-footer_tag_research button:hover {
            border-color: #14b8a6 !important;
        }

        .st-key-input_card [data-testid="stHorizontalBlock"] .st-key-footer_tag_idea,
        .st-key-input_card [data-testid="stHorizontalBlock"] .st-key-footer_tag_research {
            flex: 0 0 auto !important;
        }

        .st-key-input_card .st-key-send_btn {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }

        .st-key-input_card .st-key-send_btn button {
            width: 36px !important;
            min-width: 36px !important;
            max-width: 36px !important;
            height: 36px !important;
            min-height: 36px !important;
            margin-left: auto !important;
            margin-right: 0 !important;
            border-radius: 50% !important;
            background: #171717 !important;
            background-color: #171717 !important;
            color: transparent !important;
            border: none !important;
            padding: 0 !important;
            font-size: 0 !important;
            line-height: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .st-key-input_card .st-key-send_btn button * {
            display: none !important;
        }

        .st-key-input_card .st-key-send_btn button::after {
            content: "↑" !important;
            position: absolute !important;
            left: 50% !important;
            top: 50% !important;
            transform: translate(-50%, -50%) !important;
            color: #ffffff !important;
            font-size: 1.1rem !important;
            line-height: 1 !important;
            display: block !important;
            margin: 0 !important;
            padding: 0 !important;
            pointer-events: none !important;
        }

        .st-key-input_card .st-key-send_btn [data-testid="stMarkdownContainer"] {
            display: none !important;
        }

        .st-key-input_card .st-key-send_btn button:hover::after {
            color: #ffffff !important;
        }

        .st-key-input_card .st-key-send_btn button:hover {
            background: #14b8a6 !important;
            background-color: #14b8a6 !important;
            border: none !important;
            color: transparent !important;
        }

        .pp-example-card {
            background: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            transition: all 0.2s;
            cursor: pointer;
            pointer-events: none;
        }

        .st-key-ex_card_1[data-testid="stVerticalBlock"],
        .st-key-ex_card_2[data-testid="stVerticalBlock"],
        .st-key-ex_card_3[data-testid="stVerticalBlock"] {
            position: relative !important;
        }

        .st-key-ex_card_1 .st-key-ex_card_1_click,
        .st-key-ex_card_2 .st-key-ex_card_2_click,
        .st-key-ex_card_3 .st-key-ex_card_3_click {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100% !important;
            z-index: 2 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-ex_card_1 .st-key-ex_card_1_click button,
        .st-key-ex_card_2 .st-key-ex_card_2_click button,
        .st-key-ex_card_3 .st-key-ex_card_3_click button {
            width: 100% !important;
            height: 100% !important;
            min-height: 140px !important;
            opacity: 0 !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
            cursor: pointer !important;
            box-shadow: none !important;
        }

        .st-key-ex_card_1:hover .pp-example-card,
        .st-key-ex_card_2:hover .pp-example-card,
        .st-key-ex_card_3:hover .pp-example-card {
            border-color: #14b8a6;
            box-shadow: 0 4px 16px rgba(20, 184, 166, 0.08);
        }

        .pp-card-icon {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: rgba(20, 184, 166, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            font-size: 1.1rem;
        }

        .pp-card-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #0a0a0a;
            margin: 0 0 6px 0;
        }

        .pp-card-desc {
            font-size: 0.8rem;
            color: #6b7280;
            line-height: 1.4;
            margin: 0;
        }

        .pp-results-section {
            margin-top: 32px;
            padding-top: 24px;
            border-top: 1px solid #e5e5e5;
        }

        .pp-results-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #0a0a0a;
            margin: 0 0 16px 0;
        }

        .score-card {
            background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
            color: #ffffff;
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
        }

        .score-value {
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
        }

        .score-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid #e5e5e5;
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
            background: rgba(255,255,255,0.05) !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] summary,
        [data-testid="stSidebar"] [data-testid="stExpander"] p,
        [data-testid="stSidebar"] [data-testid="stExpander"] label {
            color: #d1d5db !important;
            font-size: 0.85rem !important;
        }

        [data-testid="stSidebar"] input {
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


DEFAULT_HISTORY = [
    "AI 智能垃圾分类机器人",
    "基于深度学习的医疗影像诊断系统",
    "无人驾驶车辆路径规划算法",
    "可穿戴式心率监测设备",
    "智能家居语音控制系统",
]

EXAMPLE_CARDS = [
    {
        "key": "ex_card_1",
        "icon": "🤖",
        "title": "智能机器人分析",
        "desc": "评估 AI 驱动机器人创新的专利潜力",
        "text": "面向工业场景的 AI 智能分拣机器人，支持自动垃圾分类与物体识别",
    },
    {
        "key": "ex_card_2",
        "icon": "🏥",
        "title": "医疗技术评审",
        "desc": "评估生物医学设备与健康科技相关专利",
        "text": "基于深度学习的医疗影像诊断系统，用于肿瘤早期筛查",
    },
    {
        "key": "ex_card_3",
        "icon": "🔋",
        "title": "绿色能源检测",
        "desc": "分析可再生能源与可持续技术方案的专利前景",
        "text": "面向电动汽车与储能应用的高效率固态电池技术",
    },
]


IDEA_MODE_LABEL = "💡 Idea Mode"
RESEARCH_MODE_LABEL = "🔬 Research Mode"


def _set_idea_mode() -> None:
    st.session_state.analysis_mode = IDEA_MODE_LABEL


def _set_research_mode() -> None:
    st.session_state.analysis_mode = RESEARCH_MODE_LABEL


def _inject_footer_mode_tag_styles(is_idea_mode: bool) -> None:
    idea_active = is_idea_mode
    st.markdown(
        f"""
        <style>
        .st-key-footer_tag_idea button {{
            border: 1px solid {"#14b8a6" if idea_active else "#e5e5e5"} !important;
            background: {"rgba(20, 184, 166, 0.1)" if idea_active else "#ffffff"} !important;
            color: {"#14b8a6" if idea_active else "#6b7280"} !important;
            font-weight: {"500" if idea_active else "400"} !important;
        }}
        .st-key-footer_tag_research button {{
            border: 1px solid {"#14b8a6" if not idea_active else "#e5e5e5"} !important;
            background: {"rgba(20, 184, 166, 0.1)" if not idea_active else "#ffffff"} !important;
            color: {"#14b8a6" if not idea_active else "#6b7280"} !important;
            font-weight: {"500" if not idea_active else "400"} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _load_example(text: str) -> None:
    st.session_state.main_input = text


def _reset_analysis() -> None:
    st.session_state.main_input = ""
    st.session_state.pop("idea_result", None)
    st.session_state.pop("research_result", None)


def _append_history(title: str) -> None:
    if "history" not in st.session_state:
        st.session_state.history = list(DEFAULT_HISTORY)
    entry = f"📝 {title[:40]}"
    if entry not in st.session_state.history:
        st.session_state.history = [entry] + st.session_state.history[:9]


def main() -> None:
    if "main_input" not in st.session_state:
        st.session_state.main_input = ""
    if "history" not in st.session_state:
        st.session_state.history = list(DEFAULT_HISTORY)

    if "analysis_mode" not in st.session_state:
        st.session_state.analysis_mode = IDEA_MODE_LABEL

    with st.sidebar:
        st.markdown(
            '<p class="pp-sidebar-brand">Patent<span>Pilot</span></p>',
            unsafe_allow_html=True,
        )

        if st.button("+ New Analysis", key="new_analysis_btn", use_container_width=True):
            _reset_analysis()
            st.rerun()

        st.markdown('<p class="pp-section-title">Mode</p>', unsafe_allow_html=True)
        mode = st.radio(
            "分析模式",
            [IDEA_MODE_LABEL, RESEARCH_MODE_LABEL],
            label_visibility="collapsed",
            key="analysis_mode",
        )
        is_idea_mode = mode.startswith("💡")

        st.markdown('<p class="pp-section-title">History</p>', unsafe_allow_html=True)
        for item in st.session_state.history:
            st.markdown(f'<p class="pp-history-item">{item}</p>', unsafe_allow_html=True)

        st.markdown(
            '<p class="pp-sidebar-footer">AI-Powered Patent Navigation</p>',
            unsafe_allow_html=True,
        )

    has_result = ("idea_result" in st.session_state) or ("research_result" in st.session_state)
    progress_overlay = st.empty()

    if has_result:
        with st.container(key="dashboard_area"):
            if "idea_result" in st.session_state:
                render_idea_result(st.session_state.idea_result)
            elif "research_result" in st.session_state:
                render_research_result(st.session_state.research_result)
    else:
        with st.container(key="chat_area"):
            st.markdown(
                """
                <p class="pp-welcome-brand">Patent<span>Pilot</span></p>
                <p class="pp-welcome-subtitle">How can I help you today?</p>
                """,
                unsafe_allow_html=True,
            )

            with st.container(key="input_card"):
                placeholder = (
                    "Describe your innovation idea..."
                    if is_idea_mode
                    else "Paste your research abstract or project description..."
                )
                st.text_area(
                    "输入内容",
                    placeholder=placeholder,
                    height=80,
                    label_visibility="collapsed",
                    key="main_input",
                )

                footer_cols = st.columns([2.5, 3.3, 0.5])
                _inject_footer_mode_tag_styles(is_idea_mode)

                with footer_cols[0]:
                    tag_idea_col, tag_research_col = st.columns(2, gap="small")
                    with tag_idea_col:
                        st.button(
                            "💡 Idea",
                            key="footer_tag_idea",
                            on_click=_set_idea_mode,
                            use_container_width=True,
                        )
                    with tag_research_col:
                        st.button(
                            "🔬 Research",
                            key="footer_tag_research",
                            on_click=_set_research_mode,
                            use_container_width=True,
                        )

                with footer_cols[1]:
                    st.empty()

                with footer_cols[2]:
                    analyze = st.button(
                        "↑",
                        type="primary",
                        key="send_btn",
                        help="开始分析",
                        use_container_width=True,
                    )

            card_cols = st.columns(3)
            for col, card in zip(card_cols, EXAMPLE_CARDS):
                with col:
                    with st.container(key=card["key"]):
                        st.markdown(
                            f"""
                            <div class="pp-example-card">
                                <div class="pp-card-icon">{card["icon"]}</div>
                                <p class="pp-card-title">{card["title"]}</p>
                                <p class="pp-card-desc">{card["desc"]}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.button(
                            " ",
                            key=f"{card['key']}_click",
                            use_container_width=True,
                            on_click=_load_example,
                            args=(card["text"],),
                            help="点击填入示例",
                        )

            if analyze:
                content = st.session_state.main_input.strip()
                if not content:
                    st.warning("请先输入内容再开始分析。")
                else:
                    try:
                        from src.services.analyzer import PatentAnalyzer
                        from src.ui.analysis_progress import run_with_progress

                        def _call_analyzer() -> dict:
                            analyzer = PatentAnalyzer()
                            if is_idea_mode:
                                return analyzer.analyze_idea(content)
                            return analyzer.analyze_research(content)

                        result = run_with_progress(
                            _call_analyzer,
                            placeholder=progress_overlay,
                            tick_seconds=0.35,
                        )
                        if is_idea_mode:
                            st.session_state.idea_result = result
                            st.session_state.pop("research_result", None)
                        else:
                            st.session_state.research_result = result
                            st.session_state.pop("idea_result", None)
                        _append_history(content)
                        st.rerun()
                    except Exception as exc:
                        st.error(f"分析失败：{exc}")


def render_idea_result(result: dict) -> None:
    if result.get("parse_error"):
        st.error("分析结果解析失败")
        st.text_area("原始返回", result.get("raw_response", ""), height=200)
        return
    from src.ui.dashboard import render_analysis_dashboard

    render_analysis_dashboard(
        result,
        mode="idea",
        topic_input=st.session_state.get("main_input", ""),
        mode_label=st.session_state.get("analysis_mode", IDEA_MODE_LABEL),
    )


def render_research_result(result: dict) -> None:
    if result.get("parse_error"):
        st.error("分析结果解析失败")
        st.text_area("原始返回", result.get("raw_response", ""), height=200)
        return
    from src.ui.research_dashboard import render_research_dashboard

    render_research_dashboard(
        result,
        topic_input=st.session_state.get("main_input", ""),
        mode_label=st.session_state.get("analysis_mode", RESEARCH_MODE_LABEL),
    )


if not st.session_state.app_started:
    render_splash_page()
    st.stop()

inject_main_app_styles()
main()
