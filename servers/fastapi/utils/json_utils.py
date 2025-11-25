import re


def strip_code_fence(text: str) -> str:
    if not text:
        return ""

    cleaned = text.strip()

    fence_match = re.match(r"```(?:[a-zA-Z0-9_-]+\s*)?\n", cleaned)
    if fence_match:
        cleaned = cleaned[fence_match.end() :]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned[: cleaned.rfind("```")]

    return cleaned.strip()


def extract_json_object(text: str) -> str:
    """
    Pull out a JSON object from LLM output that may contain code fences or prose.
    Returns the best-effort JSON string (possibly unchanged).
    """
    cleaned = strip_code_fence(text)

    if cleaned.lstrip().startswith("{"):
        return cleaned.lstrip()

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return cleaned[first_brace : last_brace + 1].strip()

    return cleaned
