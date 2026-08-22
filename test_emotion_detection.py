"""Unit tests for Watson NLP emotion detection and its Flask route."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import emotion_detection
from server import app


EMOTIONS = {
    "anger": 0.01,
    "disgust": 0.02,
    "fear": 0.03,
    "joy": 0.91,
    "sadness": 0.04,
}


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"emotion_prediction": {"emotion": EMOTIONS}}


def test_emotion_detector_returns_scores_and_dominant_emotion(monkeypatch):
    calls = {}

    def fake_post(url, headers, json, timeout):
        calls.update(url=url, headers=headers, json=json, timeout=timeout)
        return FakeResponse()

    monkeypatch.setattr(emotion_detection.requests, "post", fake_post)

    result = emotion_detection.emotion_detector("I am delighted by this result.")

    assert result == {**EMOTIONS, "dominant_emotion": "joy"}
    assert calls["url"] == emotion_detection.WATSON_NLP_URL
    assert calls["headers"] == {
        "grpc-metadata-mm-model-id": emotion_detection.MODEL_NAME
    }
    assert calls["json"] == {
        "raw_document": {"text": "I am delighted by this result."}
    }
    assert calls["timeout"] == 30


@pytest.mark.parametrize("value", [None, "", "   "])
def test_empty_input_returns_explicit_invalid_shape(value):
    assert emotion_detection.emotion_detector(value) == {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def test_route_rejects_missing_text():
    client = app.test_client()

    response = client.get("/emotionDetector")

    assert response.status_code == 400
    assert response.get_data(as_text=True) == "Invalid text! Please try again!"


def test_route_returns_json(monkeypatch):
    monkeypatch.setattr(
        "server.emotion_detector",
        lambda text: {**EMOTIONS, "dominant_emotion": "joy"},
    )
    client = app.test_client()

    response = client.get("/emotionDetector?textToAnalyze=hello")

    assert response.status_code == 200
    assert response.get_json()["dominant_emotion"] == "joy"