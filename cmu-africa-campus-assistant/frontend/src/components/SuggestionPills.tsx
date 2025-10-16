
import React from 'react';
import { Suggestion } from '../types';

interface SuggestionPillsProps {
  suggestions: Suggestion[];
  onSuggestionClick: (prompt: string) => void;
}

const SuggestionPills: React.FC<SuggestionPillsProps> = ({
  suggestions,
  onSuggestionClick,
}) => {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="mb-4 animate-fade-in">
      <p className="text-xs text-gray-600 mb-2 font-medium">💡 Quick suggestions:</p>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion.id}
            onClick={() => onSuggestionClick(suggestion.prompt)}
            className="px-4 py-2 bg-white border-2 border-primary-300 text-primary-700 rounded-full text-sm font-medium hover:bg-primary-50 hover:border-primary-400 transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
          >
            {suggestion.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SuggestionPills;
