"""Application settings using Pydantic BaseSettings for environment validation.

This module provides automatic validation of environment variables at startup,
ensuring all required configurations are present and correctly typed before
the application runs.

Example:
    >>> from config.settings import settings
    >>> print(settings.llm_model)
    'gemini-2.0-flash-exp'
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class uses Pydantic BaseSettings to automatically load and validate
    environment variables from the .env file. Required fields will raise
    ValidationError if missing, ensuring fail-fast behavior.

    Attributes:
        langsmith_api_key: LangSmith API Key for tracing and monitoring (required)
        google_api_key: Google Gemini API Key for LLM access (required)
        llm_model: LLM model identifier (default: gemini-2.0-flash-exp)
        langsmith_project: LangSmith project name (default: rag-conversational)
        langsmith_tracing: Enable LangSmith tracing (default: True)
        langsmith_endpoint: LangSmith API endpoint URL
    """

    # LangSmith Configuration (required)
    langsmith_api_key: str = Field(
        ..., description="LangSmith API Key for tracing and monitoring"
    )

    # Google Gemini Configuration (required)
    google_api_key: str = Field(..., description="Google Gemini API Key")

    # Optional configurations with defaults
    llm_model: str = Field(
        default="gemini-2.0-flash-exp", description="LLM model identifier"
    )

    langsmith_project: str = Field(
        default="rag-conversational", description="LangSmith project name"
    )

    langsmith_tracing: bool = Field(
        default=True, description="Enable LangSmith tracing"
    )

    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com", description="LangSmith API endpoint"
    )

    langsmith_trace_sample_rate: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="LangSmith trace sampling rate (0.0=disabled, 1.0=all requests)",
    )

    # Reranker Configuration (BGE)
    reranker_enabled: bool = Field(
        default=True, description="Enable BGE semantic reranking"
    )

    reranker_model: str = Field(
        default="BAAI/bge-reranker-base",
        description="BGE reranker model: base, large, or v2-m3",
    )

    reranker_top_n: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of top documents to keep after reranking",
    )

    reranker_score_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score threshold (0.0 = no filtering)",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )

    log_format: str = Field(
        default="auto",
        description="Log format: auto (TTY=console, pipe=JSON), json, or console",
    )

    model_config = SettingsConfigDict(
        env_file="c:/Users/ADMIN/Desktop/rules-base/.venv/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Accept MY_VAR or my_var
        extra="ignore",  # Ignore extra environment variables
        validate_default=True,  # Validate default values
    )


# Singleton instance for app-wide access
# This will validate all settings on import, providing fail-fast behavior
settings = Settings()
