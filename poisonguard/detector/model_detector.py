class DefaultModelPredictor:

    def predict(self, title: str, content: str) -> dict:

        text = f"{title} {content}".lower()

        suspicious_words = [
            "emergency",
            "override",
            "critical",
        ]

        suspicious_hits = sum(
            1 for word in suspicious_words
            if word in text
        )

        score = min(1.0, 0.2 + suspicious_hits * 0.35)
        label = "poisoned" if score >= 0.5 else "clean"

        return {
            "score": round(score, 2),
            "label": label,
            "source": "default-model-layer",
        }


class ModelDetector:

    def __init__(self):

        self.predictor = DefaultModelPredictor()

    def predict(self, title: str, content: str) -> dict:

        return self.predictor.predict(title, content)
