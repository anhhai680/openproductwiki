# Project Brief: OpenProductWiki

## Vision
OpenProductWiki (DeepWiki-Open) is an AI-powered platform that automatically generates comprehensive, interactive wikis for any GitHub, GitLab, or BitBucket repository. The goal is to transform code repositories into beautiful, navigable documentation with minimal effort from developers.

## Core Value Proposition
- **Instant Documentation**: Convert any repository into a structured wiki in seconds
- **AI-Powered Analysis**: Understand code structure, relationships, and architecture automatically
- **Visual Diagrams**: Generate Mermaid diagrams to visualize system architecture and data flows
- **Interactive Q&A**: Chat with repositories using RAG-powered AI for accurate, contextual answers
- **Multi-Platform Support**: Works with GitHub, GitLab, and BitBucket repositories (including private ones)

## Primary Goals
1. **Democratize Documentation**: Make high-quality documentation accessible to any developer or team
2. **Reduce Documentation Overhead**: Eliminate manual documentation maintenance burden
3. **Enhance Code Understanding**: Provide visual and interactive ways to explore codebases
4. **Support Multiple Workflows**: Accommodate different development platforms and AI model preferences

## Target Users
- **Individual Developers**: Need quick documentation for personal or open-source projects
- **Development Teams**: Want to onboard new team members faster with auto-generated documentation
- **Technical Writers**: Require comprehensive understanding of codebases they're documenting
- **Enterprise Users**: Need private repository support with their own AI model endpoints
- **Service Providers**: Want to offer documentation services with multiple model options

## Key Differentiators
- **Provider-Agnostic AI**: Support for Google Gemini, OpenAI, OpenRouter, Azure OpenAI, and local Ollama models
- **Private Repository Access**: Secure token-based authentication for private repositories
- **Visual Architecture**: Automatic generation of system diagrams and component relationships
- **Deep Research**: Multi-turn AI research process for complex technical investigations
- **Streaming Interface**: Real-time generation with progress feedback
- **Enterprise Ready**: Custom endpoints, authorization modes, and flexible configuration

## Success Metrics
- Time to generate comprehensive documentation (target: under 60 seconds for medium repositories)
- User satisfaction with generated content quality
- Adoption rate across different repository types and sizes
- Successful private repository integrations
- Multi-language and multi-platform usage

## Technical Constraints
- Must handle repositories of varying sizes efficiently
- Requires robust error handling for different repository structures
- Need to maintain performance with multiple AI model providers
- Must ensure security for private repository access
- Should scale to handle concurrent wiki generation requests

This project represents the intersection of AI, developer tooling, and documentation automation, aiming to solve the persistent problem of outdated or missing technical documentation.