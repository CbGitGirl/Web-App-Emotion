# Watson NLP Emotion Detector

This project implements the IBM Watson NLP final-project emotion detector. It
uses the `emotion_aggregated-workflow_lang_en_stock` model to return scores for
anger, disgust, fear, joy, and sadness, plus the dominant emotion.

## Files

- `emotion_detection.py` — Watson NLP model wrapper and stable response shape
- `2a_emotion_detection.py` — rubric-named submission copy of the detector function
- `2b_application_creation.txt` — import and test terminal transcript for the rubric
- `3a_output_formatting.py` — rubric-named output-formatting submission
- `3b_formatted_output_test.txt` — rubric-named formatted-output terminal transcript
- `EmotionDetection/` — importable application package
- `4b_packaging_test.txt` — rubric-named package-validation terminal transcript
- `5a_unit_testing.py` — rubric-named unit-test submission
- `5b_unit_testing_result.txt` — rubric-named all-tests-passed transcript
- `6a_server.py` — rubric-named Flask deployment submission
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


### Replit validation boundary

The live model check cannot be completed in this Replit workspace: its managed
Python site-packages are read-only, `watson-nlp==4.8.0` is not available from
the accessible package registry, and the hosted Skills Network emotion service
is unreachable from this network. The local server has been verified to return
an explicit HTTP 503 in that condition. The `2b_application_creation.txt` and
`3b_formatted_output_test.txt` transcripts use a Watson-compatible fake model
only; they are deterministic formatting checks, not live inference evidence.

Capture the five real scores and `dominant_emotion` by repeating the run steps
in the course Watson runtime with the model installed. This remaining evidence
is tracked as follow-up task #1103.

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

### Local validation recorded in Replit

Using a temporary writable Python environment, `pytest -q` completed with
`6 passed` and `python -m pylint server.py emotion_detection.py` rated the code
at `10.00/10`. The exact requirements installation remained blocked at
`watson-nlp==4.8.0`; a real-sentence call to the locally started server
therefore returned the documented HTTP 503 rather than fabricated scores.
