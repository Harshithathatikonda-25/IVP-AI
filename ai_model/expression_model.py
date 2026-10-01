from pathlib import Path
import cv2
import numpy as np
from config import EMOTION_MODEL_PATH, EXPRESSIONS, IMAGE_SIZE

class ExpressionModel:
    def __init__(self):
        model_path = Path(EMOTION_MODEL_PATH)
        self.net = cv2.dnn.readNetFromONNX(str(model_path))

    def predict(self, face):
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (IMAGE_SIZE, IMAGE_SIZE), swapRB=False, crop=False
        )
        self.net.setInput(blob)
        scores = self.net.forward().reshape(-1).astype(np.float32)
        scores -= np.max(scores)
        probabilities = np.exp(scores)
        probabilities /= probabilities.sum()
        index = int(np.argmax(probabilities))
        confidence = float(probabilities[index])
        label = EXPRESSIONS[index]
        return label, confidence
