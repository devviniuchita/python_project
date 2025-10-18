"""Test script to validate Pydantic Settings loading."""

from src.config.settings import settings

print("=" * 80)
print("PYDANTIC SETTINGS VALIDATION")
print("=" * 80)
print("✅ Settings loaded successfully!")
print(f"LLM Model: {settings.llm_model}")
print(f"LangSmith Project: {settings.langsmith_project}")
print(f"LangSmith Tracing: {settings.langsmith_tracing}")
print(f"LangSmith Endpoint: {settings.langsmith_endpoint}")
print("\nAPI Keys Status:")
print(f"  - LANGSMITH_API_KEY: {'***' if settings.langsmith_api_key else 'NOT SET'}")
print(f"  - GOOGLE_API_KEY: {'***' if settings.google_api_key else 'NOT SET'}")
print("=" * 80)
