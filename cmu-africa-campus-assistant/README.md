
# 🎓 CMU-Africa Campus Assistant

A modern, full-stack AI-powered campus assistant built with RAG (Retrieval-Augmented Generation) technology for CMU-Africa students, faculty, and staff.

## 🌟 Features

### Frontend (React + TypeScript + Tailwind CSS)
- ✨ **Modern, Student-Friendly UI**: Beautiful, responsive design optimized for mobile and desktop
- 💬 **Real-Time Chat Interface**: Smooth conversational experience with message history
- 🎯 **Smart Suggestions**: Contextual suggestion pills displayed ABOVE the input box
- 📚 **Collapsible Sources**: Expandable source citations for transparency
- 🔄 **Follow-Up Questions**: AI-generated follow-up suggestions as clickable buttons
- 🎨 **Attractive Design**: CMU-branded colors with smooth animations

### Backend (Python FastAPI)
- 🤖 **Strict RAG Pipeline**: No hallucination - only context-based responses
- 🔍 **Vector Search**: Pinecone integration for semantic search
- 🧠 **OpenAI Integration**: GPT-4 for intelligent response generation
- 📊 **Structured JSON Responses**: Consistent format with answer, sources, suggestions, and follow-ups
- 🛡️ **Error Handling**: Robust fallback mechanisms
- 🚀 **Fast & Scalable**: Async FastAPI for high performance

### Key Capabilities
- **Academic Information**: Programs, courses, requirements
- **Transportation**: Shuttle schedules, routes, tracking
- **Campus Life**: Events, clubs, activities
- **Housing**: Options, applications, availability
- **General Inquiries**: Library hours, contact info, facilities

## 📁 Project Structure

```
cmu-africa-campus-assistant/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── rag_pipeline.py         # Enhanced RAG pipeline
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── load_knowledge_base.py # Script to load sample data
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── SuggestionPills.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── Header.tsx
│   │   │   └── WelcomeScreen.tsx
│   │   ├── services/
│   │   │   └── api.ts         # API service layer
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript types
│   │   ├── App.tsx            # Main App component
│   │   ├── App.css
│   │   ├── index.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── .env
├── data/
│   └── sample_knowledge_base.json  # Sample CMU-Africa data
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone API Key** ([Get one here](https://www.pinecone.io/))

### 1. Clone the Repository

```bash
cd /home/ubuntu/code_artifacts/cmu-africa-campus-assistant
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# OPENAI_API_KEY=your_openai_key_here
# PINECONE_API_KEY=your_pinecone_key_here
```

**Edit `.env` file:**
```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
```

### 3. Load Sample Knowledge Base (Optional)

```bash
# Still in backend directory
python load_knowledge_base.py
```

This will index sample CMU-Africa information into Pinecone.

### 4. Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: **http://localhost:8000**

Test health endpoint: **http://localhost:8000/api/health**

### 5. Frontend Setup

Open a **new terminal**:

```bash
cd /home/ubuntu/code_artifacts/cmu-africa-campus-assistant/frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be running at: **http://localhost:3000**

The app should automatically open in your browser! 🎉

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "rag_pipeline": "initialized",
  "vector_store_stats": {
    "total_vectors": 50,
    "dimension": 1536
  }
}
```

#### 2. Chat Query
```http
POST /api/chat
```

**Request Body:**
```json
{
  "message": "What are the shuttle bus timings?",
  "user_profile": {
    "program": "MSIT",
    "year": 2
  },
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "answer": "CMU-Africa provides free shuttle bus services...",
  "sources": [
    {
      "id": "bus_services_1",
      "title": "CMU-Africa Shuttle Bus Services",
      "snippet": "The shuttle operates on weekdays from 7:00 AM...",
      "category": "Transportation"
    }
  ],
  "suggestions": [
    {
      "id": "bus_schedule",
      "label": "📅 Bus Schedule",
      "prompt": "What are the shuttle bus timings today?"
    }
  ],
  "follow_up": "Would you like to know about weekend shuttle schedules?"
}
```

#### 3. Index Documents
```http
POST /api/index/documents
```

**Request Body:**
```json
[
  {
    "id": "doc_1",
    "title": "Document Title",
    "content": "Document content...",
    "category": "Academic Programs",
    "keywords": ["keyword1", "keyword2"]
  }
]
```

#### 4. Index Statistics
```http
GET /api/index/stats
```

## 🎨 Frontend Features

### Suggestion Pills
Contextual suggestions appear **above** the input box as interactive pills:
- 📅 Bus Schedule
- 🗺️ View Routes
- 📚 Course List
- 🎉 Campus Events

### Collapsible Sources
Each AI response includes collapsible sources with:
- Source title and category badge
- Snippet (max 25 words)
- Direct quotes from context

### Follow-Up Questions
AI-generated follow-up questions appear as clickable suggestions

### Responsive Design
- Mobile-first approach
- Smooth animations
- Accessible color scheme
- CMU-branded (red: #C41230)

## 🔧 Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --port 8000

# Run tests (if you add them)
pytest
```

### Frontend Development

```bash
cd frontend

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Adding New Knowledge

Edit `data/sample_knowledge_base.json` and add new entries:

```json
{
  "id": "unique_id",
  "title": "Document Title",
  "category": "Category Name",
  "content": "Full content here...",
  "keywords": ["keyword1", "keyword2"]
}
```

Then run:
```bash
cd backend
python load_knowledge_base.py
```

## 🛠️ Customization

### Modify Suggestion Generation

Edit `backend/rag_pipeline.py`, function `_generate_suggestions()`:

```python
suggestion_templates = {
    'YourCategory': [
        {'id': 'action_id', 'label': '🔥 Label', 
         'prompt': 'Full user prompt here'}
    ]
}
```

### Adjust UI Colors

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  cmu: {
    red: '#C41230',  // Change this
    gray: '#6B6B6B',
  }
}
```

### Modify System Prompt

Edit `backend/rag_pipeline.py`, function `query()`:

```python
system_prompt = f"""You are the CMU-Africa Campus Assistant...
Your custom instructions here...
"""
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "API keys not configured"**
- Make sure `.env` file exists in `backend/` directory
- Check that `OPENAI_API_KEY` and `PINECONE_API_KEY` are set

**Error: "Failed to initialize Pinecone index"**
- Verify your Pinecone API key is correct
- Check your Pinecone account has available index capacity
- Ensure the region matches your Pinecone project

**Error: "Failed to create embedding"**
- Check OpenAI API key is valid
- Verify you have credits in your OpenAI account

### Frontend Issues

**Error: "Failed to get response"**
- Ensure backend is running on port 8000
- Check `frontend/.env` has correct `REACT_APP_API_BASE_URL`
- Visit http://localhost:8000/api/health to verify backend

**CORS Errors**
- Backend already has CORS configured for localhost:3000
- If using different port, update `backend/main.py` CORS settings

**npm install fails**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Try `npm install --legacy-peer-deps`

## 📊 System Architecture

```
┌─────────────────┐
│   User Browser  │
│  (localhost:3000)│
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  React Frontend │
│  - TypeScript   │
│  - Tailwind CSS │
│  - Axios        │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│  FastAPI Backend│
│  - Python       │
│  (localhost:8000)│
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌───────────┐
│Pinecone│  │  OpenAI   │
│Vector  │  │  GPT-4    │
│ Store  │  │Embeddings │
└────────┘  └───────────┘
```

## 🎯 Strict RAG Rules

The system follows **strict RAG-first principles**:

1. **No Hallucination**: Responses only from retrieved context
2. **Transparency**: All sources cited and accessible
3. **Fallback Handling**: Clear messaging when info unavailable
4. **Contextual Suggestions**: Personalized based on query and profile
5. **Follow-Up Generation**: Natural conversation flow

## 📝 License

This project is part of CMU-Africa educational initiatives.

## 🤝 Contributing

To add new features:
1. Backend: Add endpoints in `backend/main.py`
2. Frontend: Add components in `frontend/src/components/`
3. Test thoroughly before deployment

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review API documentation
- Check backend logs: `backend/` terminal
- Check frontend console: Browser DevTools

## 🎓 Built With

- **Frontend**: React 18, TypeScript, Tailwind CSS, Axios
- **Backend**: FastAPI, Python 3.8+, Pydantic
- **AI/ML**: OpenAI GPT-4, OpenAI Embeddings
- **Vector DB**: Pinecone
- **Deployment**: Uvicorn (ASGI server)

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Maintained by**: CMU-Africa Tech Team

🎉 **Enjoy your AI-powered campus assistant!** 🎉
