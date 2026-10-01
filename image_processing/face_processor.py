import cv2
import numpy as np
from config import FACE_DETECTOR_MODEL_PATH, IMAGE_SIZE

class FaceProcessor:
    def __init__(self):
        self.detector = cv2.FaceDetectorYN_create(
            FACE_DETECTOR_MODEL_PATH, "", (320, 320), 0.6, 0.3, 5000
        )

    def detect_faces(self, frame):
        frame_height, frame_width = frame.shape[:2]
        self.detector.setInputSize((frame_width, frame_height))
        _, detections = self.detector.detect(frame)
        if detections is None:
            return []

        faces = []
        for detection in detections:
            x, y, width, height = detection[:4]
            left = max(0, int(np.floor(x)))
            top = max(0, int(np.floor(y)))
            right = min(frame_width, int(np.ceil(x + width)))
            bottom = min(frame_height, int(np.ceil(y + height)))
            if right > left and bottom > top:
                faces.append((left, top, right - left, bottom - top))
        return faces

    def preprocess_face(self, frame, box):
        x, y, w, h = box
        face = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        return cv2.resize(gray, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA)
