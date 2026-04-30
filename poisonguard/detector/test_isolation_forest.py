# test_isolation_forest.py
from sentence_transformers import SentenceTransformer
import joblib, json

# Load model + embedder
iso = joblib.load("poisonguard/detector/isolation_forest_model.joblib")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load poisoned dataset
with open("poisonguard/detector/poisoned_data.json", "r", encoding="utf-8") as f:
    poisoned_docs = json.load(f)

# Build features
def build_features(docs):
    features = []
    for doc in docs:
        content_vec = embedder.encode(doc["content"])
        metadata_vec = embedder.encode(doc["title"])
        combined = list(content_vec) + list(metadata_vec)
        features.append(combined)
    return features

X_poisoned = build_features(poisoned_docs)

# Evaluate
scores = iso.decision_function(X_poisoned)
preds = iso.predict(X_poisoned)  # -1 = anomaly, 1 = normal

for i, doc in enumerate(poisoned_docs[11:40]):
    print(f"Doc {i}: Title='{doc['title']}' | Score={scores[i]:.4f} | Pred={preds[i]}")
