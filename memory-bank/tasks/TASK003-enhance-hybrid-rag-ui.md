# [TASK003] - Enhance Hybrid RAG Configuration UI

**Status:** Pending  
**Added:** 2025-09-30  
**Updated:** 2025-09-30

## Original Request
User suggested using Ollama for embeddings while keeping external LLM providers for answering questions. Need to enhance the UI to make this hybrid approach more visible and user-friendly.

## Thought Process
The current system already supports this hybrid approach:
- **Embeddings**: Controlled by `api/config/embedder.json` (currently Ollama nomic-embed-text)
- **Generation**: Controlled by user selection in the UI (OpenAI, Google, etc.)

However, users might not understand that:
1. Embeddings happen locally with Ollama (private, free)
2. Generation uses their selected external provider (flexible, high-quality)
3. This gives them the best of both worlds

We should enhance the UI to:
1. Make the hybrid approach visible and understandable
2. Show embedding status (local vs external)
3. Highlight the benefits of this approach
4. Provide embedding model selection options

## Implementation Plan
- [ ] Add embedding provider status indicator to the UI
- [ ] Create information tooltip explaining the hybrid approach
- [ ] Add embedding model selection (advanced users)
- [ ] Update configuration modal with hybrid approach explanation
- [ ] Add cost/privacy indicators for different choices
- [ ] Create embedding model management utilities
- [ ] Update documentation with hybrid setup benefits
- [ ] Implement dimension-safe model switching (Ollama ↔ OpenAI)
- [ ] Add dimension validation UI warnings
- [ ] Create seamless migration presets for common models

## Progress Tracking

**Overall Status:** Pending - 0%

### Subtasks
| ID | Description | Status | Updated | Notes |
|----|-------------|--------|---------|-------|
| 3.1 | Design hybrid approach UI indicators | Not Started | - | Show local vs external processing |
| 3.2 | Add embedding status display | Not Started | - | Show current embedding model |
| 3.3 | Create information tooltips | Not Started | - | Explain benefits of hybrid approach |
| 3.4 | Implement embedding model selector | Not Started | - | Allow advanced users to choose |
| 3.5 | Add cost/privacy indicators | Not Started | - | Visual cues for user benefits |
| 3.6 | Update configuration modal | Not Started | - | Clearer separation of concerns |
| 3.7 | Create embedding management tools | Not Started | - | Install/update embedding models |
| 3.8 | Implement dimension-safe switching | Not Started | - | Prevent FAISS dimension mismatch errors |
| 3.9 | Add dimension validation warnings | Not Started | - | UI alerts for incompatible models |
| 3.10 | Create migration presets | Not Started | - | One-click Ollama ↔ OpenAI switching |

## Progress Log
### 2025-09-30
- Identified that current system already supports hybrid approach perfectly
- Embeddings: Ollama nomic-embed-text (768d, local, free, private)
- Generation: User-selected external providers (flexible, high-quality)
- Created comprehensive documentation (HYBRID_RAG_SETUP.md)
- Architecture is optimal, now need to enhance UX to make benefits visible
- **Updated**: Added dimension mismatch prevention requirements
- **Key insight**: Current 768D setup enables seamless OpenAI migration
- **Solution**: Use text-embedding-3-small with dimensions=768 for compatibility
- Created configuration templates for dimension-safe switching
- Built embedding model testing utilities to verify compatibility

## Technical Context
- **Current Embedding**: Ollama nomic-embed-text (768 dimensions)
- **Current Generation**: User-configurable (OpenAI, Google, OpenRouter, Azure)
- **Benefits**: Privacy, cost-effectiveness, flexibility, performance
- **UI Gap**: Users don't see the hybrid nature of the system
- **Opportunity**: Make the architecture benefits visible and configurable
- **Dimension Strategy**: Standardize on 768D for cross-provider compatibility
- **Migration Path**: OpenAI text-embedding-3-small with dimensions=768
- **Prevention**: Built-in dimension validation and user warnings
- **Compatibility**: Created config templates for seamless switching

## Design Considerations
- **Simplicity**: Don't overwhelm users with too many options
- **Education**: Help users understand the benefits
- **Flexibility**: Allow advanced users to customize
- **Visibility**: Show what's happening behind the scenes
- **Trust**: Build confidence in the privacy/cost benefits
- **Safety**: Prevent dimension mismatch errors during model switching
- **Compatibility**: Ensure seamless migration between providers
- **Validation**: Real-time dimension checking and warnings
- **Presets**: One-click configurations for common scenarios
- **Recovery**: Clear migration paths when dimension mismatches occur

## Dimension Mismatch Prevention Strategy

### Current Safe Configuration (768D Standard)
- **Ollama**: nomic-embed-text (768D) ✅
- **OpenAI Compatible**: text-embedding-3-small with dimensions=768 ✅
- **Hugging Face**: all-mpnet-base-v2 (768D) ✅

### UI Requirements for Dimension Safety
1. **Real-time Dimension Display**: Show current embedding dimensions
2. **Compatibility Warnings**: Alert when switching to incompatible models
3. **Migration Presets**: Pre-configured safe switches
4. **Validation Checks**: Prevent dimension mismatches before they occur
5. **Recovery Options**: Clear guidance when mismatches are detected

### Seamless Migration Presets
```json
// Preset 1: Ollama to OpenAI (Compatible)
{
  "name": "Ollama → OpenAI (Safe)",
  "from": {"provider": "ollama", "model": "nomic-embed-text", "dimensions": 768},
  "to": {"provider": "openai", "model": "text-embedding-3-small", "dimensions": 768},
  "migration_required": false,
  "benefits": ["API reliability", "Enterprise support"],
  "costs": ["$0.02/1M tokens", "Privacy trade-off"]
}

// Preset 2: OpenAI to Ollama (Compatible) 
{
  "name": "OpenAI → Ollama (Safe)",
  "from": {"provider": "openai", "model": "text-embedding-3-small", "dimensions": 768},
  "to": {"provider": "ollama", "model": "nomic-embed-text", "dimensions": 768},
  "migration_required": false,
  "benefits": ["100% privacy", "Zero cost", "No API limits"],
  "costs": ["Local compute", "Manual model management"]
}
```

### Implementation Priority
1. **High**: Dimension validation and warnings
2. **High**: Compatible migration presets
3. **Medium**: Advanced embedding model selection
4. **Low**: Custom dimension configuration (expert users only)

## UI Design Reference
Created comprehensive UI mockup: `UI_MOCKUP_HYBRID_RAG.md`
- Configuration modal with dimension compatibility indicators
- Real-time validation warnings for model switches
- Migration presets for common scenarios (Ollama ↔ OpenAI)
- Benefits display to educate users about hybrid approach
- Status indicators showing current embedding/generation setup