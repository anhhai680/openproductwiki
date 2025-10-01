#!/usr/bin/env python3
"""
Embedding Model Management Utility

This script provides tools for managing embedding models in the hybrid RAG system.
It allows users to install, update, and switch between different embedding models
while ensuring dimension compatibility.
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add the API directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

class EmbeddingModelManager:
    """Manages embedding models for the hybrid RAG system."""
    
    def __init__(self):
        self.api_dir = Path(__file__).parent.parent / "api"
        self.config_dir = self.api_dir / "config"
        self.embedder_config_path = self.config_dir / "embedder.json"
        
    def get_current_config(self) -> Dict:
        """Get the current embedding configuration."""
        try:
            with open(self.embedder_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.embedder_config_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            return {}
    
    def update_config(self, new_config: Dict) -> bool:
        """Update the embedding configuration."""
        try:
            # Backup current config
            backup_path = self.embedder_config_path.with_suffix('.json.bak')
            if self.embedder_config_path.exists():
                with open(self.embedder_config_path, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
                logger.info(f"Backed up current config to {backup_path}")
            
            # Write new config
            with open(self.embedder_config_path, 'w') as f:
                json.dump(new_config, f, indent=2)
            
            logger.info("Successfully updated embedding configuration")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available embedding models."""
        return [
            {
                "id": "ollama_nomic-embed-text",
                "name": "Nomic Embed Text",
                "provider": "ollama",
                "dimensions": 768,
                "cost": "free",
                "privacy": "local",
                "compatible": True,
                "description": "High-quality embeddings running locally with Ollama",
                "install_cmd": "ollama pull nomic-embed-text"
            },
            {
                "id": "openai_text-embedding-3-small",
                "name": "Text Embedding 3 Small",
                "provider": "openai",
                "dimensions": 768,
                "cost": "low",
                "privacy": "external",
                "compatible": True,
                "description": "OpenAI's efficient embedding model (768D for compatibility)",
                "install_cmd": None  # API-based, no installation needed
            },
            {
                "id": "openai_text-embedding-3-large",
                "name": "Text Embedding 3 Large", 
                "provider": "openai",
                "dimensions": 3072,
                "cost": "medium",
                "privacy": "external",
                "compatible": False,
                "description": "OpenAI's highest quality embedding model (requires migration)",
                "install_cmd": None
            },
            {
                "id": "huggingface_all-mpnet-base-v2",
                "name": "All-MiniLM-L6-v2",
                "provider": "huggingface",
                "dimensions": 768,
                "cost": "free",
                "privacy": "local",
                "compatible": True,
                "description": "Popular sentence transformer model (768D compatible)",
                "install_cmd": "pip install sentence-transformers"
            }
        ]
    
    def check_model_availability(self, model_id: str) -> bool:
        """Check if a model is available/installed."""
        models = self.get_available_models()
        model = next((m for m in models if m["id"] == model_id), None)
        
        if not model:
            return False
            
        if model["provider"] == "ollama":
            # Check if Ollama model is installed
            try:
                result = subprocess.run(
                    ["ollama", "list"], 
                    capture_output=True, 
                    text=True, 
                    check=False
                )
                model_name = model_id.split("_", 1)[1]  # Extract model name from ID
                return model_name in result.stdout
            except FileNotFoundError:
                logger.warning("Ollama not found. Please install Ollama first.")
                return False
                
        elif model["provider"] == "openai":
            # Check if OpenAI API key is available
            return bool(os.environ.get("OPENAI_API_KEY"))
            
        elif model["provider"] == "huggingface":
            # Check if sentence-transformers is installed
            try:
                import sentence_transformers
                return True
            except ImportError:
                return False
                
        return False
    
    def install_model(self, model_id: str) -> bool:
        """Install a specific embedding model."""
        models = self.get_available_models()
        model = next((m for m in models if m["id"] == model_id), None)
        
        if not model:
            logger.error(f"Model {model_id} not found in available models")
            return False
            
        if not model["install_cmd"]:
            logger.info(f"Model {model_id} is API-based and doesn't require installation")
            return True
            
        logger.info(f"Installing {model['name']} using: {model['install_cmd']}")
        
        try:
            result = subprocess.run(
                model["install_cmd"].split(),
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Successfully installed {model['name']}")
            logger.debug(f"Installation output: {result.stdout}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install {model['name']}: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error(f"Command not found for installing {model['name']}")
            return False
    
    def switch_model(self, model_id: str, force: bool = False) -> bool:
        """Switch to a different embedding model."""
        models = self.get_available_models()
        target_model = next((m for m in models if m["id"] == model_id), None)
        
        if not target_model:
            logger.error(f"Model {model_id} not found")
            return False
            
        # Check current configuration
        current_config = self.get_current_config()
        current_model = current_config.get("embedder", {}).get("model_kwargs", {}).get("model", "unknown")
        
        logger.info(f"Switching from {current_model} to {target_model['name']}")
        
        # Check dimension compatibility
        if not target_model["compatible"] and not force:
            logger.warning(f"Model {target_model['name']} has different dimensions and may cause FAISS errors")
            logger.warning("Use --force to proceed anyway, or choose a compatible model")
            logger.info("Compatible models (768D): ollama_nomic-embed-text, openai_text-embedding-3-small")
            return False
            
        # Check if model is available
        if not self.check_model_availability(model_id):
            logger.info(f"Model {target_model['name']} is not available. Attempting to install...")
            if not self.install_model(model_id):
                logger.error(f"Failed to install {target_model['name']}")
                return False
                
        # Update configuration
        new_config = current_config.copy()
        
        # Update embedder configuration based on provider
        provider = target_model["provider"]
        model_name = model_id.split("_", 1)[1]  # Extract model name from ID
        
        if provider == "ollama":
            new_config["embedder"] = {
                "client_class": "OllamaClient",
                "model_kwargs": {
                    "model": model_name
                }
            }
        elif provider == "openai":
            new_config["embedder"] = {
                "client_class": "OpenAIClient", 
                "model_kwargs": {
                    "model": model_name,
                    "dimensions": target_model["dimensions"]
                }
            }
        elif provider == "huggingface":
            new_config["embedder"] = {
                "client_class": "HuggingFaceClient",
                "model_kwargs": {
                    "model": model_name
                }
            }
            
        # Update configuration
        if self.update_config(new_config):
            logger.info(f"Successfully switched to {target_model['name']}")
            
            # Warn about embedding cache
            if not target_model["compatible"]:
                logger.warning("IMPORTANT: Clear embedding cache to prevent dimension mismatch errors:")
                logger.warning("python clear_embeddings.py")
                
            return True
        else:
            logger.error("Failed to update configuration")
            return False
    
    def list_models(self) -> None:
        """List all available embedding models."""
        models = self.get_available_models()
        current_config = self.get_current_config()
        current_model = current_config.get("embedder", {}).get("model_kwargs", {}).get("model", "unknown")
        
        print("\n📚 Available Embedding Models:")
        print("=" * 60)
        
        for model in models:
            status_indicators = []
            
            # Current model indicator
            model_name = model["id"].split("_", 1)[1]
            if model_name == current_model:
                status_indicators.append("🔹 CURRENT")
                
            # Availability indicator
            if self.check_model_availability(model["id"]):
                status_indicators.append("✅ INSTALLED")
            else:
                status_indicators.append("❌ NOT INSTALLED")
                
            # Compatibility indicator
            if model["compatible"]:
                status_indicators.append("🔄 COMPATIBLE")
            else:
                status_indicators.append("⚠️  MIGRATION REQUIRED")
                
            status_str = " | ".join(status_indicators)
            
            print(f"\n🎯 {model['name']}")
            print(f"   ID: {model['id']}")
            print(f"   Provider: {model['provider']}")
            print(f"   Dimensions: {model['dimensions']}")
            print(f"   Cost: {model['cost']} | Privacy: {model['privacy']}")
            print(f"   Status: {status_str}")
            print(f"   Description: {model['description']}")
            
        print("\n" + "=" * 60)
        print("💡 Use 'python embedding_manager.py switch <model_id>' to switch models")
        print("💡 Compatible models share 768 dimensions for seamless switching")

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Embedding Model Management Utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    subparsers.add_parser("list", help="List all available embedding models")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a specific embedding model")
    install_parser.add_argument("model_id", help="Model ID to install")
    
    # Switch command
    switch_parser = subparsers.add_parser("switch", help="Switch to a different embedding model")
    switch_parser.add_argument("model_id", help="Model ID to switch to")
    switch_parser.add_argument("--force", action="store_true", help="Force switch even if dimensions are incompatible")
    
    # Status command
    subparsers.add_parser("status", help="Show current embedding configuration")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check if a model is available")
    check_parser.add_argument("model_id", help="Model ID to check")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    manager = EmbeddingModelManager()
    
    if args.command == "list":
        manager.list_models()
        
    elif args.command == "install":
        success = manager.install_model(args.model_id)
        sys.exit(0 if success else 1)
        
    elif args.command == "switch":
        success = manager.switch_model(args.model_id, force=args.force)
        sys.exit(0 if success else 1)
        
    elif args.command == "status":
        config = manager.get_current_config()
        embedder_config = config.get("embedder", {})
        model = embedder_config.get("model_kwargs", {}).get("model", "unknown")
        client = embedder_config.get("client_class", "unknown")
        
        print(f"\n🔧 Current Embedding Configuration:")
        print(f"   Model: {model}")
        print(f"   Client: {client}")
        print(f"   Config file: {manager.embedder_config_path}")
        
    elif args.command == "check":
        available = manager.check_model_availability(args.model_id)
        status = "✅ Available" if available else "❌ Not available"
        print(f"Model {args.model_id}: {status}")
        sys.exit(0 if available else 1)

if __name__ == "__main__":
    main()