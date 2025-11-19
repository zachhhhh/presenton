from fastapi import HTTPException

from constants.llm import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_GOOGLE_MODEL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_CUSTOM_MODEL,
    DEFAULT_CUSTOM_LLM_URL,
)
from enums.llm_provider import LLMProvider
from openai import OpenAI
from utils.get_env import (
    get_anthropic_model_env,
    get_custom_llm_api_key_env,
    get_custom_llm_url_env,
    get_custom_model_env,
    get_google_model_env,
    get_llm_provider_env,
    get_ollama_model_env,
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
    """Return a custom OpenAI-compatible client pointing at Z.AI."""
    base_url = get_custom_llm_url_env() or DEFAULT_CUSTOM_LLM_URL
    return OpenAI(
        base_url=base_url,
        api_key=get_custom_llm_api_key_env() or "null",
    )


def get_google_llm_client():
    """Google/Anthropic support is disabled; use glm4.6 instead."""
    raise RuntimeError("Google Gemini client is disabled while focusing on glm4.6.")


def get_large_model() -> str:
    """Return the glm4.6 model ID used across the stack."""
    return get_custom_model_env() or DEFAULT_CUSTOM_MODEL
