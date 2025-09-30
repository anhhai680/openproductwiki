#!/usr/bin/env python3
"""
Embedding Model Comparison Tool

This script compares different embedding models and their characteristics
to help choose the best option for OpenProductWiki.
"""

import sys
import os
sys.path.append('/Volumes/Data/Projects/MyProjects/AI/openproductwiki')

import requests
import json

def get_embedding_models_info():
    """Get information about different embedding models"""
    
    models = {
        "Ollama Models": {
            "nomic-embed-text": {
                "dimensions": 768,
                "max_tokens": 8192,
                "provider": "Ollama (Local)",
                "cost": "Free",
                "privacy": "100% Local",
                "performance": "Fast",
                "quality": "High",
                "notes": "Current model, good for general text"
            },
            "all-minilm": {
                "dimensions": 384,
                "max_tokens": 512,
                "provider": "Ollama (Local)",
                "cost": "Free",
                "privacy": "100% Local", 
                "performance": "Very Fast",
                "quality": "Good",
                "notes": "Smaller, faster model"
            },
            "mxbai-embed-large": {
                "dimensions": 1024,
                "max_tokens": 512,
                "provider": "Ollama (Local)",
                "cost": "Free",
                "privacy": "100% Local",
                "performance": "Slower",
                "quality": "Very High",
                "notes": "Highest quality Ollama model"
            }
        },
        "OpenAI Models": {
            "text-embedding-3-small": {
                "dimensions": "256-1536 (configurable)",
                "max_tokens": 8191,
                "provider": "OpenAI API",
                "cost": "$0.02/1M tokens",
                "privacy": "External API",
                "performance": "API dependent",
                "quality": "High",
                "notes": "Flexible dimensions, widely used"
            },
            "text-embedding-3-large": {
                "dimensions": "256-3072 (configurable)",
                "max_tokens": 8191,
                "provider": "OpenAI API", 
                "cost": "$0.13/1M tokens",
                "privacy": "External API",
                "performance": "API dependent",
                "quality": "Very High",
                "notes": "Best OpenAI embedding model"
            },
            "text-embedding-ada-002": {
                "dimensions": 1536,
                "max_tokens": 8191,
                "provider": "OpenAI API",
                "cost": "$0.10/1M tokens",
                "privacy": "External API", 
                "performance": "API dependent",
                "quality": "High",
                "notes": "Legacy model, still widely used"
            }
        },
        "Hugging Face Models": {
            "all-MiniLM-L6-v2": {
                "dimensions": 384,
                "max_tokens": 512,
                "provider": "Local/API",
                "cost": "Free (local)",
                "privacy": "Configurable",
                "performance": "Fast",
                "quality": "Good",
                "notes": "Most popular sentence transformer"
            },
            "all-mpnet-base-v2": {
                "dimensions": 768,
                "max_tokens": 514,
                "provider": "Local/API",
                "cost": "Free (local)",
                "privacy": "Configurable", 
                "performance": "Medium",
                "quality": "High",
                "notes": "Better quality than MiniLM"
            },
            "e5-large-v2": {
                "dimensions": 1024,
                "max_tokens": 512,
                "provider": "Local/API",
                "cost": "Free (local)",
                "privacy": "Configurable",
                "performance": "Slower",
                "quality": "Very High", 
                "notes": "State-of-the-art open model"
            }
        }
    }
    
    return models

def analyze_dimension_compatibility():
    """Analyze dimension compatibility issues"""
    
    print("📏 Dimension Compatibility Analysis")
    print("=" * 60)
    
    common_dimensions = {
        "384": ["all-MiniLM-L6-v2", "all-minilm (Ollama)"],
        "768": ["nomic-embed-text (Ollama)", "all-mpnet-base-v2", "text-embedding-3-small (768d config)"],
        "1024": ["mxbai-embed-large (Ollama)", "e5-large-v2"],
        "1536": ["text-embedding-ada-002", "text-embedding-3-small (default)"],
        "3072": ["text-embedding-3-large (max)"]
    }
    
    for dim, models in common_dimensions.items():
        print(f"\n{dim}D Models:")
        for model in models:
            print(f"  • {model}")
    
    print("\n⚠️  Dimension Mismatch Issues:")
    print("  • Different models = different dimensions")
    print("  • FAISS requires all vectors to have same dimensions")
    print("  • Changing models requires clearing old embeddings")
    print("  • Solution: Use clear_embeddings.py when switching")

def recommend_best_model():
    """Recommend the best embedding model for this project"""
    
    print("\n🎯 Recommendations for OpenProductWiki")
    print("=" * 60)
    
    recommendations = {
        "Best Overall (Current)": {
            "model": "nomic-embed-text (Ollama)",
            "dimensions": 768,
            "reasons": [
                "✅ 100% private - documents never leave your machine",
                "✅ Free - no API costs",
                "✅ Fast - no network latency",
                "✅ Good quality - comparable to OpenAI small",
                "✅ Common dimension (768) - compatible with many models",
                "✅ Large context (8192 tokens) - handles big code files"
            ]
        },
        "Best Performance": {
            "model": "all-minilm (Ollama)",
            "dimensions": 384,
            "reasons": [
                "✅ Fastest embedding speed",
                "✅ Smallest memory footprint", 
                "✅ Still good quality for most use cases",
                "⚠️ Smaller dimension may lose some semantic detail"
            ]
        },
        "Best Quality": {
            "model": "mxbai-embed-large (Ollama)",
            "dimensions": 1024,
            "reasons": [
                "✅ Highest quality embeddings",
                "✅ Better semantic understanding",
                "✅ Still private and free",
                "⚠️ Slower processing",
                "⚠️ More memory usage"
            ]
        },
        "Best for OpenAI Migration": {
            "model": "text-embedding-3-small (768D config)",
            "dimensions": 768,
            "reasons": [
                "✅ Same dimensions as current setup",
                "✅ No migration issues when switching",
                "✅ High quality",
                "❌ Costs money",
                "❌ Privacy concerns",
                "❌ API dependency"
            ]
        }
    }
    
    for category, info in recommendations.items():
        print(f"\n{category}:")
        print(f"  Model: {info['model']}")
        print(f"  Dimensions: {info['dimensions']}D")
        print("  Reasons:")
        for reason in info['reasons']:
            print(f"    {reason}")

def migration_strategy():
    """Provide migration strategy for changing embedding models"""
    
    print("\n🔄 Migration Strategy")
    print("=" * 60)
    
    print("To avoid dimension mismatch issues in the future:")
    print("\n1. Standardize on 768 dimensions:")
    print("   • Current: nomic-embed-text (768D) ✅")
    print("   • Future OpenAI: text-embedding-3-small with dimensions=768")
    print("   • Alternative: all-mpnet-base-v2 (768D)")
    
    print("\n2. Migration process when changing models:")
    print("   • Update embedder.json configuration")
    print("   • Run: python clear_embeddings.py")
    print("   • Regenerate wikis with new model")
    print("   • Test with: python test_hybrid_setup.py")
    
    print("\n3. Configuration for future-proofing:")
    print("   • Use configurable dimension in text-embedding-3-small")
    print("   • Keep dimension validation in rag.py")
    print("   • Maintain embedding model abstraction")
    
    print("\n4. Recommended configurations:")
    
    configs = {
        "Current (Recommended)": {
            "model": "nomic-embed-text",
            "provider": "Ollama",
            "dimensions": 768,
            "config": '{"client_class": "OllamaClient", "model_kwargs": {"model": "nomic-embed-text"}}'
        },
        "OpenAI Compatible": {
            "model": "text-embedding-3-small",
            "provider": "OpenAI",
            "dimensions": 768,
            "config": '{"client_class": "OpenAIClient", "model_kwargs": {"model": "text-embedding-3-small", "dimensions": 768}}'
        },
        "Hugging Face Local": {
            "model": "all-mpnet-base-v2",
            "provider": "sentence-transformers",
            "dimensions": 768,
            "config": 'Requires sentence-transformers integration'
        }
    }
    
    for name, config in configs.items():
        print(f"\n{name}:")
        print(f"  Model: {config['model']}")
        print(f"  Provider: {config['provider']}")
        print(f"  Dimensions: {config['dimensions']}D")
        print(f"  Config: {config['config']}")

def main():
    """Main function"""
    print("🔍 Embedding Model Analysis for OpenProductWiki")
    print("=" * 70)
    
    models = get_embedding_models_info()
    
    # Display model comparison table
    print("\n📊 Model Comparison")
    print("=" * 70)
    
    for category, model_dict in models.items():
        print(f"\n{category}:")
        for model_name, info in model_dict.items():
            print(f"\n  {model_name}:")
            print(f"    Dimensions: {info['dimensions']}")
            print(f"    Provider: {info['provider']}")
            print(f"    Cost: {info['cost']}")
            print(f"    Privacy: {info['privacy']}")
            print(f"    Quality: {info['quality']}")
            print(f"    Notes: {info['notes']}")
    
    analyze_dimension_compatibility()
    recommend_best_model()
    migration_strategy()
    
    print(f"\n🎯 Final Recommendation:")
    print("Keep your current setup (nomic-embed-text/768D) - it's optimal!")
    print("If you need OpenAI in future, use text-embedding-3-small with dimensions=768")

if __name__ == "__main__":
    main()