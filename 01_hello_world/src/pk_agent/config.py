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

# we define a pydantic settings model 
# special type that allows to populate fields from env variables and .env files
class Settings(BaseSettings):
    """Global application settings."""

    # defines LLM choice in "<provider>:<model>" format. init_chat_model
    # understands: anthropic, openai, google_genai, ollama, mistralai, ...
    llm_model: str = "anthropic:claude-sonnet-4-6"
    llm_temperature: float = 0.0

    # define secrets and machine-specific values, loaded from .env
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    # compute path
    project_root: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = project_root / "data"

    # tell pytdantic to also look into the .env file, read it as utf8, 
    # ignore unknown keys, and match variable names case-insensitively
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

# reads the .env file, applies defaults and constructs a populated settings object
# we will later do   from pk_agent.config import settings  to use these values
settings = Settings()