
import React from 'react';

interface WelcomeScreenProps {
  onQuickQuestion: (question: string) => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onQuickQuestion }) => {
  const quickQuestions = [
    {
      icon: '🚌',
      question: 'What are the shuttle bus timings?',
      color: 'bg-blue-50 border-blue-200 hover:bg-blue-100',
    },
    {
      icon: '🎓',
      question: 'What programs does CMU-Africa offer?',
      color: 'bg-purple-50 border-purple-200 hover:bg-purple-100',
    },
    {
      icon: '📚',
      question: 'What are the library hours?',
      color: 'bg-green-50 border-green-200 hover:bg-green-100',
    },
    {
      icon: '🏠',
      question: 'Tell me about housing options',
      color: 'bg-orange-50 border-orange-200 hover:bg-orange-100',
    },
  ];

  return (
    <div className="flex-1 flex items-center justify-center p-6">
      <div className="max-w-3xl w-full text-center animate-fade-in">
        <div className="mb-8">
          <div className="inline-block bg-gradient-to-br from-primary-400 to-primary-600 rounded-full p-6 mb-4 shadow-lg">
            <span className="text-6xl">🤖</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-3">
            Welcome to CMU-Africa!
          </h2>
          <p className="text-lg text-gray-600">
            I'm here to help you navigate campus life. Ask me anything!
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {quickQuestions.map((item, index) => (
            <button
              key={index}
              onClick={() => onQuickQuestion(item.question)}
              className={`${item.color} border-2 rounded-xl p-5 text-left transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-1`}
            >
              <div className="flex items-center gap-3">
                <span className="text-3xl">{item.icon}</span>
                <span className="text-sm md:text-base font-medium text-gray-800">
                  {item.question}
                </span>
              </div>
            </button>
          ))}
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>💡 Tip: I can help with academics, transportation, housing, events, and more!</p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
