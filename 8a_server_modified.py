"""Task 8 submission: Flask server prepared for static code analysis."""

# The assignment requires this filename to begin with a digit.
# pylint: disable=invalid-name

from __future__ import annotations

from flask import Flask, jsonify, request

from emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    """Return a lightweight service health response."""
    return jsonify({"status": "ok"})


@app.get("/emotionDetector")
def emotion_detector_route():
    """Detect emotions for the course-compatible query parameter."""
    text_to_analyze = request.args.get("textToAnalyze")
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text_to_analyze)
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503

    return jsonify(result)


if __name__ == "__main__":
    # Static analysis command:
    # uv run --with pylint --with flask pylint server.py emotion_detection.py
    app.run(host="0.0.0.0", port=5000, debug=False)