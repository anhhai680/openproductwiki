# DeepWiki-Open Copilot Instructions

## Repository Overview

**DeepWiki-Open** is an AI-powered documentation generator that automatically creates interactive wikis for GitHub, GitLab, and Bitbucket repositories. It's a full-stack application with a Next.js frontend and FastAPI backend that uses RAG (Retrieval Augmented Generation) to analyze code structure and generate comprehensive documentation with visual diagrams.

### Key Technologies
- **Frontend**: Next.js 15.3.1, React 19, TypeScript, Tailwind CSS
- **Backend**: Python 3.11-3.13, FastAPI, uvicorn
- **AI/ML**: Multiple LLM providers (OpenAI, Google Gemini, OpenRouter, Azure, Ollama), AdalFlow, FAISS for vector storage
- **Docker**: Multi-stage builds with optimized production deployment
- **Testing**: pytest for Python, ESLint for TypeScript

### Repository Structure
```
deepwiki/
├── api/                     # Python FastAPI backend
│   ├── main.py             # API entry point
│   ├── api.py              # FastAPI routes
│   ├── rag.py              # RAG implementation
│   ├── data_pipeline.py    # Repository processing
│   ├── config/             # JSON configuration files
│   │   ├── generator.json  # LLM model configurations
│   │   ├── embedder.json   # Embedding model settings
│   │   └── repo.json       # Repository filtering rules
│   └── requirements.txt    # Python dependencies
├── src/                    # Next.js frontend
│   ├── app/               # Next.js app router pages
│   └── components/        # React components
├── test/                  # Python tests
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Multi-stage container build
└── package.json          # Node.js dependencies
```

## Environment Setup & Dependencies

### Required Environment Variables
```bash
# Core API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key      # Required for embeddings by default
GOOGLE_API_KEY=your_google_api_key      # Required for Gemini models
OPENROUTER_API_KEY=your_openrouter_key  # Optional for OpenRouter models
AZURE_OPENAI_API_KEY=your_azure_key     # Optional for Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_VERSION=your_azure_version

# Optional Configuration
OLLAMA_HOST=http://localhost:11434       # For local Ollama models
PORT=8001                               # API server port
SERVER_BASE_URL=http://localhost:8001   # API base URL
LOG_LEVEL=INFO                          # Logging verbosity
DEEPWIKI_AUTH_MODE=false               # Authorization mode
DEEPWIKI_AUTH_CODE=your_secret_code    # Secret for auth mode
```

### Python Requirements
- **Python Version**: 3.11-3.13 (3.13 recommended)
- **Key Dependencies**: FastAPI, AdalFlow, FAISS, Google GenAI, OpenAI, Ollama
- Install with: `pip install -r api/requirements.txt`

### Node.js Requirements  
- **Node.js**: 20+ (verified with Node 20)
- **Package Manager**: npm or yarn (yarn@1.22.22 specified)
- Install with: `npm install` or `yarn install`

## Build & Development Commands

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server (with Turbopack)
npm run dev                # Runs on http://localhost:3000

# Build for production
npm run build             # Creates optimized build

# Start production server
npm start                 # Serves built application

# Lint code
npm run lint             # ESLint with Next.js rules
```

### Backend Development
```bash
# Install Python dependencies
pip install -r api/requirements.txt

# Start API server (development)
python -m api.main       # Runs on http://localhost:8001

# Alternative with uv (if available)
uv run -m api.main

# Run with custom port
PORT=8002 python -m api.main
```

### Testing
```bash
# Run Python tests
python -m pytest test/ -v

# Run specific test file
python -m pytest test/test_extract_repo_name.py -v

# Run tests with coverage
python -m pytest test/ --cov=api --cov-report=html
```

### Docker Commands
```bash
# Build and run with Docker Compose
docker-compose up

# Build image locally
docker build -t deepwiki-open .

# Run with custom environment
docker run -p 8001:8001 -p 3000:3000 \
  --env-file .env \
  -v ~/.adalflow:/root/.adalflow \
  deepwiki-open

# Health check
curl -f http://localhost:8001/health
```

## Common Build Issues & Solutions

### Frontend Build Errors
1. **ESLint Errors**: The build may fail due to unused variables or missing dependencies
   - Fix unused variables in `src/components/ConfigurationModal.tsx`
   - Add missing dependencies to useEffect and useCallback hooks
   - Run `npm run lint` to see all issues

2. **Memory Issues**: Next.js builds can be memory-intensive
   - The Dockerfile sets `NODE_OPTIONS="--max-old-space-size=4096"`
   - For local builds, increase memory: `NODE_OPTIONS="--max-old-space-size=8192" npm run build`

3. **TypeScript Errors**: Strict mode is enabled
   - Fix type issues in `src/app/[owner]/[repo]/page.tsx`
   - Ensure all props are properly typed

### Backend Setup Issues
1. **Missing API Keys**: The system logs warnings but continues without keys
   - At minimum, `OPENAI_API_KEY` is required for embeddings
   - Other keys are only needed for specific model providers

2. **FAISS Dimension Mismatch**: Common error when switching embedding models
   - Error: `AssertionError: assert d == self.d`
   - Solution: Run `python clear_embeddings.py` to clear cached embeddings
   - See `FAISS_ERROR_FIX.md` for detailed troubleshooting

3. **Port Conflicts**: Default ports 3000 and 8001 may be in use
   - Change API port: `PORT=8002 python -m api.main`
   - Update `SERVER_BASE_URL` accordingly in frontend

### Docker Issues
1. **Build Context**: Ensure you're in the project root
2. **Memory Limits**: Docker Compose sets 6GB limit, may need adjustment for large repos
3. **Volume Mounts**: `~/.adalflow` directory stores repositories and embeddings

## Configuration Management

### Model Configuration (`api/config/generator.json`)
- Defines available LLM providers and models
- Each provider has default models and custom model support
- Temperature and other parameters are configurable per model

### Embedding Configuration (`api/config/embedder.json`)
- Controls text processing and vector storage
- **Critical**: Changing embedding models requires clearing cache
- Backup configurations available for different setups

### Repository Filters (`api/config/repo.json`)
- Defines file patterns to exclude during processing
- Controls repository size limits

## Testing Strategy

### Python Tests
- Located in `test/` directory
- Uses pytest with asyncio support
- Configuration in `pytest.ini`
- Focus on core functionality like repository name extraction

### Frontend Testing
- ESLint for code quality
- TypeScript for type safety
- No automated UI tests currently configured

## Deployment Considerations

### Production Build
- Always use `npm run build` for frontend
- Docker builds use multi-stage optimization
- Standalone Next.js output for better performance

### Environment Security
- Never commit API keys to git
- Use `.env` files locally
- Mount environment variables in production containers

### Data Persistence
- Repository data stored in `~/.adalflow/repos/`
- Embeddings cached in `~/.adalflow/databases/`
- Wiki content cached in `~/.adalflow/wikicache/`
- Mount these directories to persist data across restarts

## Development Workflow

1. **Setup**: Create `.env` file with required API keys
2. **Backend**: Start API server with `python -m api.main`
3. **Frontend**: Start dev server with `npm run dev`
4. **Testing**: Run tests before committing changes
5. **Building**: Use `npm run build` to verify production build
6. **Docker**: Test full stack with `docker-compose up`

## Important Notes

- **Always clear embeddings** when changing embedding models or configurations
- **API keys are provider-specific** - only add keys for providers you intend to use
- **Memory requirements** are high for large repositories - ensure adequate RAM
- **Build times** can be significant due to AI model dependencies
- **Trust these instructions** and only search for additional information if something is incomplete or incorrect

For detailed setup instructions, refer to the comprehensive README.md file in the repository root.