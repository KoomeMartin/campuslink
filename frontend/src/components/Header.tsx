
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-cmu-red to-red-700 text-white py-6 px-6 shadow-lg">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-4">
          <div className="bg-white rounded-full p-3 shadow-md">
            <span className="text-3xl">🎓</span>
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold">
              CMU-Africa Campus Assistant
            </h1>
            <p className="text-red-100 text-sm md:text-base">
              Your AI-powered guide to campus life
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
