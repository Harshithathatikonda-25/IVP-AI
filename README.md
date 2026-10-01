# Facial Expression AI
## AI-Based Facial Expression Recognition using Image Processing and Deep Learning

### Pipeline
Camera / Video
-> YuNet Face Detection
-> Image Processing
-> Face Cropping
-> Grayscale + Resize to 64 x 64
-> FER+ Expression Classifier
-> Per-Face Expression + Confidence + Emoji
-> Dashboard

### Expression classes
neutral, happy, surprise, sad, angry, disgust, fear, contempt

This project classifies visible facial expressions in images/video frames. It should not be presented as a reliable measurement of a person's internal emotional state.

### Setup in VS Code

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

### Pretrained models
The app uses the ONNX FER+ expression classifier and YuNet face detector in `models/`. They run through OpenCV DNN; a custom Keras model and TensorFlow are not required. FER+ returns eight expression classes, and each detected face receives its own prediction and emoji overlay.

FER+ source: https://github.com/onnx/models/tree/main/validated/vision/body_analysis/emotion_ferplus
YuNet source: https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet

Predictions describe visible facial expressions and can be inaccurate; they do not reliably measure a person's internal emotional state. Review the model and dataset licenses before redistributing the model files.

Use only a properly licensed/public dataset and follow your institution's privacy requirements.
