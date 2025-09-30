# Enhanced Hybrid RAG UI Mockup

## Current Configuration Display

```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Model Configuration                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📄 Document Processing (Local & Private)                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 🔒 Embeddings: Ollama nomic-embed-text (768D)          │ │
│ │ ✅ Status: Active  📍 Location: Local  💰 Cost: Free   │ │
│ │ 🔄 Change Model                                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ 🧠 Answer Generation (External API)                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Provider: [OpenAI ▼]  Model: [gpt-4o ▼]               │ │
│ │ 📍 Location: External API  💰 Cost: $0.015/1K tokens  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ℹ️  Hybrid Benefits: Private docs + Best AI models         │
└─────────────────────────────────────────────────────────────┘
```

## Enhanced Configuration Modal

```
┌───────────────────────────────────────────────────────────────┐
│ ⚙️  Advanced Configuration                                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│ 📄 EMBEDDING CONFIGURATION                                   │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ Current: 🔒 Ollama nomic-embed-text (768D)               │ │
│ │                                                           │ │
│ │ Quick Switch Options:                                     │ │
│ │ ○ Ollama nomic-embed-text (768D) ✅ COMPATIBLE          │ │
│ │ ○ OpenAI text-embedding-3-small (768D) ✅ COMPATIBLE    │ │
│ │ ○ Ollama all-minilm (384D) ⚠️  REQUIRES MIGRATION      │ │
│ │ ○ OpenAI ada-002 (1536D) ⚠️  REQUIRES MIGRATION        │ │
│ │                                                           │ │
│ │ [📋 Advanced Settings] [📊 Compare Models]               │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                                               │
│ 🧠 GENERATION CONFIGURATION                                  │
│ │ Provider: [OpenAI ▼]  Model: [gpt-4o ▼]                  │ │
│                                                               │
│ 💡 HYBRID BENEFITS                                           │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ 🔒 Privacy: Documents stay local during embedding        │ │
│ │ 💰 Cost: Only pay for final answers, not document prep   │ │
│ │ 🚀 Speed: No API limits on document processing           │ │
│ │ 🎯 Quality: Best models for answering questions          │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                                               │
│ [Cancel] [Apply Changes]                                      │
└───────────────────────────────────────────────────────────────┘
```

## Dimension Mismatch Warning

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️  Dimension Mismatch Warning                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ The selected embedding model has different dimensions:      │
│                                                             │
│ Current: nomic-embed-text (768D)                           │
│ Selected: text-embedding-ada-002 (1536D)                  │
│                                                             │
│ This will cause FAISS retrieval errors. Choose an option:  │
│                                                             │
│ ○ Use compatible model: text-embedding-3-small (768D)     │
│ ○ Clear embeddings and migrate (regenerate all wikis)     │
│ ○ Cancel and keep current model                            │
│                                                             │
│ 💡 Recommended: Use text-embedding-3-small with 768D       │
│    for seamless compatibility                              │
│                                                             │
│ [Cancel] [Apply Safe Option] [Force Migration]             │
└─────────────────────────────────────────────────────────────┘
```

## Migration Success Message

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ Model Successfully Updated                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Embedding model changed:                                    │
│ From: Ollama nomic-embed-text (768D)                       │
│ To:   OpenAI text-embedding-3-small (768D)                │
│                                                             │
│ ✅ No dimension mismatch - existing wikis remain valid     │
│ ✅ Q&A feature will continue working                       │
│ ✅ No data migration required                              │
│                                                             │
│ Changes take effect for new wiki generations.              │
│                                                             │
│ [OK]                                                        │
└─────────────────────────────────────────────────────────────┘
```

## Embedding Model Comparison

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Embedding Model Comparison                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Model                    │ Dims │ Cost/1M │ Privacy │ Compat │
│ ──────────────────────── │ ──── │ ─────── │ ─────── │ ────── │
│ nomic-embed-text (Ollama)│ 768D │  Free   │  100%   │   ✅   │
│ text-emb-3-small (OpenAI)│ 768D │  $20    │  API    │   ✅   │
│ all-mpnet-base-v2 (HF)   │ 768D │  Free   │  100%   │   ✅   │
│ ──────────────────────── │ ──── │ ─────── │ ─────── │ ────── │
│ all-minilm (Ollama)      │ 384D │  Free   │  100%   │   ⚠️   │
│ ada-002 (OpenAI)         │1536D │  $100   │  API    │   ⚠️   │
│ e5-large-v2 (HF)         │1024D │  Free   │  100%   │   ⚠️   │
│                                                             │
│ ✅ = Compatible (same 768D)                                │
│ ⚠️  = Requires migration (different dimensions)            │
│                                                             │
│ [Select Model] [Close]                                      │
└─────────────────────────────────────────────────────────────┘
```

## Status Indicator in Main UI

```
🔧 Configuration: 🔒 Local Embeddings + 🌐 OpenAI Generation
```

This UI design ensures users:
1. **Understand the hybrid approach** (local + external)
2. **See dimension compatibility** before switching
3. **Get warnings** about potential issues
4. **Have safe migration paths** with pre-configured options
5. **Understand the benefits** of their current setup