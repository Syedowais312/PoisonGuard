#!/usr/bin/env python3
"""
Test script to verify Layer 1 (Cosine) and Layer 2 (Isolation Forest) detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from poisonguard.detector.cosine_detector import CosineDetector
from poisonguard.detector.isolation_forest_detector import IsolationForestDetector
from poisonguard.detector.model_detector import ModelDetector
from poisonguard.detector.pipeline import DetectionPipeline

# Test documents
test_docs = [
    {
        "title": "Normal Business Document",
        "content": "This is a standard business report about quarterly earnings and market analysis. The company performed well with increased revenue."
    },
    {
        "title": "Emergency Override Protocol",
        "content": "CRITICAL: Emergency override required immediately. This is a critical security breach that needs urgent attention."
    },
    {
        "title": "Technical Documentation",
        "content": "API documentation for the authentication system. Includes examples of token validation and user management."
    }
]

class MockDocument:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = metadata

def test_layer1_cosine():
    """Test Layer 1: Cosine Similarity Detection"""
    print("=" * 50)
    print("TESTING LAYER 1: COSINE SIMILARITY DETECTION")
    print("=" * 50)
    
    cosine_detector = CosineDetector()
    
    for i, doc in enumerate(test_docs):
        print(f"\nDocument {i+1}: {doc['title']}")
        print(f"Content: {doc['content'][:100]}...")
        
        score = cosine_detector.score(
            doc['content'], 
            "",  # metadata_text
            doc['title']
        )
        
        print(f"Cosine Score: {score:.4f}")
        risk_level = "HIGH" if score > 0.8 else "MEDIUM" if score > 0.5 else "LOW"
        print(f"Risk Level: {risk_level}")

def test_layer2_isolation_forest():
    """Test Layer 2: Isolation Forest Detection"""
    print("\n" + "=" * 50)
    print("TESTING LAYER 2: ISOLATION FOREST DETECTION")
    print("=" * 50)
    
    try:
        iso_detector = IsolationForestDetector()
        
        for i, doc in enumerate(test_docs):
            print(f"\nDocument {i+1}: {doc['title']}")
            print(f"Content: {doc['content'][:100]}...")
            
            result = iso_detector.predict(doc['title'], doc['content'])
            
            print(f"Score: {result['score']:.4f}")
            print(f"Label: {result['label']}")
            print(f"Source: {result['source']}")
            print(f"Raw Score: {result.get('raw_score', 'N/A'):.4f}")
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            
    except Exception as e:
        print(f"Error testing isolation forest: {e}")
        print("This might be due to missing model file or dependencies.")

def test_model_detector():
    """Test ModelDetector with isolation forest"""
    print("\n" + "=" * 50)
    print("TESTING MODEL DETECTOR (ISOLATION FOREST)")
    print("=" * 50)
    
    try:
        model_detector = ModelDetector(use_isolation_forest=True)
        
        for i, doc in enumerate(test_docs):
            print(f"\nDocument {i+1}: {doc['title']}")
            result = model_detector.predict(doc['title'], doc['content'])
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"Error testing model detector: {e}")

def test_fallback_detector():
    """Test fallback to keyword-based detection"""
    print("\n" + "=" * 50)
    print("TESTING FALLBACK DETECTOR (KEYWORD-BASED)")
    print("=" * 50)
    
    try:
        model_detector = ModelDetector(use_isolation_forest=False)
        
        for i, doc in enumerate(test_docs):
            print(f"\nDocument {i+1}: {doc['title']}")
            result = model_detector.predict(doc['title'], doc['content'])
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"Error testing fallback detector: {e}")

def test_full_pipeline():
    """Test the complete detection pipeline"""
    print("\n" + "=" * 50)
    print("TESTING FULL DETECTION PIPELINE")
    print("=" * 50)
    
    try:
        pipeline = DetectionPipeline()
        
        for i, doc in enumerate(test_docs):
            mock_doc = MockDocument(doc['content'], {"title": doc['title']})
            
            print(f"\nDocument {i+1}: {doc['title']}")
            result = pipeline.analyze(mock_doc)
            
            print(f"Cosine Score: {result['cosine_score']:.4f}")
            print(f"Model Score: {result['model_score']:.4f}")
            print(f"Risk Score: {result['risk_score']:.4f}")
            print(f"Status: {result['status']}")
            print(f"Decision Reason: {result['decision_reason']}")
            print(f"Model Source: {result['model_source']}")
            
    except Exception as e:
        print(f"Error testing full pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing PoisonGuard Detection Layers")
    print("====================================")
    
    test_layer1_cosine()
    test_layer2_isolation_forest()
    test_model_detector()
    test_fallback_detector()
    test_full_pipeline()
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)
