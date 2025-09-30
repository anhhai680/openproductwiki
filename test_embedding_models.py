#!/usr/bin/env python3
"""
Embedding Model Testing Utility

This script helps test different embedding models and their dimensions
to avoid FAISS dimension mismatch issues.
"""

import sys
import os
import json
import requests
from pathlib import Path

def test_ollama_model(model_name):
    """Test an Ollama embedding model"""
    try:
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        
        # Check if model exists
        response = requests.get(f"{ollama_host}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            available_models = [m.get('name', '').split(':')[0] for m in models]
            
            if model_name not in available_models:
                print(f"❌ Model '{model_name}' not available in Ollama")
                print(f"   Available models: {', '.join(available_models)}")
                print(f"   To install: ollama pull {model_name}")
                return None
        
        # Test embedding
        test_data = {
            'model': model_name,
            'prompt': 'test embedding dimensions'
        }
        
        response = requests.post(f"{ollama_host}/api/embeddings", json=test_data, timeout=10)
        if response.status_code == 200:
            embedding_data = response.json()
            if 'embedding' in embedding_data:
                dimensions = len(embedding_data['embedding'])
                print(f"✅ {model_name}: {dimensions} dimensions")
                return dimensions
            else:
                print(f"❌ No embedding in response for {model_name}")
                return None
        else:
            print(f"❌ Failed to get embedding from {model_name}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing {model_name}: {e}")
        return None

def test_openai_dimensions():
    """Test OpenAI embedding dimensions with different configurations"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set, skipping OpenAI tests")
        return
    
    print("\n🔍 Testing OpenAI embedding dimensions...")
    
    configs = [
        {"model": "text-embedding-3-small", "dimensions": 768},
        {"model": "text-embedding-3-small", "dimensions": 1536},
        {"model": "text-embedding-ada-002"}  # No dimensions param
    ]
    
    for config in configs:
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            response = client.embeddings.create(
                input="test embedding dimensions",
                **config
            )
            
            dimensions = len(response.data[0].embedding)
            model_name = config['model']
            config_dims = config.get('dimensions', 'default')
            
            print(f"✅ {model_name} (config: {config_dims}D): {dimensions} actual dimensions")
            
        except Exception as e:
            print(f"❌ Error testing OpenAI {config}: {e}")

def show_dimension_compatibility():
    """Show which models are compatible with current setup"""
    
    current_config_path = Path("api/config/embedder.json")
    if current_config_path.exists():
        with open(current_config_path) as f:
            config = json.load(f)
            current_model = config.get("embedder", {}).get("model_kwargs", {}).get("model", "unknown")
    else:
        current_model = "unknown"
    
    print(f"\n📊 Current Model: {current_model}")
    
    # Test current model
    if current_model != "unknown":
        current_dims = test_ollama_model(current_model)
        if current_dims:
            print(f"📏 Current Dimensions: {current_dims}D")
            
            print(f"\n✅ Compatible Models (same {current_dims}D):")
            
            compatible_models = {
                384: ["all-minilm", "all-MiniLM-L6-v2"],
                768: ["nomic-embed-text", "all-mpnet-base-v2", "text-embedding-3-small (768D config)"],
                1024: ["mxbai-embed-large", "e5-large-v2"],
                1536: ["text-embedding-ada-002", "text-embedding-3-small (default)"]
            }
            
            if current_dims in compatible_models:
                for model in compatible_models[current_dims]:
                    print(f"  • {model}")
            
            print(f"\n⚠️  Incompatible Models (require clear_embeddings.py):")
            for dims, models in compatible_models.items():
                if dims != current_dims:
                    print(f"  {dims}D: {', '.join(models)}")

def create_config_templates():
    """Create configuration templates for different models"""
    
    templates = {
        "nomic-embed-text-768d.json": {
            "embedder": {
                "client_class": "OllamaClient",
                "model_kwargs": {
                    "model": "nomic-embed-text"
                }
            },
            "retriever": {"top_k": 20},
            "text_splitter": {"split_by": "word", "chunk_size": 350, "chunk_overlap": 100}
        },
        "openai-768d-compatible.json": {
            "embedder": {
                "client_class": "OpenAIClient",
                "model_kwargs": {
                    "model": "text-embedding-3-small",
                    "dimensions": 768,
                    "encoding_format": "float"
                }
            },
            "retriever": {"top_k": 20},
            "text_splitter": {"split_by": "word", "chunk_size": 350, "chunk_overlap": 100}
        },
        "performance-384d.json": {
            "embedder": {
                "client_class": "OllamaClient",
                "model_kwargs": {
                    "model": "all-minilm"
                }
            },
            "retriever": {"top_k": 20},
            "text_splitter": {"split_by": "word", "chunk_size": 350, "chunk_overlap": 100}
        }
    }
    
    config_dir = Path("api/config/templates")
    config_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Creating configuration templates in {config_dir}/")
    
    for filename, config in templates.items():
        template_path = config_dir / filename
        with open(template_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"  ✅ Created: {filename}")

def main():
    """Main function"""
    print("🧪 Embedding Model Testing Utility")
    print("=" * 50)
    
    print("\n🔍 Testing available Ollama models...")
    ollama_models = ["nomic-embed-text", "all-minilm", "mxbai-embed-large"]
    
    for model in ollama_models:
        test_ollama_model(model)
    
    test_openai_dimensions()
    show_dimension_compatibility()
    create_config_templates()
    
    print("\n💡 Recommendations:")
    print("  • Keep current nomic-embed-text (768D) - it's optimal")
    print("  • If switching to OpenAI, use dimensions=768 for compatibility")
    print("  • Use clear_embeddings.py when changing dimension sizes")
    print("  • Test new configs with: python test_hybrid_setup.py")

if __name__ == "__main__":
    main()