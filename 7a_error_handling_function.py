"""Task 7 submission: emotion detector error handling."""

from __future__ import annotations

from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - dependency is listed in requirements.txt
    requests = None


WATSON_NLP_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_NAME = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, Any]:
    """Return the error-handling shape used for invalid input."""
    return {**{name: None for name in EMOTION_NAMES}, "dominant_emotion": None}


def emotion_detector(text_to_analyze: str | None) -> dict[str, Any]:
    """Return emotion scores or an explicit invalid-input result.

    The Flask server converts a result with no dominant emotion into the
    rubric-required HTTP 400 response.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    if requests is None:
        raise RuntimeError(
            "The requests package is not installed. Install requirements.txt "
            "before running detection."
        )

    response = requests.post(
        WATSON_NLP_URL,
        headers={"grpc-metadata-mm-model-id": MODEL_NAME},
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    response.raise_for_status()
    emotion_scores = response.json()["emotion_prediction"]["emotion"]

    result = {name: emotion_scores[name] for name in EMOTION_NAMES}
    result["dominant_emotion"] = max(
        EMOTION_NAMES, key=lambda name: emotion_scores[name]
    )
    return result