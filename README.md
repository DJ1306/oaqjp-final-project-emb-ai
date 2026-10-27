# Final Project

An AI-powered web application that analyzes textual input to detect emotional sentiment using Watson NLP Emotion Predict library. The application extracts fine-grained emotion scores for anger, disgust, fear, joy, and sadness, identifies the dominant emotion, and provides both a modular Python package and an interactive web interface powered by Flask.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites & Dependencies](#prerequisites--dependencies)
- [Installation](#installation)
- [Watson NLP Configuration](#watson-nlp-configuration)
- [Running the Application](#running-the-application)
- [Running Unit Tests](#running-unit-tests)
- [Static Code Analysis (Pylint)](#static-code-analysis-pylint)
- [Example Requests and Outputs](#example-requests-and-outputs)
- [Known Environment Limitations](#known-environment-limitations)
- [Evidence Directory](#evidence-directory)

---

## Overview
This project was developed as the final graded project for the course **Developing AI Applications with Python and Flask** (IBM / Coursera). The solution encapsulates emotion detection into a reusable package `EmotionDetection`, exposes a REST endpoint `/emotionDetector` using Flask, and serves a user-friendly browser interface for real-time text analysis and error handling.

---

## Features
- **Emotion Analysis via Watson NLP**: Analyzes any English statement to compute scores for five core emotions: `anger`, `disgust`, `fear`, `joy`, and `sadness`.
- **Dominant Emotion Identification**: Automatically evaluates and highlights the emotion with the highest confidence score.
- **Robust Error Handling**:
  - Handles HTTP 400 responses from the NLP service gracefully by returning `None` across all emotion keys.
  - Detects blank, empty, or whitespace-only user input in the Flask server without triggering redundant remote network calls.
  - Returns friendly user notifications (`"Invalid text! Please try again!"`).
- **Comprehensive Unit Testing**: Unittest suite covering all five dominant emotions and edge cases with mocked external calls to enable offline validation.
- **Pylint Clean**: Achieves a perfect 10.00/10 score across all project Python files.

---

## Project Structure
```text
Emotion Detector/
├── .gitignore                      # Git ignore file for Python environments & artifacts
├── LICENSE                         # Project license
├── README.md                       # Project documentation
├── requirements.txt                # Application dependencies
├── server.py                       # Flask web application server
├── test_emotion_detection.py       # Unittest test suite with mock support
├── EmotionDetection/               # Emotion detection Python package
│   ├── __init__.py                 # Package init exposing emotion_detector
│   └── emotion_detection.py        # Watson NLP integration and response parser
├── static/                         # Frontend static assets
│   └── mywebscript.js              # Client-side AJAX script
├── templates/                      # Flask HTML templates
│   └── index.html                  # Main user interface template
└── evidence/                       # Submission evidence and artifacts
    ├── 6b_deployment_test.png      # Screenshot of running application with joy response
    ├── 7c_error_handling_interface.png # Screenshot of blank input error handling
    ├── emotion_detection.py        # Source code snapshot
    ├── server.py                   # Source code snapshot
    ├── test_emotion_detection.py   # Source code snapshot
    ├── terminal_dictionary_format.txt
    ├── terminal_import_execution.txt
    ├── terminal_package_validation.txt
    ├── terminal_pylint_score.txt
    ├── terminal_pylint_server.txt
    └── terminal_unit_tests.txt
```

---

## Prerequisites & Dependencies
- **Python**: Version 3.10+ (tested on Python 3.13.1)
- **Pip**: Latest version
- Core Python Libraries (see `requirements.txt`):
  - `Flask>=3.0.0`
  - `requests>=2.31.0`
  - `pylint>=3.0.0`

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai.git
   cd "Emotion Detector"
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Watson NLP Configuration

The default endpoint configured in `EmotionDetection/emotion_detection.py` connects to the IBM Skills Network Watson NLP Emotion Predict service:

- **Endpoint URL**: `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`
- **Header**: `grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock`
- **Payload Format**:
  ```json
  {
    "raw_document": {
      "text": "<input_statement>"
    }
  }
  ```

For local testing or custom deployment environments, you can override the endpoint URL via the `WATSON_EMOTION_URL` environment variable:
```bash
# Windows PowerShell
$env:WATSON_EMOTION_URL="http://127.0.0.1:5050/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

# Linux / macOS
export WATSON_EMOTION_URL="http://127.0.0.1:5050/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
```

---

## Running the Application

1. **Start the Flask server:**
   ```bash
   python server.py
   ```
   By default, the server listens on `0.0.0.0:5000` (configurable via `HOST` and `PORT` environment variables).

2. **Access the application:**
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

3. **Analyze Emotion:**
   Enter any sentence into the text box and click **Run Sentiment Analysis**.

---

## Running Unit Tests

Run the test discovery command:
```bash
python -m unittest discover -v
```
Or run the test file directly:
```bash
python test_emotion_detection.py -v
```

All 5 core statements and error conditions are tested:
- "I am glad this happened" -> `joy`
- "I am really mad about this" -> `anger`
- "I feel disgusted just hearing about this" -> `disgust`
- "I am so sad about this" -> `sadness`
- "I am really afraid that this will happen" -> `fear`
- Blank input -> `dominant_emotion is None`

---

## Static Code Analysis (Pylint)

To verify compliance with PEP 8 and static analysis standards:

```bash
# Analyze server.py
python -m pylint server.py

# Analyze the package
python -m pylint EmotionDetection

# Analyze the entire project
python -m pylint server.py EmotionDetection/emotion_detection.py test_emotion_detection.py
```

**Target and Actual Score**: `10.00/10`

---

## Example Requests and Outputs

### 1. Python Package Usage
```python
from EmotionDetection import emotion_detector

result = emotion_detector("I am glad this happened")
print(result)
```
**Output:**
```json
{
    "anger": 0.01,
    "disgust": 0.02,
    "fear": 0.03,
    "joy": 0.94,
    "sadness": 0.02,
    "dominant_emotion": "joy"
}
```

### 2. Web API Endpoint (`GET /emotionDetector`)
**Request:**
```text
GET /emotionDetector?textToAnalyze=I%20think%20I%20am%20having%20fun
```
**Response (HTTP 200):**
```text
For the given statement, the system response is 'anger': 0.01, 'disgust': 0.02, 'fear': 0.03, 'joy': 0.94 and 'sadness': 0.02. The dominant emotion is <b>joy</b>.
```

### 3. Blank / Invalid Input
**Request:**
```text
GET /emotionDetector?textToAnalyze=
```
**Response (HTTP 200):**
```text
Invalid text! Please try again!
```

---

## Known Environment Limitations
- The host `sn-watson-emotion.labs.skills.network` resolves to private internal IP addresses (`10.241.x.x`) that are specifically routed within the IBM Skills Network Cloud Lab environment.
- When running outside the IBM Cloud Lab network, requests directly targeting that host will experience network timeouts. To ensure resilience, `emotion_detection.py` includes socket timeouts and safe fallback error handling, while `test_emotion_detection.py` incorporates unittest mocking so tests pass reliably in all environments.

---

## Evidence Directory
Submission evidence artifacts are available in the `evidence/` directory:
- `6b_deployment_test.png`: Browser view of valid statement analysis.
- `7c_error_handling_interface.png`: Browser view of blank statement error handling.
- `terminal_pylint_server.txt` & `terminal_pylint_score.txt`: 10.00/10 Pylint score validation.
- `terminal_unit_tests.txt`: Unit tests execution log.
- `terminal_import_execution.txt`: Package import log.
- `terminal_dictionary_format.txt`: JSON output format log.
- `terminal_package_validation.txt`: Package namespace verification log.
