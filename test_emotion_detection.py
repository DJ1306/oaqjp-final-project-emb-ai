"""Unit tests for EmotionDetection package."""

import json as _json
import unittest
from unittest.mock import patch
from EmotionDetection.emotion_detection import emotion_detector


def mocked_requests_post(*args, **kwargs):
    """Mock requests.post for Watson NLP emotion detection API."""
    class MockResponse:  # pylint: disable=too-few-public-methods
        """Mock HTTP response."""
        def __init__(self, data, status_code):
            self.data = data
            self.status_code = status_code
            self.text = _json.dumps(data)

        def json(self):
            """Return json response data."""
            return self.data

    _ = args
    json_payload = kwargs.get("json", {})
    text = ""
    if json_payload and "raw_document" in json_payload and "text" in json_payload["raw_document"]:
        text = json_payload["raw_document"]["text"]

    if not text or not text.strip():
        return MockResponse({}, 400)

    # Return realistic Watson NLP scores based on test sentences
    scores = {
        "anger": 0.02,
        "disgust": 0.02,
        "fear": 0.02,
        "joy": 0.02,
        "sadness": 0.02,
    }

    if "glad" in text.lower():
        scores["joy"] = 0.90
    elif "mad" in text.lower():
        scores["anger"] = 0.90
    elif "disgusted" in text.lower():
        scores["disgust"] = 0.90
    elif "sad" in text.lower():
        scores["sadness"] = 0.90
    elif "afraid" in text.lower():
        scores["fear"] = 0.90
    else:
        scores["joy"] = 0.50

    response_payload = {
        "emotionPredictions": [
            {
                "emotion": scores,
                "target": ""
            }
        ],
        "producerId": {
            "name": "Aggregated Emotion Workflow",
            "version": "0.0.1"
        }
    }
    return MockResponse(response_payload, 200)


@patch("requests.post", side_effect=mocked_requests_post)
class TestEmotionDetection(unittest.TestCase):
    """Test suite for emotion detection functionality."""

    def test_emotion_detector(self, _):
        """Test the five standard statements and verify dominant emotion."""
        # Statement 1 - Joy
        result_1 = emotion_detector("I am glad this happened")
        self.assertEqual(result_1["dominant_emotion"], "joy")
        self.assertIn("anger", result_1)
        self.assertIn("disgust", result_1)
        self.assertIn("fear", result_1)
        self.assertIn("joy", result_1)
        self.assertIn("sadness", result_1)

        # Statement 2 - Anger
        result_2 = emotion_detector("I am really mad about this")
        self.assertEqual(result_2["dominant_emotion"], "anger")

        # Statement 3 - Disgust
        result_3 = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result_3["dominant_emotion"], "disgust")

        # Statement 4 - Sadness
        result_4 = emotion_detector("I am so sad about this")
        self.assertEqual(result_4["dominant_emotion"], "sadness")

        # Statement 5 - Fear
        result_5 = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result_5["dominant_emotion"], "fear")

    def test_emotion_detector_blank_input(self, _):
        """Test emotion detector handles blank input / status 400 properly."""
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        for emotion in ["anger", "disgust", "fear", "joy", "sadness"]:
            self.assertIsNone(result[emotion])


if __name__ == "__main__":
    unittest.main()
