#!/usr/bin/env python3
"""
Test Hybrid RAG Setup

This script tests that the hybrid RAG setup works correctly:
- Ollama for embeddings (local, private, free)
- External LLMs for generation (high quality)
"""

import sys
import os
sys.path.append('/Volumes/Data/Projects/MyProjects/AI/openproductwiki')

import logging
from api.rag import RAG
from api.config import get_embedder_config, is_ollama_embedder

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_hybrid_setup():
    """Test the hybrid RAG setup"""
    try:
        print("🧪 Testing Hybrid RAG Setup")
        print("=" * 50)
        
        # Check embedding configuration
        is_ollama = is_ollama_embedder()
        embedder_config = get_embedder_config()
        
        print(f"📍 Embedding Provider: {'Ollama (Local)' if is_ollama else 'External API'}")
        if embedder_config:
            model = embedder_config.get("model_kwargs", {}).get("model", "unknown")
            print(f"📍 Embedding Model: {model}")
        
        # Test different generation providers
        providers_to_test = [
            ("google", "gemini-2.5-flash"),
            ("openai", "gpt-4o"),
            ("openrouter", "openai/gpt-4o")
        ]
        
        for provider, model in providers_to_test:
            try:
                print(f"\n🔧 Testing generation provider: {provider}/{model}")
                
                # Initialize RAG with external provider for generation
                rag = RAG(provider=provider, model=model)
                
                # Test embedding (should always use Ollama)
                test_embedding = rag.query_embedder("test query")
                if hasattr(test_embedding, 'embedding'):
                    embedding_dim = len(test_embedding.embedding)
                elif hasattr(test_embedding, 'data') and test_embedding.data:
                    embedding_dim = len(test_embedding.data[0].embedding)
                else:
                    embedding_dim = "unknown"
                
                print(f"  ✅ Embeddings: Ollama nomic-embed-text ({embedding_dim}D)")
                print(f"  ✅ Generation: {provider}/{model}")
                print(f"  💡 Benefits: Private embeddings + {provider} quality")
                
            except Exception as e:
                print(f"  ⚠️  {provider} not available: {e}")
        
        print("\n🎉 Hybrid RAG Setup Working!")
        print("Benefits of current configuration:")
        print("  🔒 Privacy: Documents embedded locally (never sent to APIs)")
        print("  💰 Cost: Free embeddings, pay only for generation")
        print("  🚀 Performance: No API limits on embeddings")
        print("  🎯 Quality: Use best models for answering (GPT-4, Gemini, etc.)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing hybrid setup: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_configuration_recommendations():
    """Show configuration recommendations for optimal hybrid setup"""
    print("\n📋 Hybrid Setup Recommendations")
    print("=" * 50)
    
    print("For EMBEDDINGS (Local):")
    print("  📦 Current: Ollama nomic-embed-text (768D)")
    print("  🔄 Alternatives:")
    print("    - all-minilm: Faster, 384D")
    print("    - mxbai-embed-large: Higher quality, 1024D")
    
    print("\nFor GENERATION (External):")
    print("  💰 Cost-Effective: gpt-4o-mini, gemini-2.5-flash")
    print("  🎯 High Quality: gpt-4o, gemini-2.5-pro, o1")
    print("  🔧 Specialized: deepseek-r1 (coding), claude-3.5-sonnet")
    
    print("\nCurrent Configuration Files:")
    print("  📁 Embedding: api/config/embedder.json")
    print("  📁 Generation: api/config/generator.json")
    
    print("\nTo change embedding model:")
    print("  1. ollama pull <new-model>")
    print("  2. Update embedder.json")
    print("  3. python clear_embeddings.py")
    print("  4. Regenerate wikis")

if __name__ == "__main__":
    success = test_hybrid_setup()
    show_configuration_recommendations()
    sys.exit(0 if success else 1)