'use client';

import React from 'react';

interface EmbeddingModel {
  id: string;
  name: string;
  provider: string;
  dimensions: number;
  cost: string;
  privacy: string;
  compatible: boolean;
  description: string;
}

interface DimensionWarningProps {
  currentModel: EmbeddingModel;
  selectedModel: EmbeddingModel;
  onConfirm: (action: 'compatible' | 'migrate' | 'cancel') => void;
  isVisible: boolean;
}

export default function DimensionCompatibilityWarning({
  currentModel,
  selectedModel,
  onConfirm,
  isVisible
}: DimensionWarningProps) {
  if (!isVisible) return null;

  const isDimensionMismatch = currentModel.dimensions !== selectedModel.dimensions;

  if (!isDimensionMismatch) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-[var(--background)] border border-[var(--border-color)] rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        {/* Header */}
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 bg-yellow-100 text-yellow-600 rounded-full flex items-center justify-center">
            ⚠️
          </div>
          <h3 className="text-lg font-semibold text-[var(--foreground)]">
            Dimension Mismatch Warning
          </h3>
        </div>

        {/* Content */}
        <div className="space-y-4">
          <p className="text-sm text-[var(--muted)]">
            The selected embedding model has different dimensions:
          </p>

          <div className="bg-[var(--background)]/50 rounded-md p-3 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-[var(--muted)]">Current:</span>
              <span className="font-medium text-[var(--foreground)]">
                {currentModel.name} ({currentModel.dimensions}D)
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-[var(--muted)]">Selected:</span>
              <span className="font-medium text-[var(--foreground)]">
                {selectedModel.name} ({selectedModel.dimensions}D)
              </span>
            </div>
          </div>

          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-700">
              This will cause FAISS retrieval errors. Choose an option:
            </p>
          </div>

          {/* Options */}
          <div className="space-y-2">
            <label className="flex items-start gap-2 cursor-pointer">
              <input 
                type="radio" 
                name="migration-option" 
                value="compatible"
                className="mt-1"
                defaultChecked
              />
              <div>
                <div className="text-sm font-medium text-[var(--foreground)]">
                  Use compatible model (Recommended)
                </div>
                <div className="text-xs text-[var(--muted)]">
                  Switch to text-embedding-3-small with 768D for seamless compatibility
                </div>
              </div>
            </label>

            <label className="flex items-start gap-2 cursor-pointer">
              <input 
                type="radio" 
                name="migration-option" 
                value="migrate"
                className="mt-1"
              />
              <div>
                <div className="text-sm font-medium text-[var(--foreground)]">
                  Clear embeddings and migrate
                </div>
                <div className="text-xs text-[var(--muted)]">
                  Regenerate all wikis with new embedding dimensions
                </div>
              </div>
            </label>

            <label className="flex items-start gap-2 cursor-pointer">
              <input 
                type="radio" 
                name="migration-option" 
                value="cancel"
                className="mt-1"
              />
              <div>
                <div className="text-sm font-medium text-[var(--foreground)]">
                  Cancel and keep current model
                </div>
                <div className="text-xs text-[var(--muted)]">
                  No changes will be made
                </div>
              </div>
            </label>
          </div>

          {/* Recommendation */}
          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex items-start gap-2">
              <span className="text-blue-500 text-sm">💡</span>
              <div className="text-sm text-blue-700">
                <strong>Recommended:</strong> Use text-embedding-3-small with 768D 
                for seamless compatibility with your current setup.
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 mt-6">
          <button
            onClick={() => onConfirm('cancel')}
            className="flex-1 px-4 py-2 text-sm border border-[var(--border-color)] rounded-md hover:bg-[var(--background)]/50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              const selectedOption = document.querySelector('input[name="migration-option"]:checked') as HTMLInputElement;
              onConfirm(selectedOption?.value as 'compatible' | 'migrate' | 'cancel' || 'cancel');
            }}
            className="flex-1 px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Apply Safe Option
          </button>
          <button
            onClick={() => onConfirm('migrate')}
            className="flex-1 px-4 py-2 text-sm bg-yellow-600 text-white rounded-md hover:bg-yellow-700 transition-colors"
          >
            Force Migration
          </button>
        </div>
      </div>
    </div>
  );
}