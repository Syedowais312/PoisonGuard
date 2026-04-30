import requests


class APIClient:

    def __init__(self):

        self.server_url = "http://127.0.0.1:5000"

    def send_result(self, result):

        payload = {
            "title": result["title"],
            "content": result["document"].content,
            "metadata": result["document"].metadata,
            "risk_score": result["risk_score"],
            "status": result["status"],
            "cosine_score": result["cosine_score"],
            "cosine_risk": result["cosine_risk"],
            "model_score": result["model_score"],
            "model_risk": result["model_risk"],
            "model_label": result["model_label"],
            "model_source": result["model_source"],
            "decision_reason": result["decision_reason"],
        }

        try:
            response = requests.post(
                f"{self.server_url}/log",
                json=payload,
                timeout=3,
            )

            print(response.json())
        except requests.RequestException as exc:
            print(f"PoisonGuard logging failed: {exc}")
