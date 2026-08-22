"""Watson NLP emotion detection service logic."""

from __future__ import annotations

from typing import Any

try:
    import watson_nlp
except ImportError:  # pragma: no cover - exercised only without the optional runtime
    watson_nlp = None


MODEL_NAME = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, Any]:
    """Return the stable response shape used for invalid input."""
    return {**{name: None for name in EMOTION_NAMES}, "dominant_emotion": None}


def emotion_detector(text_to_analyze: str | None) -> dict[str, Any]:
    """Detect the five Watson NLP emotions and their dominant emotion.

    Watson NLP is loaded lazily so importing the module remains safe for tools
    and tests when the model runtime is not installed. A missing or blank
    string is invalid and never reaches the model.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    if watson_nlp is None:
        raise RuntimeError(
            "Watson NLP is not installed. Install requirements.txt and the "
            "Watson NLP emotion model before running detection."
        )

    model = watson_nlp.load(MODEL_NAME)
    response = model.run(text_to_analyze)
    emotion_scores = response["emotion_prediction"]["emotion"]

    result = {name: emotion_scores[name] for name in EMOTION_NAMES}
    result["dominant_emotion"] = max(
        EMOTION_NAMES, key=lambda name: emotion_scores[name]
    )
    return result