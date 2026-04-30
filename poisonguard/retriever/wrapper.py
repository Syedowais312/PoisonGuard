class PoisonGuardRetriever:

    def __init__(self, base_retriever):

        self.base_retriever = base_retriever
        
        # Lazy imports to avoid circular dependencies
        self._pipeline = None
        self._api_client = None
    
    @property
    def pipeline(self):
        if self._pipeline is None:
            from poisonguard.detector.pipeline import DetectionPipeline
            self._pipeline = DetectionPipeline()
        return self._pipeline
    
    @property
    def api_client(self):
        if self._api_client is None:
            from poisonguard.client.api_client import APIClient
            self._api_client = APIClient()
        return self._api_client

    def retrieve(self, query):

        docs = self.base_retriever.retrieve(query)

        safe_docs = []

        for doc in docs:

            result = self.pipeline.analyze(doc)

            self.api_client.send_result(result)

            if result["status"] == "SAFE":

                safe_docs.append(doc)

        return safe_docs
