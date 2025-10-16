#!/bin/bash

echo "Setting up CMU-Africa Information Assistant..."
echo "=============================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q streamlit openai pinecone-client python-dotenv pandas tiktoken

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "Make sure to configure your API keys in the .env file or through the web interface."
