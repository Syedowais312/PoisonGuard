import joblib
from sentence_transformers import SentenceTransformer


class IsolationForestDetector:
    
    def __init__(self, model_path: str = None):
        """
        Initialize the Isolation Forest detector.
        
        Args:
            model_path: Path to the trained isolation forest model
        """
        if model_path is None:
            model_path = "poisonguard/detector/isolation_forest_model.joblib"
        
        self.model = joblib.load(model_path)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    def build_features(self, title: str, content: str):
        """
        Build features for isolation forest prediction.
        
        Args:
            title: Document title
            content: Document content
            
        Returns:
            Combined feature vector
        """
        content_vec = self.embedder.encode(content)
        metadata_vec = self.embedder.encode(title)
        combined = list(content_vec) + list(metadata_vec)
        return combined
    
    def predict(self, title: str, content: str) -> dict:
        """
        Predict if document is poisoned using isolation forest.
        
        Args:
            title: Document title
            content: Document content
            
        Returns:
            Dictionary with score, label, and source
        """
        features = self.build_features(title, content)
        
        # Get anomaly score (lower = more anomalous)
        score = self.model.decision_function([features])[0]
        # Get prediction (-1 = anomaly, 1 = normal)
        prediction = self.model.predict([features])[0]
        
        # Convert score to 0-1 range where higher means more suspicious
        # Isolation forest decision_function: higher = more normal, lower = more anomalous
        # Use sigmoid-like transformation: negative scores become high suspicious scores
        import math
        normalized_score = 1 / (1 + math.exp(score))  # Lower scores -> higher suspicious scores
        
        label = "poisoned" if prediction == -1 else "clean"
        
        return {
            "score": round(normalized_score, 4),
            "label": label,
            "source": "isolation-forest-layer",
            "raw_score": float(score),
            "prediction": int(prediction)
        }
