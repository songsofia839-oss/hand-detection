from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

from detector import HandDetector

app = Flask(__name__)
CORS(app)

detector = HandDetector()


@app.route("/detect", methods=["POST"])
def detect():
    # Get image sent by JavaScript
    file = request.files["image"]

    # Convert uploaded image into OpenCV format
    image_bytes = file.read()
    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Run hand detection
    result = detector.detect(frame)

    # Encode annotated frame as JPEG
    success, buffer = cv2.imencode(".jpg", frame)

    if not success:
        return jsonify({"error": "Could not encode image"}), 500

    # Convert JPEG to base64
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    return jsonify({
        "number": result,
        "image": image_base64
    })


if __name__ == "__main__":
    app.run(debug=True)