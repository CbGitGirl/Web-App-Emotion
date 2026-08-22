# Watson NLP Emotion Detector

This project implements the IBM Watson NLP final-project emotion detector. It
uses the `emotion_aggregated-workflow_lang_en_stock` model to return scores for
anger, disgust, fear, joy, and sadness, plus the dominant emotion.

## Files

- `emotion_detection.py` — Watson NLP model wrapper and stable response shape
- `server.py` — Flask API
- `test_emotion_detection.py` — unit and route tests
- `requirements.txt` — Python dependencies

## Setup

The Watson NLP Python package and its model may require the IBM Watson NLP
runtime/model environment used by the course. Install the dependencies in a
Python environment that supports that runtime:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If the course environment provides the model separately, install or register
`emotion_aggregated-workflow_lang_en_stock` there before starting the server.
The application does not silently substitute another emotion detector.

## Run

```bash
python server.py
```

Then request:

```text
http://localhost:5000/emotionDetector?textToAnalyze=I%20love%20this
```

The response has this shape:

```json
{
  "anger": 0.01,
  "disgust": 0.01,
  "fear": 0.01,
  "joy": 0.95,
  "sadness": 0.02,
  "dominant_emotion": "joy"
}
```

Blank or missing input returns HTTP 400. If the Watson NLP runtime is not
installed, detection returns HTTP 503 with an actionable error instead of
pretending the result is valid.

## Test

The tests use a small Watson-compatible fake model for deterministic unit
testing and do not download a model:

```bash
pytest -q
```

For the static-analysis submission, run:

```bash
python -m pylint server.py emotion_detection.py
```