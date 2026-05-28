import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DEFAULT_DEEPSEEK_API_URL = "https://api.modelarts-maas.com/v2/chat/completions"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def _secret_or_env(key: str, default: str = "") -> str:
    """Read config from Streamlit Secrets (Cloud) or environment / .env (local)."""
    try:
        import streamlit as st

        if key in st.secrets:
            raw = st.secrets[key]
            if raw is not None:
                text = str(raw).strip()
                if text:
                    return text
    except Exception:
        pass

    env_val = os.getenv(key)
    if env_val is not None:
        text = str(env_val).strip()
        if text:
            return text
    return default


def get_deepseek_api_key() -> str:
    return _secret_or_env("DEEPSEEK_API_KEY", "")


def get_deepseek_api_url() -> str:
    return _secret_or_env("DEEPSEEK_API_URL", DEFAULT_DEEPSEEK_API_URL)


def get_deepseek_model() -> str:
    return _secret_or_env("DEEPSEEK_MODEL", DEFAULT_DEEPSEEK_MODEL)
