import cv2
from flask import Flask, render_template, Response, jsonify
from image_processing.face_processor import FaceProcessor
from ai_model.expression_model import ExpressionModel
from config import CAMERA_SOURCE

app = Flask(__name__, template_folder="dashboard/templates",
            static_folder="dashboard/static")

camera = cv2.VideoCapture(CAMERA_SOURCE)
face_processor = FaceProcessor()
model = ExpressionModel()

latest = {
    "expression": "Waiting",
    "confidence": 0.0,
    "faces": 0,
    "face_box": None,
    "face_predictions": [],
    "model_loaded": model.net is not None,
}

def generate_frames():
    global latest

    while True:
        ok, frame = camera.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        faces = face_processor.detect_faces(frame)
        frame_height, frame_width = frame.shape[:2]
        face_predictions = []

        for (x, y, w, h) in faces:
            face = face_processor.preprocess_face(frame, (x, y, w, h))
            label, confidence = model.predict(face)
            face_predictions.append({
                "expression": label,
                "confidence": confidence,
                "face_box": {
                    "x": x / frame_width,
                    "y": y / frame_height,
                    "width": w / frame_width,
                    "height": h / frame_height,
                },
            })

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.putText(
                frame, f"{label}: {confidence:.1%}",
                (x, max(25, y-10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 255, 255), 2
            )

        primary = max(face_predictions, key=lambda item: item["face_box"]["width"] * item["face_box"]["height"], default=None)
        latest.update({
            "faces": len(faces),
            "face_predictions": face_predictions,
            "expression": primary["expression"] if primary else "Waiting",
            "confidence": primary["confidence"] if primary else 0.0,
            "face_box": primary["face_box"] if primary else None,
        })

        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue

        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
               buffer.tobytes() + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/api/status")
def status():
    return jsonify(latest)

if __name__ == "__main__":
    app.run(debug=True)
