# Technical Context: OpenProductWiki

## Technology Stack

### Frontend (Next.js 15.3.1)
- **Framework**: Next.js with App Router
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x
- **UI Components**: Custom React components
- **State Management**: React hooks and context
- **Internationalization**: next-intl (currently English-only)
- **Theming**: next-themes for dark/light mode

### Backend (Python 3.13)
- **Framework**: FastAPI for REST API
- **WebSocket**: Native FastAPI WebSocket support
- **AI Integration**: Multiple provider clients
- **Vector Database**: FAISS for embeddings
- **RAG Framework**: AdalFlow for retrieval augmented generation
- **Process Management**: Uvicorn ASGI server

### Key Dependencies

#### Frontend Dependencies
```json
{
  "mermaid": "^11.4.1",           // Diagram rendering
  "next-intl": "^4.1.0",         // Internationalization
  "react-markdown": "^10.1.0",    // Markdown rendering
  "react-syntax-highlighter": "^15.6.1", // Code highlighting
  "svg-pan-zoom": "^3.6.2"       // Interactive diagrams
}
```

#### Backend Dependencies
```python
fastapi>=0.95.0                 # Web framework
adalflow>=0.1.0                 # RAG framework
google-generativeai>=0.3.0      # Google Gemini
openai>=1.76.2                  # OpenAI API
azure-identity>=1.12.0          # Azure authentication
ollama>=0.4.8                   # Local model support
faiss-cpu>=1.7.4                # Vector similarity search
langid>=1.1.6                   # Language detection
```

## Development Environment

### Local Development Setup
1. **Python Environment**: Python 3.13 with pip/poetry
2. **Node.js Environment**: Node.js 18+ with npm/yarn
3. **API Keys**: Environment variables in `.env` file
4. **Database**: FAISS vector store (local files)
5. **Cache**: Local filesystem for repository and wiki cache

### Environment Variables
```bash
# Required for OpenAI embeddings (always needed)
OPENAI_API_KEY=your_openai_api_key

# AI Provider Keys (use as needed)
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_VERSION=your_azure_version

# Optional Configuration
OLLAMA_HOST=http://localhost:11434
DEEPWIKI_CONFIG_DIR=/custom/config/path
PORT=8001
SERVER_BASE_URL=http://localhost:8001

# Authorization (optional)
DEEPWIKI_AUTH_MODE=false
DEEPWIKI_AUTH_CODE=your_secret_code

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=api/logs/application.log
```

## Deployment Options

### Docker Deployment
- **Single Container**: Combined frontend/backend
- **Multi-stage Build**: Optimized production image
- **Volume Mounts**: Persistent data storage
- **Environment**: Docker Compose orchestration

### Production Considerations
- **Reverse Proxy**: Nginx for static file serving
- **SSL/TLS**: HTTPS for secure token handling
- **Scaling**: Horizontal scaling for API servers
- **Monitoring**: Application logs and performance metrics

## Data Storage Architecture

### Repository Cache
- **Location**: `~/.adalflow/repos/`
- **Format**: Git clones of analyzed repositories
- **Cleanup**: Automatic cleanup for space management

### Vector Database
- **Location**: `~/.adalflow/databases/`
- **Technology**: FAISS CPU version
- **Format**: Binary index files with metadata
- **Indexing**: Per-repository embedding storage

### Wiki Cache
- **Location**: `~/.adalflow/wikicache/`
- **Format**: JSON files with generated content
- **Invalidation**: Based on repository changes

## AI Provider Integration

### Supported Providers
1. **Google Gemini**
   - Models: gemini-2.5-flash, gemini-2.5-pro
   - API: google-generativeai library
   - Features: High-quality text generation

2. **OpenAI**
   - Models: GPT-4o, GPT-4, GPT-3.5-turbo
   - API: openai library v1.76+
   - Features: Embeddings and text generation

3. **OpenRouter**
   - Models: Multiple providers through single API
   - API: OpenAI-compatible interface
   - Features: Model diversity and cost optimization

4. **Azure OpenAI**
   - Models: GPT-4o, GPT-4
   - API: Azure SDK with authentication
   - Features: Enterprise-grade deployment

5. **Ollama**
   - Models: Local open-source models
   - API: REST API to local server
   - Features: Privacy and customization

### Configuration System
- **Provider Selection**: Runtime configuration
- **Model Parameters**: Temperature, top_p, max_tokens
- **Fallback Logic**: Graceful degradation between providers
- **Custom Endpoints**: Support for enterprise deployments

## Security Considerations

### API Key Management
- Environment variable storage
- No hardcoded credentials
- Secure token transmission for private repos

### Private Repository Access
- Personal access token authentication
- Temporary token storage during processing
- Secure cleanup after generation

### CORS and Security Headers
- Configured CORS for cross-origin requests
- Security headers for production deployment
- Input validation and sanitization

## Performance Optimizations

### Caching Strategy
- **Repository Cache**: Avoid repeated cloning
- **Wiki Cache**: Store generated documentation
- **Embedding Cache**: Reuse vector computations

### Streaming Implementation
- **WebSocket**: Real-time progress updates
- **Chunked Processing**: Large repositories in segments
- **Background Tasks**: Non-blocking wiki generation

### Resource Management
- **Memory**: Efficient embedding storage
- **CPU**: Parallel processing where possible
- **Disk**: Automatic cache cleanup

## Development Workflow
1. **Frontend Development**: `npm run dev` (port 3000)
2. **Backend Development**: `python -m api.main` (port 8001)
3. **Full Stack**: Docker Compose for integrated testing
4. **Testing**: pytest for backend, manual testing for frontend
5. **Deployment**: Docker build and container deployment

This technical foundation supports the project's goals of flexibility, performance, and enterprise readiness while maintaining developer-friendly local development workflows.