"""
RAG Pipeline Module - Orchestrates the Retrieval-Augmented Generation process
"""

from typing import List, Dict, Any, Optional, Tuple
from .embeddings import get_embedding_model
from .vector_store import get_vector_store
from .llm import get_llm_client


class RAGPipeline:
    """
    RAG Pipeline that coordinates query processing, retrieval, and response generation
    """
    
    def __init__(self):
        """Initialize RAG pipeline components"""
        self.embedding_model = None
        self.vector_store = None
        self.llm_client = None
        self.initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize all RAG components
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print("Initializing RAG pipeline...")
            
            # Initialize embedding model
            print("Loading embedding model...")
            self.embedding_model = get_embedding_model()
            
            # Initialize vector store
            print("Connecting to vector store...")
            self.vector_store = get_vector_store()
            self.vector_store.connect_to_index()
            
            # Initialize LLM client
            print("Initializing LLM client...")
            self.llm_client = get_llm_client()
            
            self.initialized = True
            print("RAG pipeline initialized successfully!")
            return True
        
        except Exception as e:
            print(f"Error initializing RAG pipeline: {e}")
            self.initialized = False
            return False
    
    def query(self, user_query: str, top_k: int = 5, 
             conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline
        
        Args:
            user_query: User's question
            top_k: Number of documents to retrieve
            conversation_history: Previous conversation messages
            
        Returns:
            Dictionary containing response and metadata
        """
        if not self.initialized:
            return {
                "response": "System not initialized. Please check your configuration.",
                "sources": [],
                "error": "System not initialized"
            }
        
        try:
            # Step 1: Generate query embedding
            query_embedding = self._embed_query(user_query)
            
            # Step 2: Retrieve relevant documents
            retrieved_docs = self._retrieve_documents(query_embedding, top_k)
            
            # Step 3: Generate response using LLM
            response = self._generate_response(user_query, retrieved_docs, conversation_history)
            
            # Step 4: Format and return results
            return {
                "response": response,
                "sources": self._format_sources(retrieved_docs),
                "num_sources": len(retrieved_docs),
                "error": None
            }
        
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your question. Please try again.",
                "sources": [],
                "error": str(e)
            }
    
    def _embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for user query
        
        Args:
            query: User's question
            
        Returns:
            Query embedding vector
        """
        return self.embedding_model.encode_query(query)
    
    def _retrieve_documents(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from vector store
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents with metadata
        """
        results = self.vector_store.query(
            query_vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract matches
        matches = results.get('matches', [])
        
        # Format documents
        documents = []
        for match in matches:
            documents.append({
                'id': match.get('id'),
                'score': match.get('score'),
                'metadata': match.get('metadata', {})
            })
        
        return documents
    
    def _generate_response(self, query: str, documents: List[Dict[str, Any]], 
                          conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate response using LLM with retrieved context
        
        Args:
            query: User's question
            documents: Retrieved documents
            conversation_history: Previous conversation messages
            
        Returns:
            Generated response
        """
        return self.llm_client.generate_response(query, documents, conversation_history)
    
    def _format_sources(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format source documents for display
        
        Args:
            documents: Retrieved documents
            
        Returns:
            Formatted sources
        """
        sources = []
        for doc in documents:
            metadata = doc.get('metadata', {})
            sources.append({
                'title': metadata.get('title', 'Unknown'),
                'category': metadata.get('category', 'General'),
                'score': round(doc.get('score', 0.0), 3),
                'content_preview': metadata.get('content', '')[:200] + '...' if len(metadata.get('content', '')) > 200 else metadata.get('content', '')
            })
        
        return sources
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get status of RAG pipeline components
        
        Returns:
            Status dictionary
        """
        status = {
            "initialized": self.initialized,
            "embedding_model": self.embedding_model is not None,
            "vector_store": self.vector_store is not None,
            "llm_client": self.llm_client is not None
        }
        
        # Get vector store stats if available
        if self.vector_store and self.initialized:
            try:
                stats = self.vector_store.get_index_stats()
                status["vector_count"] = stats.get('total_vector_count', 0)
                status["index_name"] = self.vector_store.index_name
            except:
                status["vector_count"] = "Unknown"
        
        return status


# Global pipeline instance
_rag_pipeline_instance = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Get or create a singleton RAG pipeline instance
    
    Returns:
        RAGPipeline instance
    """
    global _rag_pipeline_instance
    
    if _rag_pipeline_instance is None:
        _rag_pipeline_instance = RAGPipeline()
    
    return _rag_pipeline_instance
