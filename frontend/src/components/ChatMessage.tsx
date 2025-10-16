
import React, { useState } from 'react';
import { Message } from '../types';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [showSources, setShowSources] = useState(false);
  const isUser = message.type === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-slide-up`}>
      <div className={`max-w-3xl ${isUser ? 'ml-12' : 'mr-12'} w-full`}>
        {/* Message Bubble */}
        <div
          className={`rounded-2xl px-6 py-4 ${
            isUser
              ? 'bg-cmu-red text-white'
              : 'bg-white border border-gray-200 text-gray-800'
          } shadow-sm`}
        >
          {isUser ? (
            <p className="text-sm md:text-base">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Sources Section (for assistant messages) */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3">
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-xs text-gray-600 hover:text-gray-900 flex items-center gap-1 transition-colors"
            >
              <span>📚</span>
              <span className="font-medium">
                {showSources ? 'Hide' : 'Show'} Sources ({message.sources.length})
              </span>
              <span className={`transition-transform ${showSources ? 'rotate-180' : ''}`}>
                ▼
              </span>
            </button>

            {showSources && (
              <div className="mt-2 space-y-2 animate-fade-in">
                {message.sources.map((source, index) => (
                  <div
                    key={source.id}
                    className="bg-gray-50 border border-gray-200 rounded-lg p-3"
                  >
                    <div className="flex items-start gap-2">
                      <span className="text-xs font-bold text-gray-500">
                        [{index + 1}]
                      </span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="text-sm font-semibold text-gray-900">
                            {source.title}
                          </h4>
                          <span className="text-xs px-2 py-0.5 bg-primary-100 text-primary-700 rounded-full">
                            {source.category}
                          </span>
                        </div>
                        <p className="text-xs text-gray-600">{source.snippet}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <p className="text-xs text-gray-500 mt-2 px-2">
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
};

export default ChatMessage;
