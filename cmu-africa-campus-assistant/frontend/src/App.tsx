
import React, { useState, useEffect, useRef } from 'react';
import { Message, Suggestion } from './types';
import { chatAPI } from './services/api';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import SuggestionPills from './components/SuggestionPills';
import ChatInput from './components/ChatInput';
import WelcomeScreen from './components/WelcomeScreen';
import './App.css';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentSuggestions, setCurrentSuggestions] = useState<Suggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Call API
      const response = await chatAPI.sendMessage({
        message: messageText,
        session_id: 'session_' + Date.now(),
      });

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        sources: response.sources,
        suggestions: response.suggestions,
        followUp: response.follow_up,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setCurrentSuggestions(response.suggestions || []);
    } catch (err: any) {
      console.error('Error sending message:', err);
      setError(
        err.response?.data?.detail ||
          'Failed to get response. Please check if the backend is running.'
      );

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content:
          '❌ Sorry, I encountered an error. Please make sure the backend server is running on port 8000. You can check the connection by visiting http://localhost:8000/api/health',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (prompt: string) => {
    handleSendMessage(prompt);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />

      {/* Main Chat Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-5xl mx-auto">
          {messages.length === 0 ? (
            <WelcomeScreen onQuickQuestion={handleSendMessage} />
          ) : (
            <>
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex justify-start mb-4">
                  <div className="bg-white rounded-2xl px-6 py-4 shadow-sm border border-gray-200 animate-pulse">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.4s' }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>

      {/* Input Area with Suggestions Above */}
      <div className="border-t border-gray-200 bg-white shadow-lg">
        <div className="max-w-5xl mx-auto px-4 py-4">
          {/* Suggestions appear above input */}
          {currentSuggestions.length > 0 && !isLoading && (
            <SuggestionPills
              suggestions={currentSuggestions}
              onSuggestionClick={handleSuggestionClick}
            />
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Chat Input */}
          <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />

          {/* Footer */}
          <p className="text-xs text-gray-500 text-center mt-3">
            Powered by RAG + OpenAI • CMU-Africa Campus Assistant v1.0
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
