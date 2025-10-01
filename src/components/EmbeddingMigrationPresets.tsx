'use client';

import React from 'react';

interface EmbeddingPreset {
  id: string;
  name: string;
  description: string;
  embedding: {
    model: string;
    provider: string;
    dimensions: number;
    cost: string;
  };
  generation: {
    model: string;
    provider: string;
    cost: string;
  };
  benefits: string[];
  recommended: boolean;
}

interface EmbeddingMigrationPresetsProps {
  presets: EmbeddingPreset[];
  currentConfig: {
    embeddingModel: string;
    generationModel: string;
  };
  onSelectPreset: (preset: EmbeddingPreset) => void;
  onCustomConfig: () => void;
}

export default function EmbeddingMigrationPresets({
  presets,
  currentConfig,
  onSelectPreset,
  onCustomConfig
}: EmbeddingMigrationPresetsProps) {
  const getCostBadgeColor = (cost: string) => {
    switch (cost.toLowerCase()) {
      case 'free': return 'bg-green-100 text-green-700';
      case 'low': return 'bg-blue-100 text-blue-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'high': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-[var(--foreground)]">
          Migration Presets
        </h3>
        <button
          onClick={onCustomConfig}
          className="text-sm text-blue-600 hover:text-blue-700 underline"
        >
          Custom Configuration
        </button>
      </div>

      <p className="text-sm text-[var(--muted)]">
        Choose a pre-configured setup to ensure dimension compatibility and optimal performance.
      </p>

      <div className="grid gap-4">
        {presets.map((preset) => {
          const isCurrentConfig = 
            preset.embedding.model === currentConfig.embeddingModel &&
            preset.generation.model === currentConfig.generationModel;

          return (
            <div
              key={preset.id}
              className={`
                border rounded-lg p-4 cursor-pointer transition-all
                ${preset.recommended 
                  ? 'border-blue-300 bg-blue-50' 
                  : 'border-[var(--border-color)] bg-[var(--background)]'
                }
                ${isCurrentConfig 
                  ? 'ring-2 ring-green-500 bg-green-50' 
                  : 'hover:border-blue-400'
                }
              `}
              onClick={() => onSelectPreset(preset)}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-[var(--foreground)]">
                    {preset.name}
                  </h4>
                  {preset.recommended && (
                    <div className="px-2 py-1 bg-blue-600 text-white text-xs rounded-full">
                      Recommended
                    </div>
                  )}
                  {isCurrentConfig && (
                    <div className="px-2 py-1 bg-green-600 text-white text-xs rounded-full">
                      Current
                    </div>
                  )}
                </div>
                <button className="text-blue-600 hover:text-blue-700 text-sm">
                  Select →
                </button>
              </div>

              <p className="text-sm text-[var(--muted)] mb-4">
                {preset.description}
              </p>

              {/* Configuration Details */}
              <div className="grid md:grid-cols-2 gap-4 mb-4">
                {/* Embedding */}
                <div className="space-y-2">
                  <div className="text-xs font-medium text-[var(--muted)] uppercase">
                    Embedding
                  </div>
                  <div className="bg-[var(--background)]/50 rounded-md p-2">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium">
                        {preset.embedding.model}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs ${getCostBadgeColor(preset.embedding.cost)}`}>
                        {preset.embedding.cost}
                      </span>
                    </div>
                    <div className="text-xs text-[var(--muted)]">
                      {preset.embedding.provider} • {preset.embedding.dimensions}D
                    </div>
                  </div>
                </div>

                {/* Generation */}
                <div className="space-y-2">
                  <div className="text-xs font-medium text-[var(--muted)] uppercase">
                    Generation
                  </div>
                  <div className="bg-[var(--background)]/50 rounded-md p-2">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium">
                        {preset.generation.model}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs ${getCostBadgeColor(preset.generation.cost)}`}>
                        {preset.generation.cost}
                      </span>
                    </div>
                    <div className="text-xs text-[var(--muted)]">
                      {preset.generation.provider}
                    </div>
                  </div>
                </div>
              </div>

              {/* Benefits */}
              <div className="space-y-2">
                <div className="text-xs font-medium text-[var(--muted)] uppercase">
                  Benefits
                </div>
                <div className="flex flex-wrap gap-1">
                  {preset.benefits.map((benefit, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                    >
                      {benefit}
                    </span>
                  ))}
                </div>
              </div>

              {/* Compatibility Indicator */}
              <div className="mt-3 flex items-center gap-2">
                <span className="text-green-500 text-sm">✓</span>
                <span className="text-xs text-green-600">
                  Dimension compatible • No migration required
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Custom Configuration Option */}
      <div className="border border-dashed border-[var(--border-color)] rounded-lg p-4 text-center">
        <h4 className="font-medium text-[var(--foreground)] mb-2">
          Need a Custom Configuration?
        </h4>
        <p className="text-sm text-[var(--muted)] mb-3">
          Mix and match models for your specific requirements
        </p>
        <button
          onClick={onCustomConfig}
          className="px-4 py-2 border border-[var(--border-color)] rounded-md text-sm hover:bg-[var(--background)]/50 transition-colors"
        >
          Configure Manually
        </button>
      </div>
    </div>
  );
}