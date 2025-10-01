'use client';

import React, { useState } from 'react';

interface LLMModel {
  id: string;
  name: string;
  provider: string;
  costTier: 'free' | 'low' | 'medium' | 'high';
  capabilities: string[];
  description: string;
}

interface EmbeddingModel {
  id: string;
  name: string;
  provider: string;
  dimensions: number;
  cost: string;
  privacy: string;
  description: string;
}

interface HybridConfig {
  embedding: EmbeddingModel;
  generation: LLMModel;
  enabled: boolean;
}

interface HybridRAGControlsProps {
  config: HybridConfig;
  embeddingModels: EmbeddingModel[];
  generationModels: LLMModel[];
  onConfigChange: (config: HybridConfig) => void;
  onDimensionWarning: (current: EmbeddingModel, selected: EmbeddingModel) => void;
}

export default function HybridRAGControls({
  config,
  embeddingModels,
  generationModels,
  onConfigChange,
  onDimensionWarning
}: HybridRAGControlsProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleEmbeddingChange = (modelId: string) => {
    const selectedModel = embeddingModels.find(m => m.id === modelId);
    if (!selectedModel) return;

    // Check for dimension mismatch
    if (config.embedding && selectedModel.dimensions !== config.embedding.dimensions) {
      onDimensionWarning(config.embedding, selectedModel);
      return;
    }

    onConfigChange({
      ...config,
      embedding: selectedModel
    });
  };

  const handleGenerationChange = (modelId: string) => {
    const selectedModel = generationModels.find(m => m.id === modelId);
    if (!selectedModel) return;

    onConfigChange({
      ...config,
      generation: selectedModel
    });
  };

  const getCostBadgeColor = (costTier: string) => {
    switch (costTier) {
      case 'free': return 'bg-green-100 text-green-700';
      case 'low': return 'bg-blue-100 text-blue-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'high': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="border border-[var(--border-color)] rounded-lg p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold text-[var(--foreground)]">
            Hybrid RAG Configuration
          </h3>
          <div className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
            Optimized
          </div>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
        >
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>

      {/* Benefits Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
        <div className="flex items-start gap-2">
          <span className="text-blue-500 text-sm">💡</span>
          <div className="text-sm text-blue-700">
            <strong>Hybrid Benefits:</strong> Free local embeddings + powerful external generation = 
            optimal cost-performance balance with enhanced privacy.
          </div>
        </div>
      </div>

      {/* Configuration Details (Expandable) */}
      {isExpanded && (
        <div className="space-y-6 pt-2">
          {/* Embedding Configuration */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <h4 className="font-medium text-[var(--foreground)]">Embedding Model</h4>
              <span className="text-xs text-[var(--muted)]">(Text Understanding)</span>
            </div>
            
            <select
              value={config.embedding?.id || ''}
              onChange={(e) => handleEmbeddingChange(e.target.value)}
              className="w-full p-2 border border-[var(--border-color)] rounded-md bg-[var(--background)] text-[var(--foreground)]"
            >
              {embeddingModels.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name} ({model.dimensions}D) - {model.provider}
                </option>
              ))}
            </select>

            {config.embedding && (
              <div className="bg-[var(--background)]/50 rounded-md p-3 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--muted)]">Dimensions:</span>
                  <span className="font-medium text-[var(--foreground)]">
                    {config.embedding.dimensions}D
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--muted)]">Cost:</span>
                  <span className={`px-2 py-1 rounded-full text-xs ${getCostBadgeColor(config.embedding.cost)}`}>
                    {config.embedding.cost}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--muted)]">Privacy:</span>
                  <span className="font-medium text-[var(--foreground)]">
                    {config.embedding.privacy}
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Generation Configuration */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <h4 className="font-medium text-[var(--foreground)]">Generation Model</h4>
              <span className="text-xs text-[var(--muted)]">(Answer Generation)</span>
            </div>
            
            <select
              value={config.generation?.id || ''}
              onChange={(e) => handleGenerationChange(e.target.value)}
              className="w-full p-2 border border-[var(--border-color)] rounded-md bg-[var(--background)] text-[var(--foreground)]"
            >
              {generationModels.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name} - {model.provider}
                </option>
              ))}
            </select>

            {config.generation && (
              <div className="bg-[var(--background)]/50 rounded-md p-3 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-[var(--muted)]">Cost Tier:</span>
                  <span className={`px-2 py-1 rounded-full text-xs ${getCostBadgeColor(config.generation.costTier)}`}>
                    {config.generation.costTier}
                  </span>
                </div>
                <div className="text-sm">
                  <span className="text-[var(--muted)]">Capabilities:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {config.generation.capabilities.map((cap, index) => (
                      <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Compatibility Check */}
          <div className="bg-green-50 border border-green-200 rounded-md p-3">
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span className="text-sm text-green-700 font-medium">
                Configuration Compatible
              </span>
            </div>
            <p className="text-xs text-green-600 mt-1">
              Embedding dimensions: {config.embedding?.dimensions}D | 
              Generation model: {config.generation?.name}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}