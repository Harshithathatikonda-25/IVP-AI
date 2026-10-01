const expressionEmojiMap = {
    angry: { label: "Angry", emoji: "😠" },
    disgust: { label: "Disgust", emoji: "🤢" },
    fear: { label: "Fear", emoji: "😨" },
    happy: { label: "Happy", emoji: "😄" },
    sad: { label: "Sad", emoji: "😢" },
    surprise: { label: "Surprised", emoji: "😮" },
    neutral: { label: "Neutral", emoji: "😐" },
    contempt: { label: "Contempt", emoji: "😒" }
};

function updateFaceEffects(predictions) {
    const layer = document.getElementById("expressionEffects");

    while (layer.children.length > predictions.length) {
        layer.lastElementChild.remove();
    }

    predictions.forEach((prediction, index) => {
        const match = expressionEmojiMap[prediction.expression];
        if (!match) {
            return;
        }

        let effect = layer.children[index];
        if (!effect) {
            effect = document.createElement("span");
            effect.className = "expression-effect";
            layer.appendChild(effect);
        }

        if (effect.dataset.expression !== prediction.expression) {
            effect.textContent = match.emoji;
            effect.dataset.expression = prediction.expression;
            effect.classList.remove("pop");
            void effect.offsetWidth;
            effect.classList.add("pop");
        }

        effect.style.left = `${(prediction.face_box.x + prediction.face_box.width / 2) * 100}%`;
        effect.style.top = `${prediction.face_box.y * 100}%`;
    });
}

async function updateStatus() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();
        const predictions = data.face_predictions || [];
        const isModelMissing = !data.model_loaded;

        document.getElementById("expression").textContent =
            predictions.length
                ? "Expressions: " + predictions.map((prediction, index) => {
                    const label = expressionEmojiMap[prediction.expression]?.label || prediction.expression;
                    return `${index + 1}. ${label}`;
                }).join(" / ")
                : "Expressions: Waiting for a face";
        document.getElementById("confidence").textContent =
            "Primary face confidence: " + (data.confidence * 100).toFixed(1) + "%";
        document.getElementById("faces").textContent =
            "Faces detected: " + data.faces;
        document.getElementById("cameraState").textContent =
            data.faces > 0 ? `${data.faces} face${data.faces === 1 ? "" : "s"} in frame` : "Looking for a face";
        document.getElementById("modelStatus").textContent =
            isModelMissing ? "Demo mode" : "Model active";
        document.getElementById("modelStatus").classList.toggle("is-demo", isModelMissing);
        document.getElementById("modelHint").hidden = !isModelMissing;

        updateFaceEffects(predictions);
    } catch (error) {
        console.log(error);
    }
}
setInterval(updateStatus, 1000);
updateStatus();
