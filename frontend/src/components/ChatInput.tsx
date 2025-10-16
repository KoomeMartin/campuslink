
import React, { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex gap-3 items-end">
      <div className="flex-1 relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about CMU-Africa..."
          disabled={disabled}
          rows={1}
          className="w-full px-5 py-4 pr-12 border-2 border-gray-300 rounded-2xl focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all resize-none disabled:bg-gray-100 disabled:cursor-not-allowed text-sm md:text-base"
          style={{ minHeight: '56px', maxHeight: '120px' }}
        />
      </div>
      <button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        className="px-6 py-4 bg-cmu-red text-white rounded-2xl font-semibold hover:bg-red-700 transition-all disabled:bg-gray-300 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:transform-none"
      >
        <span className="text-xl">➤</span>
      </button>
    </div>
  );
};

export default ChatInput;
