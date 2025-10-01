'use client';

import React, { useState } from 'react';

interface EmbeddingStatusProps {
  className?: string;
  isHybridMode?: boolean;
  currentEmbedding?: string;
  currentGeneration?: string;
  onToggleHybrid?: () => void;
}

export default function EmbeddingStatusIndicator({ 
  className = '',
  isHybridMode = false,
  currentEmbedding = 'Default',
  currentGeneration = 'Default',
  onToggleHybrid
}: EmbeddingStatusProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  const handleToggle = () => {
    if (onToggleHybrid) {
      onToggleHybrid();
    }
  };

  return (
    <div className={`relative ${className}`}>
      {/* Main Status Indicator */}
      <div 
        className="flex items-center gap-2 px-3 py-1.5 bg-[var(--background)]/50 rounded-md border border-[var(--border-color)] cursor-pointer hover:bg-[var(--background)]/70 transition-colors"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onClick={handleToggle}
      >
        <div className="flex items-center gap-1 text-sm text-[var(--muted)]">
          {isHybridMode ? (
            <>
              <span className="text-green-500">🔒</span>
              <span>Local Embeddings</span>
              <span className="text-gray-400">+</span>
              <span className="text-blue-500">🌐</span>
              <span>External Generation</span>
            </>
          ) : (
            <>
              <span className="text-blue-500">🌐</span>
              <span>Standard Configuration</span>
            </>
          )}
        </div>
        <svg 
          className="w-4 h-4 text-[var(--muted)]" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>

      {/* Tooltip */}
      {showTooltip && (
        <div className="absolute bottom-full left-0 mb-2 p-3 bg-[var(--background)] border border-[var(--border-color)] rounded-lg shadow-lg z-50 min-w-[300px]">
          <div className="text-sm font-medium text-[var(--foreground)] mb-2">
            {isHybridMode ? '🎯 Hybrid RAG Configuration' : '📊 Standard Configuration'}
          </div>
          
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-[var(--muted)]">📄 Document Processing:</span>
              <span className={`font-medium ${isHybridMode ? 'text-green-600' : 'text-blue-600'}`}>
                {isHybridMode ? `🔒 ${currentEmbedding} (Local)` : `🌐 ${currentEmbedding}`}
              </span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-[var(--muted)]">🧠 Answer Generation:</span>
              <span className="text-blue-600 font-medium">🌐 {currentGeneration}</span>
            </div>
            
            {isHybridMode && (
              <div className="border-t border-[var(--border-color)] pt-2 mt-2">
                <div className="text-[var(--muted)] text-xs">Hybrid Benefits:</div>
                <ul className="text-xs text-[var(--foreground)] mt-1 space-y-1">
                  <li>🔒 Private document processing</li>
                  <li>💰 Cost-effective (only pay for answers)</li>
                  <li>⚡ Fast local embeddings</li>
                  <li>🎯 High-quality external generation</li>
                </ul>
              </div>
            )}
            
            {onToggleHybrid && (
              <div className="border-t border-[var(--border-color)] pt-2 mt-2">
                <button
                  onClick={handleToggle}
                  className="text-xs text-blue-600 hover:text-blue-700 underline"
                >
                  {isHybridMode ? 'Switch to Standard' : 'Enable Hybrid Mode'}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}