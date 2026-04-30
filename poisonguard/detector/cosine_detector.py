class CosineDetector:

    def score(
        self,
        content: str,
        metadata_text: str,
        title: str = "",
    ) -> float:

        combined_text = f"{title} {metadata_text}".lower()

        suspicious_words = [
            "emergency",
            "override",
            "critical",
        ]

        for word in suspicious_words:

            if word in combined_text:

                return 0.12

        return 0.91
