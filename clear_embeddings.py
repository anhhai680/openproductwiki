#!/usr/bin/env python3
"""
Clear FAISS Embeddings Utility

This script clears existing FAISS embeddings when there's a dimension mismatch
due to changing embedding models (e.g., from OpenAI to Ollama embeddings).

Usage:
    python clear_embeddings.py [repo_name]
    
If no repo_name is provided, it will clear all embedding databases.
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_adalflow_databases_path():
    """Get the path to adalflow databases directory"""
    home_path = Path.home()
    return home_path / ".adalflow" / "databases"

def clear_all_embeddings():
    """Clear all embedding databases"""
    databases_path = get_adalflow_databases_path()
    
    if not databases_path.exists():
        logger.info("No databases directory found - nothing to clear")
        return
    
    logger.info(f"Clearing all embedding databases in: {databases_path}")
    
    # Remove all .pkl files (database files)
    pkl_files = list(databases_path.glob("*.pkl"))
    for pkl_file in pkl_files:
        try:
            pkl_file.unlink()
            logger.info(f"Removed: {pkl_file.name}")
        except Exception as e:
            logger.error(f"Error removing {pkl_file.name}: {e}")
    
    # Remove any FAISS index files
    faiss_files = list(databases_path.glob("*.faiss")) + list(databases_path.glob("*.index"))
    for faiss_file in faiss_files:
        try:
            faiss_file.unlink()
            logger.info(f"Removed: {faiss_file.name}")
        except Exception as e:
            logger.error(f"Error removing {faiss_file.name}: {e}")
    
    logger.info(f"Cleared {len(pkl_files) + len(faiss_files)} database files")

def clear_repo_embeddings(repo_name):
    """Clear embeddings for a specific repository"""
    databases_path = get_adalflow_databases_path()
    
    if not databases_path.exists():
        logger.info("No databases directory found - nothing to clear")
        return
    
    logger.info(f"Clearing embeddings for repository: {repo_name}")
    
    # Look for files matching the repo name pattern
    pattern = f"*{repo_name}*"
    matching_files = list(databases_path.glob(f"{pattern}.pkl")) + list(databases_path.glob(f"{pattern}.faiss")) + list(databases_path.glob(f"{pattern}.index"))
    
    if not matching_files:
        logger.warning(f"No database files found matching pattern: {pattern}")
        # List available files for reference
        all_files = list(databases_path.glob("*"))
        if all_files:
            logger.info("Available database files:")
            for f in all_files:
                logger.info(f"  - {f.name}")
        return
    
    for db_file in matching_files:
        try:
            db_file.unlink()
            logger.info(f"Removed: {db_file.name}")
        except Exception as e:
            logger.error(f"Error removing {db_file.name}: {e}")
    
    logger.info(f"Cleared {len(matching_files)} database files for {repo_name}")

def main():
    """Main function"""
    print("🧹 FAISS Embeddings Cleaner")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        repo_name = sys.argv[1]
        print(f"Clearing embeddings for repository: {repo_name}")
        clear_repo_embeddings(repo_name)
    else:
        print("Clearing ALL embedding databases...")
        response = input("Are you sure you want to clear all embedding databases? (y/N): ")
        if response.lower() in ['y', 'yes']:
            clear_all_embeddings()
        else:
            print("Operation cancelled")
            return
    
    print("\n✅ Done! Next time you generate a wiki, new embeddings will be created with the current model.")
    print("💡 This will fix FAISS dimension mismatch errors.")

if __name__ == "__main__":
    main()