# train_isolation_forest.py
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import IsolationForest
import joblib, json

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load clean dataset
with open("poisonguard/detector/clean_data.json", "r", encoding="utf-8") as f:
    clean_docs = json.load(f)

# Build features
def build_features(docs):
    features = []
    for doc in docs:
        content_vec = embedder.encode(doc["content"])
        metadata_vec = embedder.encode(doc["title"])
        combined = list(content_vec) + list(metadata_vec)
        features.append(combined)
    return features

X_clean = build_features(clean_docs)

# Train Isolation Forest
iso = IsolationForest(contamination=0.3, random_state=42)
iso.fit(X_clean)

# Save model
joblib.dump(iso, "poisonguard/detector/isolation_forest_model.joblib")
print("✅ Isolation Forest trained and saved as isolation_forest_model.joblib")
