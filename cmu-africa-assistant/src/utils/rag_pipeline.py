
"""
RAG (Retrieval Augmented Generation) Pipeline Implementation
Handles Pinecone vector search and OpenAI response generation
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import tiktoken

from src.config import config


class RAGPipeline:
    """RAG Pipeline for CMU-Africa Information Assistant"""
    
    def __init__(self):
        """Initialize RAG pipeline with OpenAI and Pinecone"""
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self.index_name = config.PINECONE_INDEX_NAME
        self.index = None
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
    def initialize_index(self) -> bool:
        """
        Initialize or connect to Pinecone index
        Returns True if successful, False otherwise
        """
        try:
            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                # Create index if it doesn't exist
                self.pc.create_index(
                    name=self.index_name,
                    dimension=config.PINECONE_DIMENSION,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=config.PINECONE_ENVIRONMENT
                    )
                )
                print(f"Created new index: {self.index_name}")
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            print(f"Connected to index: {self.index_name}")
            return True
            
        except Exception as e:
            print(f"Error initializing Pinecone index: {e}")
            return False
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def upsert_document(self, doc_id: str, text: str, metadata: Dict) -> bool:
        """
        Add or update a document in the vector database
        
        Args:
            doc_id: Unique document identifier
            text: Document text content
            metadata: Document metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.index:
                raise ValueError("Index not initialized")
            
            embedding = self.get_embedding(text)
            if not embedding:
                return False
            
            # Add text to metadata for retrieval
            metadata["text"] = text
            metadata["indexed_at"] = datetime.now().isoformat()
            
            self.index.upsert(vectors=[(doc_id, embedding, metadata)])
            return True
            
        except Exception as e:
            print(f"Error upserting document: {e}")
            return False
    
    def upsert_documents_batch(self, documents: List[Dict]) -> Tuple[int, int]:
        """
        Batch upsert multiple documents
        
        Args:
            documents: List of documents with id, text, and metadata
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        for doc in documents:
            doc_id = doc.get("id")
            text = doc.get("content") or doc.get("text", "")
            metadata = doc.get("metadata", {})
            
            # Add title and category to metadata if present
            if "title" in doc:
                metadata["title"] = doc["title"]
            if "category" in doc:
                metadata["category"] = doc["category"]
            
            if self.upsert_document(doc_id, text, metadata):
                successful += 1
            else:
                failed += 1
        
        return successful, failed
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector database
        
        Args:
            doc_id: Document identifier to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.index:
                raise ValueError("Index not initialized")
            
            self.index.delete(ids=[doc_id])
            return True
            
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def search(self, query: str, top_k: int = None, filter_dict: Dict = None) -> List[Dict]:
        """
        Search for relevant documents using semantic search
        
        Args:
            query: Search query
            top_k: Number of results to return (default from config)
            filter_dict: Metadata filter for search
            
        Returns:
            List of relevant documents with metadata and scores
        """
        try:
            if not self.index:
                raise ValueError("Index not initialized")
            
            top_k = top_k or config.TOP_K_RESULTS
            
            # Generate query embedding
            query_embedding = self.get_embedding(query)
            if not query_embedding:
                return []
            
            # Search in Pinecone
            search_kwargs = {
                "vector": query_embedding,
                "top_k": top_k,
                "include_metadata": True
            }
            
            if filter_dict:
                search_kwargs["filter"] = filter_dict
            
            results = self.index.query(**search_kwargs)
            
            # Format results
            documents = []
            for match in results.matches:
                if match.score >= config.SIMILARITY_THRESHOLD:
                    documents.append({
                        "id": match.id,
                        "score": match.score,
                        "text": match.metadata.get("text", ""),
                        "title": match.metadata.get("title", ""),
                        "category": match.metadata.get("category", ""),
                        "metadata": match.metadata
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def generate_response(self, query: str, context_docs: List[Dict], language: str = "en") -> str:
        """
        Generate response using OpenAI GPT-4-mini with retrieved context
        
        Args:
            query: User query
            context_docs: Retrieved context documents
            language: Response language
            
        Returns:
            Generated response
        """
        try:
            if not context_docs:
                if language == "fr":
                    return "Je suis désolé, mais je n'ai pas trouvé d'informations pertinentes dans ma base de connaissances pour répondre à votre question. Pourriez-vous reformuler votre question ou demander quelque chose d'autre sur CMU-Africa ?"
                else:
                    return "I'm sorry, but I couldn't find relevant information in my knowledge base to answer your question. Could you please rephrase your question or ask something else about CMU-Africa?"
            
            # Prepare context from retrieved documents
            context = "\n\n".join([
                f"Document {i+1} (Relevance: {doc['score']:.2f}):\nTitle: {doc['title']}\nCategory: {doc['category']}\nContent: {doc['text']}"
                for i, doc in enumerate(context_docs)
            ])
            
            # Prepare system prompt based on language
            if language == "fr":
                system_prompt = """Vous êtes un assistant d'information pour CMU-Africa. Votre rôle est de fournir des réponses précises et utiles basées UNIQUEMENT sur le contexte fourni.

Règles importantes :
1. Répondez UNIQUEMENT en utilisant les informations du contexte fourni
2. Si l'information n'est pas dans le contexte, dites-le clairement
3. Soyez concis et précis dans vos réponses
4. Utilisez des bullet points ou de courts paragraphes pour la clarté
5. Si plusieurs documents sont pertinents, synthétisez les informations
6. N'inventez jamais d'informations - basez-vous uniquement sur le contexte
7. Répondez toujours en français"""
            else:
                system_prompt = """You are an information assistant for CMU-Africa. Your role is to provide accurate and helpful answers based ONLY on the provided context.

Important rules:
1. Answer ONLY using information from the provided context
2. If the information is not in the context, clearly state that
3. Be concise and precise in your answers
4. Use bullet points or short paragraphs for clarity
5. If multiple documents are relevant, synthesize the information
6. Never make up information - rely only on the context
7. Always respond in English"""
            
            user_prompt = f"""Context:
{context}

Question: {query}

Please provide a helpful answer based on the context above."""
            
            # Generate response using OpenAI
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            if language == "fr":
                return f"Désolé, une erreur s'est produite lors de la génération de la réponse : {str(e)}"
            else:
                return f"Sorry, an error occurred while generating the response: {str(e)}"
    
    def get_answer(self, query: str, language: str = "en") -> Dict:
        """
        Main method to get answer for a query
        Performs search and generates response
        
        Args:
            query: User query
            language: Response language
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Search for relevant documents
            context_docs = self.search(query)
            
            # Generate response
            answer = self.generate_response(query, context_docs, language)
            
            return {
                "answer": answer,
                "sources": context_docs,
                "num_sources": len(context_docs),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting answer: {e}")
            if language == "fr":
                error_msg = f"Désolé, une erreur s'est produite : {str(e)}"
            else:
                error_msg = f"Sorry, an error occurred: {str(e)}"
            
            return {
                "answer": error_msg,
                "sources": [],
                "num_sources": 0,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the Pinecone index"""
        try:
            if not self.index:
                return {"error": "Index not initialized"}
            
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            return {"error": str(e)}
