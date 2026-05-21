"""
Central configuration for the package. Allows to populate its fields from
the environmental variables in .env, and to have a single source of truth for all other
settings. SettingsConfigDict tells Pydantic to look for .env three levels up from this file,
which is the project root.

Design split between this file and .env:
  - config.py holds *application behavior* — model choice, temperature,
    paths. These are design decisions, version-controlled, the same
    on every machine.
  - .env holds *machine-specific or secret values* — API keys. These
    are gitignored and vary per developer or environment.

If you find yourself wanting to vary something per machine that isn't
secret (e.g. you want to test a different model locally), promote it
to .env at that point. Until then, keep it here where it's visible.
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings."""

    # --- Application behavior (version-controlled in this file) ---

    # LLM choice in "<provider>:<model>" format. init_chat_model
    # understands: anthropic, openai, google_genai, ollama, mistralai, ...
    llm_model: str = "anthropic:claude-sonnet-4-6"
    llm_temperature: float = 0.0

    # --- Secrets and machine-specific values (loaded from .env) ---

    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    # --- Computed paths ---

    project_root: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = project_root / "data"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

# trigger to read the .env, apply defaults, validate types, construct a populated settings object
# later we do from pk_agent.config import settings to use the values
settings = Settings()