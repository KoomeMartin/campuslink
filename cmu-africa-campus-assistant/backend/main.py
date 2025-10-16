
"""
FastAPI Backend for CMU-Africa Campus Assistant
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv
from rag_pipeline import EnhancedRAGPipeline
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="CMU-Africa Campus Assistant API",
    description="AI-powered campus assistant with RAG pipeline",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_profile: Optional[Dict] = None
    session_id: Optional[str] = None

class Source(BaseModel):
    id: str
    title: str
    snippet: str
    category: str

class Suggestion(BaseModel):
    id: str
    label: str
    prompt: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    suggestions: List[Suggestion]
    follow_up: Optional[str] = None

# Initialize RAG pipeline
rag_pipeline = None

def get_rag_pipeline():
    """Get or initialize RAG pipeline"""
    global rag_pipeline
    if rag_pipeline is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        if not openai_api_key or not pinecone_api_key:
            raise HTTPException(
                status_code=500,
                detail="API keys not configured. Please set OPENAI_API_KEY and PINECONE_API_KEY in .env file"
            )
        
        try:
            rag_pipeline = EnhancedRAGPipeline(
                openai_api_key=openai_api_key,
                pinecone_api_key=pinecone_api_key,
                pinecone_environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize RAG pipeline: {str(e)}")
    
    return rag_pipeline

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CMU-Africa Campus Assistant API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        pipeline = get_rag_pipeline()
        stats = pipeline.get_index_stats()
        return {
            "status": "healthy",
            "rag_pipeline": "initialized",
            "vector_store_stats": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user queries and returns structured responses
    
    Request body:
    {
        "message": "User's question",
        "user_profile": {"program": "MSIT", "year": 2},  // Optional
        "session_id": "unique-session-id"  // Optional
    }
    
    Response:
    {
        "answer": "AI-generated response",
        "sources": [{"id": "...", "title": "...", "snippet": "...", "category": "..."}],
        "suggestions": [{"id": "...", "label": "...", "prompt": "..."}],
        "follow_up": "Suggested follow-up question"
    }
    """
    try:
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get RAG pipeline
        pipeline = get_rag_pipeline()
        
        # Process query
        result = pipeline.query(
            user_query=request.message,
            user_profile=request.user_profile,
            session_id=request.session_id
        )
        
        return ChatResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

@app.post("/api/index/documents")
async def index_documents(documents: List[Dict]):
    """
    Index documents into the vector store
    
    Request body:
    [
        {
            "id": "doc_1",
            "title": "Document Title",
            "content": "Document content...",
            "category": "Category",
            "keywords": ["keyword1", "keyword2"]
        }
    ]
    """
    try:
        pipeline = get_rag_pipeline()
        success = pipeline.index_documents(documents)
        return {
            "status": "success" if success else "failed",
            "indexed_count": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index documents: {str(e)}")

@app.get("/api/index/stats")
async def get_index_stats():
    """Get vector store statistics"""
    try:
        pipeline = get_rag_pipeline()
        stats = pipeline.get_index_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
