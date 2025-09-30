# Active Context: OpenProductWiki

## Current Focus
**Language Simplification & RAG System Issues**: Currently working on a branch `remove-another-languages` that simplifies internationalization to English-only, while addressing FAISS retriever errors affecting the RAG system.

## Recent Changes (September 30, 2025)
- **Language Cleanup**: Removed Korean, Portuguese (Brazil), Russian, Vietnamese, Traditional Chinese, and Simplified Chinese language support
- **Internationalization**: Simplified to English-only configuration in `src/i18n.ts`
- **Git Status**: Clean working tree on `remove-another-languages` branch
- **System Issues**: FAISS retriever assertion errors detected in logs, affecting RAG functionality

## Current State Assessment
The project is a mature, feature-complete implementation with:
- ✅ **Multi-Provider AI Support**: Google Gemini, OpenAI, OpenRouter, Azure OpenAI, Ollama
- ✅ **Private Repository Access**: Token-based authentication for GitHub, GitLab, BitBucket
- ⚠️ **RAG Implementation**: Vector database with FAISS experiencing retriever errors
- ✅ **Visual Diagrams**: Mermaid.js integration for architecture visualization
- ⚠️ **Internationalization**: Reduced to English-only (previously multi-language)
- ✅ **Docker Deployment**: Complete containerization with docker-compose
- ✅ **Streaming Interface**: Real-time progress updates via WebSocket

## Active Decisions Made
1. **Language Simplification**: Decided to reduce internationalization complexity by supporting English only
2. **Memory Bank Maintenance**: Updated memory bank documentation to reflect current project state
3. **Issue Identification**: Detected FAISS retriever problems requiring investigation

## Next Steps Priority
1. **RAG System Fix**: Address FAISS retriever assertion errors affecting document retrieval
2. **Language Branch Merge**: Complete the language simplification and merge to main
3. **Performance Analysis**: Investigate memory and embedding dimension issues in FAISS
4. **Testing Coverage**: Validate RAG functionality after fixes
5. **Error Monitoring**: Improve error handling and logging for retriever failures

## Key Questions to Explore
- **RAG System**: What's causing the FAISS retriever assertion errors and how to fix them?
- **Language Strategy**: Should the project maintain English-only or restore multilingual support?
- **Error Recovery**: How can the system better handle and recover from RAG failures?
- **Performance Impact**: Are the FAISS errors affecting overall system performance?
- **User Impact**: How do these technical issues affect the user experience?

## Technology Context
- **Frontend**: Modern React with TypeScript, Tailwind CSS, and streaming UI updates
- **Backend**: FastAPI with WebSocket support for real-time communication
- **AI Integration**: Sophisticated provider abstraction supporting 5 different AI services
- **Data Pipeline**: Repository processing with caching and vector storage (experiencing issues)
- **Deployment**: Production-ready Docker setup with volume persistence
- **Language Support**: Currently English-only (simplified from multi-language)

## Immediate Priorities
1. **RAG System Debug**: Investigate and fix FAISS retriever assertion failures
2. **Branch Management**: Complete language simplification branch and merge
3. **Error Handling**: Improve RAG error recovery and user feedback
4. **System Health**: Ensure all core functionality works after changes
5. **Documentation Update**: Update technical docs to reflect current architecture

This represents a solid foundation for a production AI documentation platform with room for continued enhancement and optimization based on user needs and technical improvements.