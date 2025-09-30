# FAISS Retriever Error Fix

## Problem
You may encounter this error when using the Q&A feature:

```
AssertionError: assert d == self.d
```

This error occurs in the FAISS retriever when there's a dimension mismatch between stored embeddings and the current embedding model.

## Root Cause
This happens when:
1. **Embedding Model Changed**: The system was previously configured to use a different embedding model (e.g., OpenAI's text-embedding-3-small with 256 dimensions) but is now using a different model (e.g., Ollama's nomic-embed-text with 768 dimensions).
2. **Existing Database**: There are cached embeddings from the previous model in the database.
3. **Dimension Mismatch**: When querying, the new model produces embeddings with different dimensions than what's stored in FAISS.

## Quick Fix

### Option 1: Clear All Embeddings (Recommended)
```bash
python3 clear_embeddings.py
```

This will clear all cached embeddings, forcing the system to regenerate them with the current model.

### Option 2: Clear Specific Repository
```bash
python3 clear_embeddings.py your_repo_name
```

This clears embeddings only for a specific repository.

## What Happens Next
1. **Cached embeddings are removed**
2. **Next wiki generation will create fresh embeddings** using the current model configuration
3. **Q&A feature will work correctly** with consistent embedding dimensions

## Prevention
- When changing embedding models in `api/config/embedder.json`, clear the embedding cache
- The system now includes automatic detection of dimension mismatches
- Future versions will handle this automatically

## Technical Details
- **OpenAI text-embedding-3-small**: 256 dimensions (when configured with dimensions parameter)
- **Ollama nomic-embed-text**: 768 dimensions
- **FAISS**: Requires all vectors to have the same dimensions
- **Error Location**: `faiss_retriever.py` line 294 in `retrieve_string_queries`

## Configuration Check
Current configuration can be found in:
```
api/config/embedder.json
```

Backup configurations:
- `embedder.json.bak` - Previous OpenAI configuration
- `embedder.ollama.json.bak` - Ollama configuration