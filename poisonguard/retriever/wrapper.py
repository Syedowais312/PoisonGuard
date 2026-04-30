from poisonguard.detector.pipeline import DetectionPipeline
from poisonguard.client.api_client import APIClient


class PoisonGuardRetriever:

    def __init__(self, base_retriever):

        self.base_retriever = base_retriever

        self.pipeline = DetectionPipeline()

        self.api_client = APIClient()

    def retrieve(self, query):

        docs = self.base_retriever.retrieve(query)

        safe_docs = []

        for doc in docs:

            result = self.pipeline.analyze(doc)

            self.api_client.send_result(result)

            if result["status"] == "SAFE":

                safe_docs.append(doc)

        return safe_docs
