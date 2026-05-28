import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

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

DEEPSEEK_API_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.modelarts-maas.com/v2/chat/completions",
)
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
