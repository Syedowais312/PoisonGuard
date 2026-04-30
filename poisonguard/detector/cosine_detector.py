from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class CosineDetector:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the cosine similarity detector.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.embedder = SentenceTransformer(model_name)
        self.similarity_threshold = 0.3  # Threshold for detecting poisoning

    def score(
        self,
        content: str,
        metadata_text: str,
        title: str = "",
    ) -> float:
        """
        Calculate cosine similarity between title and content embeddings.
        Lower similarity indicates potential poisoning attack.
        
        Args:
            content: Document content
            metadata_text: Additional metadata text
            title: Document title
            
        Returns:
            float: Cosine similarity score (0-1, where lower = more suspicious)
        """
        # Combine title and metadata for comparison with content
        title_text = f"{title} {metadata_text}".strip()
        
        # Skip if either text is empty
        if not content.strip() or not title_text.strip():
            return 0.91  # Default to high similarity if no comparison possible
        
        try:
            # Generate embeddings
            title_embedding = self.embedder.encode([title_text])
            content_embedding = self.embedder.encode([content])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(title_embedding, content_embedding)[0][0]
            
            # Ensure score is in valid range
            similarity = max(0.0, min(1.0, similarity))
            
            return float(similarity)
            
        except Exception as e:
            # Fallback to keyword-based detection if embedding fails
            return self._fallback_score(title_text, content)

    def _fallback_score(self, title_text: str, content: str) -> float:
        """
        Fallback keyword-based scoring for when embedding fails.
        
        Args:
            title_text: Combined title and metadata
            content: Document content
            
        Returns:
            float: Similarity score
        """
        combined_text = f"{title_text} {content}".lower()
        
        suspicious_words = [
            "emergency",
            "override", 
            "critical",
            "urgent",
            "immediate",
            "security",
            "breach"
        ]
        
        # Check for suspicious keywords
        suspicious_count = sum(1 for word in suspicious_words if word in combined_text)
        
        if suspicious_count >= 2:
            return 0.12  # Low similarity (suspicious)
        elif suspicious_count == 1:
            return 0.5   # Medium similarity
        else:
            return 0.91  # High similarity (normal)

    def is_poisoned(self, content: str, metadata_text: str, title: str = "") -> bool:
        """
        Determine if document is poisoned based on similarity threshold.
        
        Args:
            content: Document content
            metadata_text: Additional metadata text  
            title: Document title
            
        Returns:
            bool: True if poisoned, False if safe
        """
        similarity = self.score(content, metadata_text, title)
        return similarity < self.similarity_threshold
