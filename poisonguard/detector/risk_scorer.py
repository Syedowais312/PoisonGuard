class RiskScorer:

    def calculate(
        self,
        cosine_score: float,
        model_score: float,
    ):

        cosine_risk = (1 - cosine_score) * 100
        model_risk = model_score * 100

        return int((cosine_risk * 0.5) + (model_risk * 0.5))

    def cosine_risk(self, cosine_score: float) -> int:

        return int((1 - cosine_score) * 100)

    def model_risk(self, model_score: float) -> int:

        return int(model_score * 100)
