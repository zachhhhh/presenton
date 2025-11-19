from fastapi import HTTPException

from constants.llm import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_GOOGLE_MODEL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_CUSTOM_MODEL,
)
from enums.llm_provider import LLMProvider
from google import genai
from openai import OpenAI
from utils.get_env import (
    get_anthropic_model_env,
    get_custom_model_env,
    get_google_api_key_env,
    get_google_model_env,
    get_llm_provider_env,
    get_ollama_model_env,
    get_openai_api_key_env,
    get_openai_model_env,
)


CUSTOM_COMPATIBLE_PROVIDERS = (LLMProvider.CUSTOM, LLMProvider.ZAI)


def get_llm_provider():
    try:
        return LLMProvider(get_llm_provider_env())
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Invalid LLM provider. Please select one of: openai, google, anthropic, ollama, custom, z.ai",
        )


def is_openai_selected():
    return get_llm_provider() == LLMProvider.OPENAI


def is_google_selected():
    return get_llm_provider() == LLMProvider.GOOGLE


def is_anthropic_selected():
    return get_llm_provider() == LLMProvider.ANTHROPIC


def is_ollama_selected():
    return get_llm_provider() == LLMProvider.OLLAMA


def is_custom_llm_selected():
    return get_llm_provider() in CUSTOM_COMPATIBLE_PROVIDERS


def get_model():
    selected_llm = get_llm_provider()
    if selected_llm == LLMProvider.OPENAI:
        return get_openai_model_env() or DEFAULT_OPENAI_MODEL
    elif selected_llm == LLMProvider.GOOGLE:
        return get_google_model_env() or DEFAULT_GOOGLE_MODEL
    elif selected_llm == LLMProvider.ANTHROPIC:
        return get_anthropic_model_env() or DEFAULT_ANTHROPIC_MODEL
    elif selected_llm == LLMProvider.OLLAMA:
        return get_ollama_model_env()
    elif selected_llm in CUSTOM_COMPATIBLE_PROVIDERS:
        return get_custom_model_env() or DEFAULT_CUSTOM_MODEL
    else:
        raise HTTPException(
            status_code=500,
            detail="Invalid LLM provider. Please select one of: openai, google, anthropic, ollama, custom, z.ai",
        )


def get_llm_client() -> OpenAI:
    """Return an OpenAI client for schema tests."""
    return OpenAI(api_key=get_openai_api_key_env() or None)


def get_google_llm_client() -> genai.Client:
    """Return a Google Gemini client for schema tests."""
    key = get_google_api_key_env()
    if key:
        return genai.Client(api_key=key)
    return genai.Client()


def get_large_model(provider: LLMProvider | None = None) -> str:
    """Return an LLM ID suitable for schema-parsing tests."""

    def _fallback_provider() -> LLMProvider | None:
        if get_openai_api_key_env():
            return LLMProvider.OPENAI
        if get_google_api_key_env():
            return LLMProvider.GOOGLE
        return None

    selected_provider = provider or get_llm_provider()
    if selected_provider in (LLMProvider.CUSTOM, LLMProvider.ZAI):
        fallback = _fallback_provider()
        if fallback:
            selected_provider = fallback

    match selected_provider:
        case LLMProvider.OPENAI:
            return get_openai_model_env() or DEFAULT_OPENAI_MODEL
        case LLMProvider.GOOGLE:
            return get_google_model_env() or DEFAULT_GOOGLE_MODEL
        case LLMProvider.ANTHROPIC:
            return get_anthropic_model_env() or DEFAULT_ANTHROPIC_MODEL
        case LLMProvider.OLLAMA:
            return get_ollama_model_env() or ""
        case LLMProvider.CUSTOM | LLMProvider.ZAI:
            return get_custom_model_env() or DEFAULT_CUSTOM_MODEL
        case _:
            return DEFAULT_OPENAI_MODEL
