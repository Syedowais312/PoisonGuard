from concurrent.futures import ThreadPoolExecutor

from poisonguard.detector.cosine_detector import CosineDetector
from poisonguard.detector.model_detector import ModelDetector
from poisonguard.detector.risk_scorer import RiskScorer


class DetectionPipeline:

    def __init__(self):

        self.cosine_detector = CosineDetector()
        self.model_detector = ModelDetector()
        self.risk_scorer = RiskScorer()

    def analyze(self, doc):

        title = str(doc.metadata.get("title", ""))
        metadata_text = " ".join(
            [str(value) for value in doc.metadata.values()]
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            cosine_future = executor.submit(
                self.cosine_detector.score,
                doc.content,
                metadata_text,
                title,
            )
            model_future = executor.submit(
                self.model_detector.predict,
                title,
                doc.content,
            )

            cosine_score = cosine_future.result()
            model_result = model_future.result()

        risk_score = self.risk_scorer.calculate(
            cosine_score=cosine_score,
            model_score=model_result["score"],
        )
        cosine_risk = self.risk_scorer.cosine_risk(
            cosine_score
        )
        model_risk = self.risk_scorer.model_risk(
            model_result["score"]
        )

        status = "SAFE"
        decision_reason = "passed-all-checks"

        if cosine_risk > 70:
            status = "BLOCKED"
            decision_reason = "similarity-layer-threshold"
        elif model_risk >= 80:
            status = "BLOCKED"
            decision_reason = "model-layer-threshold"
        elif risk_score > 70:
            status = "BLOCKED"
            decision_reason = "combined-risk-threshold"

        return {
            "document": doc,
            "title": title,
            "cosine_score": cosine_score,
            "cosine_risk": cosine_risk,
            "model_score": model_result["score"],
            "model_risk": model_risk,
            "model_label": model_result["label"],
            "model_source": model_result["source"],
            "risk_score": risk_score,
            "status": status,
            "decision_reason": decision_reason,
        }
