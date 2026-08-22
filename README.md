# Watson NLP Emotion Detector

This project implements the IBM Watson NLP final-project emotion detector. It
calls the course Watson NLP EmotionPredict service with the
`emotion_aggregated-workflow_lang_en_stock` model to return scores for anger,
disgust, fear, joy, and sadness, plus the dominant emotion.

## Files

- `emotion_detection.py` — Watson NLP HTTP client and stable response shape
- `2a_emotion_detection.py` — rubric-named submission copy of the detector function
- `2b_application_creation.txt` — import and test terminal transcript for the rubric
- `3a_output_formatting.py` — rubric-named output-formatting submission
- `3b_formatted_output_test.txt` — rubric-named formatted-output terminal transcript
- `EmotionDetection/` — importable application package
- `4b_packaging_test.txt` — rubric-named package-validation terminal transcript
- `5a_unit_testing.py` — rubric-named unit-test submission
- `5b_unit_testing_result.txt` — rubric-named all-tests-passed transcript
- `6a_server.py` — rubric-named Flask deployment submission
- `6b_deployment_test.png` — rubric-named Flask deployment evidence image
- `7a_error_handling_function.py` — rubric-named error-handling submission
- `7b_error_handling_server.py` — rubric-named Flask blank-input handling submission
- `7c_error_handling_interface.png` — rubric-named error-handling evidence image
- `8a_server_modified.py` — rubric-named static-analysis server submission
- `8b_static_code_analysis.txt` — rubric-named perfect-score analysis transcript
- `server.py` — Flask API
- `test_emotion_detection.py` — unit and route tests
- `requirements.txt` — Python dependencies

## Setup

Install the dependencies in a Python environment with network access:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The detector sends `text_to_analyze` as
`{"raw_document": {"text": text_to_analyze}}` to the course endpoint and sets
the `grpc-metadata-mm-model-id` header to
`emotion_aggregated-workflow_lang_en_stock`.


### Replit validation boundary

The live course endpoint may be unavailable from some development networks.
The local tests use a Watson-compatible fake HTTP response only; they are
deterministic formatting checks, not live inference evidence.

When the course endpoint is available, the server returns the five real scores
and `dominant_emotion` directly from Watson NLP.

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

Blank or missing input returns HTTP 400. If the Watson NLP request fails,
detection returns HTTP 503 with an actionable error instead of pretending the
result is valid.

## Test

The tests use a small Watson-compatible fake HTTP response for deterministic
unit testing and do not call the live endpoint:

```bash
pytest -q
```

For the static-analysis submission, run:

```bash
python -m pylint server.py emotion_detection.py
```

### Local validation recorded in Replit

Using a temporary writable Python environment, `pytest -q` completed with
`6 passed` and `python -m pylint server.py emotion_detection.py` rated the code
at `10.00/10`. The tests do not fabricate a live result; they only validate
the request contract and output formatting with a deterministic fake response.
