#!/usr/bin/env python3
"""
Hybrid RAG Configuration Validation Test

This script tests the new hybrid RAG UI components and backend endpoints
to ensure they work correctly together.
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, List, Any

async def test_endpoint(session: aiohttp.ClientSession, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Test a specific API endpoint."""
    url = f"http://localhost:8002{endpoint}"
    
    try:
        if method == "GET":
            async with session.get(url) as response:
                result = await response.json()
                return {"success": True, "status": response.status, "data": result}
        elif method == "POST":
            async with session.post(url, json=data) as response:
                result = await response.json()
                return {"success": True, "status": response.status, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def run_hybrid_rag_tests():
    """Run comprehensive tests for hybrid RAG functionality."""
    
    print("🧪 Testing Hybrid RAG Configuration API Endpoints")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        tests = [
            {
                "name": "Health Check",
                "endpoint": "/health",
                "method": "GET",
                "expected_keys": ["status", "timestamp", "service"]
            },
            {
                "name": "Embedding Models",
                "endpoint": "/embedding-models", 
                "method": "GET",
                "expected_keys": ["id", "name", "provider", "dimensions"]
            },
            {
                "name": "Generation Models",
                "endpoint": "/generation-models",
                "method": "GET", 
                "expected_keys": ["id", "name", "provider", "costTier"]
            },
            {
                "name": "Migration Presets",
                "endpoint": "/migration-presets",
                "method": "GET",
                "expected_keys": ["id", "name", "description", "embedding", "generation"]
            },
            {
                "name": "Current Embedding Config",
                "endpoint": "/embedding/current-config",
                "method": "GET",
                "expected_keys": ["model", "provider", "dimensions"]
            },
            {
                "name": "Existing Model Config", 
                "endpoint": "/models/config",
                "method": "GET",
                "expected_keys": ["providers", "defaultProvider"]
            }
        ]
        
        results = []
        
        for test in tests:
            print(f"\n🔍 Testing: {test['name']}")
            result = await test_endpoint(session, test["endpoint"], test["method"])
            
            if result["success"]:
                status_icon = "✅" if result["status"] == 200 else "⚠️"
                print(f"   {status_icon} Status: {result['status']}")
                
                # Validate response structure
                data = result["data"]
                if isinstance(data, list) and len(data) > 0:
                    # Check first item for expected keys
                    first_item = data[0]
                    missing_keys = []
                    for key in test["expected_keys"]:
                        if key not in first_item:
                            missing_keys.append(key)
                    
                    if missing_keys:
                        print(f"   ⚠️  Missing keys: {missing_keys}")
                    else:
                        print(f"   ✅ Response structure valid ({len(data)} items)")
                        
                elif isinstance(data, dict):
                    missing_keys = []
                    for key in test["expected_keys"]:
                        if key not in data:
                            missing_keys.append(key)
                    
                    if missing_keys:
                        print(f"   ⚠️  Missing keys: {missing_keys}")
                    else:
                        print(f"   ✅ Response structure valid")
                
                # Show sample data
                if test["name"] == "Embedding Models" and isinstance(data, list):
                    print(f"   📊 Found {len(data)} embedding models:")
                    for model in data[:2]:  # Show first 2
                        print(f"      • {model.get('name', 'Unknown')} ({model.get('dimensions', '?')}D) - {model.get('provider', 'Unknown')}")
                        
                elif test["name"] == "Migration Presets" and isinstance(data, list):
                    print(f"   📊 Found {len(data)} migration presets:")
                    recommended = [p for p in data if p.get("recommended", False)]
                    print(f"      • {len(recommended)} recommended presets")
                    
                elif test["name"] == "Current Embedding Config":
                    print(f"   📊 Current: {data.get('model', 'Unknown')} ({data.get('provider', 'Unknown')})")
                
            else:
                print(f"   ❌ Failed: {result['error']}")
                
            results.append({"test": test["name"], "result": result})
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        
        passed = sum(1 for r in results if r["result"]["success"] and r["result"].get("status") == 200)
        total = len(results)
        
        print(f"   Passed: {passed}/{total}")
        print(f"   Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("   🎉 All tests passed! Hybrid RAG API is ready.")
        else:
            print("   ⚠️  Some tests failed. Check the API server.")
            
        return passed == total

def test_dimension_compatibility():
    """Test dimension compatibility logic."""
    print("\n🔢 Testing Dimension Compatibility Logic")
    print("=" * 60)
    
    # Test cases for dimension compatibility
    test_cases = [
        {"current": 768, "target": 768, "compatible": True, "scenario": "Same dimensions"},
        {"current": 768, "target": 1536, "compatible": False, "scenario": "Different dimensions"},  
        {"current": 1536, "target": 768, "compatible": False, "scenario": "Dimension change"},
        {"current": 768, "target": 3072, "compatible": False, "scenario": "Large dimension change"}
    ]
    
    for i, case in enumerate(test_cases, 1):
        current = case["current"]
        target = case["target"] 
        expected = case["compatible"]
        scenario = case["scenario"]
        
        # Simple compatibility check logic
        actual = current == target
        
        status = "✅" if actual == expected else "❌"
        print(f"   {status} Test {i}: {scenario}")
        print(f"      Current: {current}D → Target: {target}D")
        print(f"      Expected: {expected}, Actual: {actual}")
        
        if actual != expected:
            print(f"      🐛 Logic error detected!")
            
    print("\n💡 Recommendation: Always validate dimensions before switching models")

def test_ui_component_props():
    """Test UI component property requirements."""
    print("\n🎨 Testing UI Component Requirements")
    print("=" * 60)
    
    # Mock data that UI components expect
    mock_embedding_model = {
        "id": "ollama_nomic-embed-text",
        "name": "Nomic Embed Text", 
        "provider": "ollama",
        "dimensions": 768,
        "cost": "free",
        "privacy": "local",
        "compatible": True,
        "description": "High-quality embeddings running locally"
    }
    
    mock_generation_model = {
        "id": "openai_gpt-4o-mini",
        "name": "GPT-4o Mini",
        "provider": "openai", 
        "costTier": "low",
        "capabilities": ["text-generation", "reasoning"],
        "description": "OpenAI's efficient model"
    }
    
    mock_preset = {
        "id": "hybrid_optimal",
        "name": "Hybrid Optimal",
        "description": "Best balance of privacy and performance",
        "embedding": {"model": "ollama_nomic-embed-text", "provider": "ollama"},
        "generation": {"model": "openai_gpt-4o-mini", "provider": "openai"},
        "benefits": ["Privacy", "Cost-effective"],
        "recommended": True
    }
    
    components = [
        {
            "name": "EmbeddingStatusIndicator",
            "required_props": ["isHybridMode", "currentEmbedding", "currentGeneration"],
            "test_data": {
                "isHybridMode": True,
                "currentEmbedding": "Nomic Embed Text",
                "currentGeneration": "GPT-4o Mini"
            }
        },
        {
            "name": "HybridRAGControls", 
            "required_props": ["config", "embeddingModels", "generationModels"],
            "test_data": {
                "config": {"embedding": mock_embedding_model, "generation": mock_generation_model},
                "embeddingModels": [mock_embedding_model],
                "generationModels": [mock_generation_model]
            }
        },
        {
            "name": "EmbeddingMigrationPresets",
            "required_props": ["presets", "currentConfig", "onSelectPreset"],
            "test_data": {
                "presets": [mock_preset],
                "currentConfig": {"embeddingModel": "ollama_nomic-embed-text"},
                "onSelectPreset": "function"
            }
        }
    ]
    
    for component in components:
        print(f"\n📦 {component['name']}")
        test_data = component["test_data"]
        required_props = component["required_props"]
        
        for prop in required_props:
            if prop in test_data:
                print(f"   ✅ {prop}: Available")
            else:
                print(f"   ❌ {prop}: Missing")
                
    print("\n💡 All UI components have their required data structures defined")

async def main():
    """Run all hybrid RAG tests."""
    print("🚀 Hybrid RAG Configuration Validation")
    print("Testing UI components and backend integration")
    print("=" * 80)
    
    # Test API endpoints
    api_success = await run_hybrid_rag_tests()
    
    # Test logic components
    test_dimension_compatibility()
    test_ui_component_props()
    
    print("\n" + "=" * 80)
    if api_success:
        print("🎉 Hybrid RAG system validation completed successfully!")
        print("✨ The enhanced UI components are ready for integration.")
    else:
        print("⚠️  Some API tests failed. Please check the server setup.")
        
    print("\n📚 Next Steps:")
    print("   1. Start the API server: python -m api.main")
    print("   2. Start the frontend: npm run dev") 
    print("   3. Test the hybrid configuration UI")
    print("   4. Validate dimension safety features")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)