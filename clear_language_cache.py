#!/usr/bin/env python3
"""
Clear Language Cache Script
============================

This script helps clear cached embeddings and wikis that were created with 
the old multi-language configuration to ensure the system only works with 
English language content.

Usage:
    python clear_language_cache.py [--embeddings] [--wikis] [--all]
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any

def load_current_config() -> Dict[str, Any]:
    """Load the current language configuration."""
    config_path = Path(__file__).parent / "api" / "config" / "lang.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        return {}

def get_adalflow_path() -> Path:
    """Get the path to the .adalflow directory."""
    return Path.home() / ".adalflow"

def clear_embeddings_cache():
    """Clear the FAISS embeddings cache."""
    adalflow_path = get_adalflow_path()
    databases_path = adalflow_path / "databases"
    
    if databases_path.exists():
        print(f"🗑️  Clearing embeddings cache: {databases_path}")
        try:
            shutil.rmtree(databases_path)
            print("✅ Embeddings cache cleared successfully")
            return True
        except Exception as e:
            print(f"❌ Error clearing embeddings cache: {e}")
            return False
    else:
        print("ℹ️  No embeddings cache found")
        return True

def clear_wiki_cache():
    """Clear cached wiki files."""
    adalflow_path = get_adalflow_path()
    wikicache_path = adalflow_path / "wikicache"
    
    if wikicache_path.exists():
        print(f"🗑️  Clearing wiki cache: {wikicache_path}")
        try:
            # Clear all cached wiki files
            for cache_file in wikicache_path.glob("*.json"):
                cache_file.unlink()
            print("✅ Wiki cache cleared successfully")
            return True
        except Exception as e:
            print(f"❌ Error clearing wiki cache: {e}")
            return False
    else:
        print("ℹ️  No wiki cache found")
        return True

def clear_repositories():
    """Clear cached repository data."""
    adalflow_path = get_adalflow_path()
    repos_path = adalflow_path / "repos"
    
    if repos_path.exists():
        print(f"🗑️  Clearing repository cache: {repos_path}")
        try:
            shutil.rmtree(repos_path)
            print("✅ Repository cache cleared successfully")
            return True
        except Exception as e:
            print(f"❌ Error clearing repository cache: {e}")
            return False
    else:
        print("ℹ️  No repository cache found")
        return True

def main():
    """Main function to clear language-related caches."""
    import sys
    
    print("🧹 Language Cache Cleaner for OpenProductWiki")
    print("=" * 50)
    
    # Check current language configuration
    config = load_current_config()
    if config:
        supported_langs = config.get("supported_languages", {})
        print(f"📝 Current supported languages: {list(supported_langs.keys())}")
        print(f"📝 Default language: {config.get('default', 'not set')}")
        
        if len(supported_langs) == 1 and "en" in supported_langs:
            print("✅ Configuration is correctly set to English-only")
        else:
            print("⚠️  Configuration still supports multiple languages")
            print("   Please update api/config/lang.json to support only English")
            return
    
    # Parse command line arguments
    args = sys.argv[1:]
    clear_all = "--all" in args or len(args) == 0
    clear_embeddings = "--embeddings" in args or clear_all
    clear_wikis = "--wikis" in args or clear_all
    clear_repos = "--repositories" in args or clear_all
    
    print("\n🎯 Clearing caches...")
    
    success = True
    
    if clear_embeddings:
        success &= clear_embeddings_cache()
    
    if clear_wikis:
        success &= clear_wiki_cache()
    
    if clear_repos:
        success &= clear_repositories()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Language cache cleanup completed successfully!")
        print("📋 What was done:")
        print("   • Cleared embeddings cache (FAISS databases)")
        print("   • Cleared wiki cache files") 
        print("   • Cleared repository cache")
        print("\n💡 Next steps:")
        print("   1. Restart your OpenProductWiki application")
        print("   2. Generate new wikis - they will now be English-only")
        print("   3. New embeddings will use only English language processing")
    else:
        print("❌ Some errors occurred during cleanup")
        print("   Please check the error messages above")

if __name__ == "__main__":
    main()