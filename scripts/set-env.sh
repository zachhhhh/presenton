#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DOTENV_FILE="$ROOT_DIR/.env"

PROVIDER=""
MODEL=""
BASE_URL=""
PUSH_VERCEL="false"
PUSH_RENDER="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --provider)
      PROVIDER="$2"; shift 2 ;;
    --model)
      MODEL="$2"; shift 2 ;;
    --base-url)
      BASE_URL="$2"; shift 2 ;;
    --vercel)
      PUSH_VERCEL="true"; shift 1 ;;
    --render)
      PUSH_RENDER="true"; shift 1 ;;
    *)
      shift 1 ;;
  esac
done

touch "$DOTENV_FILE"

set_kv() {
  local key="$1"
  local val="$2"
  if grep -qE "^${key}=" "$DOTENV_FILE"; then
    sed -i'' -e "s|^${key}=.*|${key}=${val}|" "$DOTENV_FILE"
  else
    printf "%s=%s\n" "$key" "$val" >> "$DOTENV_FILE"
  fi
}

if [[ -n "$PROVIDER" ]]; then
  set_kv "LLM" "$PROVIDER"
  if [[ "$PROVIDER" == "z.ai" || "$PROVIDER" == "custom" ]]; then
    if [[ -z "$BASE_URL" ]]; then
      BASE_URL="https://api.z.ai/api/paas/v4"
    fi
    if [[ -z "$MODEL" ]]; then
      MODEL="glm-4-air"
    fi
    set_kv "CUSTOM_LLM_URL" "$BASE_URL"
    set_kv "CUSTOM_MODEL" "$MODEL"
    set_kv "DEFAULT_LLM_PROVIDER" "$PROVIDER"
    set_kv "IMAGE_PROVIDER" "cogview"
  elif [[ "$PROVIDER" == "openai" ]]; then
    if [[ -z "$MODEL" ]]; then
      MODEL="gpt-4o-mini"
    fi
    set_kv "OPENAI_MODEL" "$MODEL"
    set_kv "DEFAULT_LLM_PROVIDER" "openai"
    set_kv "IMAGE_PROVIDER" "dall-e-3"
  elif [[ "$PROVIDER" == "google" ]]; then
    if [[ -z "$MODEL" ]]; then
      MODEL="models/gemini-2.5-flash"
    fi
    set_kv "GOOGLE_MODEL" "$MODEL"
    set_kv "DEFAULT_LLM_PROVIDER" "google"
    set_kv "IMAGE_PROVIDER" "gemini_flash"
  elif [[ "$PROVIDER" == "anthropic" ]]; then
    if [[ -z "$MODEL" ]]; then
      MODEL="claude-sonnet-4-20250514"
    fi
    set_kv "ANTHROPIC_MODEL" "$MODEL"
    set_kv "DEFAULT_LLM_PROVIDER" "anthropic"
    set_kv "IMAGE_PROVIDER" "pexels"
  elif [[ "$PROVIDER" == "ollama" ]]; then
    if [[ -z "$MODEL" ]]; then
      MODEL="llama3.2:3b"
    fi
    set_kv "OLLAMA_MODEL" "$MODEL"
    set_kv "DEFAULT_LLM_PROVIDER" "ollama"
    set_kv "IMAGE_PROVIDER" "pexels"
  fi
fi

if [[ "$PUSH_VERCEL" == "true" ]]; then
  if ! command -v vercel >/dev/null 2>&1; then
    npm install -g vercel >/dev/null 2>&1 || true
  fi
  cd "$ROOT_DIR"
  TOKEN_ARGS=()
  if [[ -n "${VERCEL_TOKEN:-}" ]]; then
    TOKEN_ARGS+=(--token "$VERCEL_TOKEN")
  fi
  PROJECT_ENV_SCOPE="production"
  if [[ -n "$PROVIDER" ]]; then
    vercel env set LLM "$PROVIDER" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  fi
  if [[ "$PROVIDER" == "z.ai" || "$PROVIDER" == "custom" ]]; then
    vercel env set CUSTOM_LLM_URL "$BASE_URL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set CUSTOM_MODEL "$MODEL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set DEFAULT_LLM_PROVIDER "$PROVIDER" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set IMAGE_PROVIDER "cogview" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  elif [[ "$PROVIDER" == "openai" ]]; then
    vercel env set OPENAI_MODEL "$MODEL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set DEFAULT_LLM_PROVIDER "openai" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set IMAGE_PROVIDER "dall-e-3" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  elif [[ "$PROVIDER" == "google" ]]; then
    vercel env set GOOGLE_MODEL "$MODEL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set DEFAULT_LLM_PROVIDER "google" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set IMAGE_PROVIDER "gemini_flash" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  elif [[ "$PROVIDER" == "anthropic" ]]; then
    vercel env set ANTHROPIC_MODEL "$MODEL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set DEFAULT_LLM_PROVIDER "anthropic" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set IMAGE_PROVIDER "pexels" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  elif [[ "$PROVIDER" == "ollama" ]]; then
    vercel env set OLLAMA_MODEL "$MODEL" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set DEFAULT_LLM_PROVIDER "ollama" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
    vercel env set IMAGE_PROVIDER "pexels" "$PROJECT_ENV_SCOPE" "${TOKEN_ARGS[@]}"
  fi
fi

if [[ "$PUSH_RENDER" == "true" ]]; then
  echo "Render env syncing is not automated in this script. Use dashboard or render.yaml."
fi
