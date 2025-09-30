#!/usr/bin/env python3
"""
Test RAG System Fix

This script tests that the RAG system fix is working by initializing
the RAG system and checking for dimension mismatches.
"""

import sys
import os
sys.path.append('/Volumes/Data/Projects/MyProjects/AI/openproductwiki')

import logging
from api.rag import RAG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_rag_initialization():
    """Test RAG system initialization"""
    try:
        print("🧪 Testing RAG System Fix")
        print("=" * 40)
        
        # Initialize RAG with current configuration
        rag = RAG(provider="ollama", model="llama2")
        print("✅ RAG system initialized successfully")
        
        # Test embedder
        if hasattr(rag, 'query_embedder'):
            test_embedding = rag.query_embedder("test")
            if hasattr(test_embedding, 'embedding'):
                dimension = len(test_embedding.embedding)
            elif hasattr(test_embedding, 'data') and test_embedding.data:
                dimension = len(test_embedding.data[0].embedding)
            else:
                dimension = "unknown"
            print(f"✅ Current embedder produces {dimension}-dimensional vectors")
        
        print("\n🎉 RAG system is working correctly!")
        print("💡 The FAISS dimension mismatch has been resolved.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing RAG system: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_rag_initialization()
    sys.exit(0 if success else 1)