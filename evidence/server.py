"""Flask server application for Emotion Detection."""

import os
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_analyzer():
    """Analyze the text submitted via query parameters and return emotion scores."""
    text_to_analyze = request.args.get("textToAnalyze")

    # Detect blank or whitespace-only input before calling external service
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    # Call emotion detector service
    response = emotion_detector(text_to_analyze)

    # Handle error or missing dominant emotion
    dominant_emotion = response.get("dominant_emotion")
    if dominant_emotion is None:
        return "Invalid text! Please try again!"

    anger = response.get("anger")
    disgust = response.get("disgust")
    fear = response.get("fear")
    joy = response.get("joy")
    sadness = response.get("sadness")

    return (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is <b>{dominant_emotion}</b>."
    )


@app.route("/")
def render_index_page():
    """Render the application home page."""
    return render_template("index.html")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port)
