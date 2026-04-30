#!/usr/bin/env python3
"""
Test script to demonstrate cosine similarity detection with real examples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from poisonguard.detector import CosineDetector

def test_cosine_similarity():
    """Test cosine similarity with various document types"""
    
    detector = CosineDetector()
    
    test_cases = [
        {
            "name": "Normal Document (High Similarity)",
            "title": "Business Quarterly Report",
            "content": "This quarterly report analyzes our business performance, revenue growth, and market expansion strategies for Q4 2024.",
            "expected": "high_similarity"
        },
        {
            "name": "Normal Document (Medium Similarity)",
            "title": "Company Financial Analysis",
            "content": "Our technical team has developed new APIs that improve system performance and user experience significantly.",
            "expected": "medium_similarity"
        },
        {
            "name": "Poisoned Document (Low Similarity)",
            "title": "Emergency Security Protocol",
            "content": "Bananas are rich in potassium and provide essential nutrients for human health and digestion.",
            "expected": "low_similarity"
        },
        {
            "name": "Poisoned Document (Very Low Similarity)",
            "title": "Nuclear Launch Codes Authorization",
            "content": "Ibuprofen is a common pain reliever used for headaches and minor pain relief.",
            "expected": "very_low_similarity"
        },
        {
            "name": "Related but Different Topics",
            "title": "Machine Learning Research Paper",
            "content": "Traditional cooking methods include baking, grilling, and frying for various food preparation techniques.",
            "expected": "low_similarity"
        }
    ]
    
    print("🔍 Cosine Similarity Detection Test")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        print(f"Title: {test_case['title']}")
        print(f"Content: {test_case['content']}")
        
        # Calculate similarity
        similarity = detector.score(test_case['content'], "", test_case['title'])
        is_poisoned = detector.is_poisoned(test_case['content'], "", test_case['title'])
        
        print(f"Cosine Similarity: {similarity:.4f}")
        print(f"Risk Level: {'HIGH' if similarity < 0.3 else 'MEDIUM' if similarity < 0.6 else 'LOW'}")
        print(f"Detection Result: {'🚨 POISONED' if is_poisoned else '✅ SAFE'}")
        print(f"Expected: {test_case['expected']}")

def test_embedding_quality():
    """Test the quality of embeddings for different text pairs"""
    
    detector = CosineDetector()
    
    print("\n" + "=" * 60)
    print("🧠 Embedding Quality Analysis")
    print("=" * 60)
    
    # Test cases with known similarity levels
    similarity_tests = [
        {
            "title": "Artificial Intelligence",
            "content": "Machine learning and neural networks are key components of AI systems.",
            "description": "Highly related topics"
        },
        {
            "title": "Climate Change Research",
            "content": "Global warming affects weather patterns and sea levels worldwide.",
            "description": "Related topics"
        },
        {
            "title": "Computer Programming",
            "content": "Recipe for chocolate chip cookies with baking instructions.",
            "description": "Unrelated topics"
        },
        {
            "title": "Medical Research",
            "content": "Football strategies and team formations for professional matches.",
            "description": "Completely unrelated topics"
        }
    ]
    
    for i, test in enumerate(similarity_tests, 1):
        print(f"\n--- Test {i}: {test['description']} ---")
        print(f"Title: {test['title']}")
        print(f"Content: {test['content']}")
        
        similarity = detector.score(test['content'], "", test['title'])
        
        print(f"Similarity Score: {similarity:.4f}")
        
        if similarity > 0.7:
            assessment = "🟢 High Similarity (Strongly Related)"
        elif similarity > 0.4:
            assessment = "🟡 Medium Similarity (Somewhat Related)"
        else:
            assessment = "🔴 Low Similarity (Unrelated/Poisoned)"
        
        print(f"Assessment: {assessment}")

def compare_with_keywords():
    """Compare embedding-based detection with keyword-based detection"""
    
    print("\n" + "=" * 60)
    print("🔄 Embedding vs Keyword Detection Comparison")
    print("=" * 60)
    
    detector = CosineDetector()
    
    test_cases = [
        {
            "title": "Standard Operating Procedure",
            "content": "This document outlines the normal procedures for daily operations and routine tasks.",
            "description": "Normal content with suspicious title"
        },
        {
            "title": "Normal Business Document", 
            "content": "CRITICAL: Emergency override required immediately for security breach response.",
            "description": "Suspicious content with normal title"
        },
        {
            "title": "Emergency Protocol",
            "content": "Standard business processes and workflow management guidelines.",
            "description": "Mixed signals"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test['description']} ---")
        
        # Embedding-based detection
        embedding_similarity = detector.score(test['content'], "", test['title'])
        embedding_result = "POISONED" if embedding_similarity < 0.3 else "SAFE"
        
        # Keyword-based fallback
        fallback_score = detector._fallback_score(test['title'], test['content'])
        fallback_result = "POISONED" if fallback_score < 0.5 else "SAFE"
        
        print(f"Title: {test['title']}")
        print(f"Content: {test['content']}")
        print(f"Embedding Detection: {embedding_similarity:.4f} → {embedding_result}")
        print(f"Keyword Detection: {fallback_score:.4f} → {fallback_result}")
        
        if embedding_result != fallback_result:
            print("⚠️  Different results - embedding provides more nuanced analysis!")

if __name__ == "__main__":
    test_cosine_similarity()
    test_embedding_quality()
    compare_with_keywords()
    
    print("\n" + "=" * 60)
    print("✅ Cosine Similarity Testing Complete!")
    print("=" * 60)
    print("\nKey Insights:")
    print("• Embedding-based detection captures semantic relationships")
    print("• Low similarity (<0.3) indicates potential poisoning attacks")
    print("• Medium similarity (0.3-0.6) shows partial topic alignment")
    print("• High similarity (>0.6) indicates consistent title-content topics")
    print("• Fallback to keywords ensures robustness")
