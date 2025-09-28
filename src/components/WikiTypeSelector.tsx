'use client';

import React from 'react';
import { FaBookOpen, FaList } from 'react-icons/fa';

interface WikiTypeSelectorProps {
  isComprehensiveView: boolean;
  setIsComprehensiveView: (value: boolean) => void;
}

const WikiTypeSelector: React.FC<WikiTypeSelectorProps> = ({
  isComprehensiveView,
  setIsComprehensiveView,
}) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-[var(--foreground)] mb-2">
        Wiki Type
      </label>
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          type="button"
          onClick={() => setIsComprehensiveView(true)}
          className={`flex items-center justify-between p-3 rounded-md border transition-colors ${
            isComprehensiveView
              ? 'bg-[var(--accent-primary)]/10 border-[var(--accent-primary)]/30 text-[var(--accent-primary)]'
              : 'bg-[var(--background)]/50 border-[var(--border-color)] text-[var(--foreground)] hover:bg-[var(--background)]'
          }`}
        >
          <div className="flex items-center">
            <FaBookOpen className="mr-2" />
            <div className="text-left">
              <div className="font-medium">Comprehensive</div>
              <div className="text-xs opacity-80">
                Detailed wiki with structured sections and more pages
              </div>
            </div>
          </div>
          {isComprehensiveView && (
            <div className="ml-2 h-4 w-4 rounded-full bg-[var(--accent-primary)]/20 flex items-center justify-center">
              <div className="h-2 w-2 rounded-full bg-[var(--accent-primary)]"></div>
            </div>
          )}
        </button>
        
        <button
          type="button"
          onClick={() => setIsComprehensiveView(false)}
          className={`flex items-center justify-between p-3 rounded-md border transition-colors ${
            !isComprehensiveView
              ? 'bg-[var(--accent-primary)]/10 border-[var(--accent-primary)]/30 text-[var(--accent-primary)]'
              : 'bg-[var(--background)]/50 border-[var(--border-color)] text-[var(--foreground)] hover:bg-[var(--background)]'
          }`}
        >
          <div className="flex items-center">
            <FaList className="mr-2" />
            <div className="text-left">
              <div className="font-medium">Concise</div>
              <div className="text-xs opacity-80">
                Simplified wiki with fewer pages and essential information
              </div>
            </div>
          </div>
          {!isComprehensiveView && (
            <div className="ml-2 h-4 w-4 rounded-full bg-[var(--accent-primary)]/20 flex items-center justify-center">
              <div className="h-2 w-2 rounded-full bg-[var(--accent-primary)]"></div>
            </div>
          )}
        </button>
      </div>
    </div>
  );
};

export default WikiTypeSelector;
