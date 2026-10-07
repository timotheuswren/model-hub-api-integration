"""Build request descriptions without sending network traffic."""
from __future__ import annotations

import os
from typing import Any


def _messages(prompt: str) -> list[dict[str, str]]:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    return [{"role": "user", "content": prompt}]


def build_huggingface_request(prompt: str, *, model: str = "zai-org/GLM-5.3", provider: str = "baseten") -> dict[str, Any]:
    """Return the OpenAI-compatible HF Router request shown in its docs."""
    return {
        "method": "POST",
        "url": "https://router.huggingface.co/v1/chat/completions",
        "headers": {"Authorization": "Bearer ${HF_TOKEN}", "Content-Type": "application/json"},
        "json": {"model": f"{model}:{provider}", "messages": _messages(prompt)},
    }


def build_argolink_request(prompt: str, *, model: str = "glm-5.3") -> dict[str, Any]:
    """Return an ArgoLink request description; it is not executed."""
    return {
        "method": "POST",
        "url": os.getenv("ARGOLINK_BASE_URL", "https://argolink.io/v1") + "/chat/completions",
        "headers": {"Authorization": "Bearer ${ARGOLINK_API_KEY}", "Content-Type": "application/json"},
        "json": {"model": model, "messages": _messages(prompt)},
    }


def compare_payloads(prompt: str) -> dict[str, dict[str, Any]]:
    """Return both payloads so callers can inspect differences before sending."""
    return {"huggingface": build_huggingface_request(prompt), "argolink": build_argolink_request(prompt)}
