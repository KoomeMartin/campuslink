
"""
RAG (Retrieval Augmented Generation) Pipeline for CMU-Africa Assistant
"""
import json
from typing import List, Dict, Optional, Tuple
import openai
from pinecone import Pinecone, ServerlessSpec
import time

class RAGPipeline:
    """Manages the RAG pipeline with Pinecone and OpenAI"""
    
    def __init__(self, openai_api_key: str, pinecone_api_key: str, 
                 pinecone_environment: str, index_name: str = "cmu-africa-knowledge-base"):
        """Initialize the RAG pipeline"""
        self.openai_api_key = openai_api_key
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        self.index_name = index_name
        self.embedding_model = "text-embedding-3-small"
        self.dimension = 1536  # Dimension for text-embedding-3-small
        
        # Initialize OpenAI
        openai.api_key = self.openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = None
        self._init_pinecone_index()
    
    def _init_pinecone_index(self):
        """Initialize or connect to Pinecone index"""
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                # Create new index
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                # Wait for index to be ready
                time.sleep(1)
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            
        except Exception as e:
            raise Exception(f"Failed to initialize Pinecone index: {str(e)}")
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to create embedding: {str(e)}")
    
    def index_documents(self, documents: List[Dict]) -> bool:
        """Index documents into Pinecone vector store"""
        try:
            vectors = []
            for doc in documents:
                # Create embedding for document content
                embedding = self.create_embedding(doc['content'])
                
                # Prepare metadata
                metadata = {
                    'title': doc.get('title', ''),
                    'category': doc.get('category', ''),
                    'content': doc['content'],
                    'keywords': ','.join(doc.get('keywords', []))
                }
                
                vectors.append({
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': metadata
                })
            
            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to index documents: {str(e)}")
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant context from vector store"""
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query)
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            contexts = []
            for match in results['matches']:
                contexts.append({
                    'content': match['metadata']['content'],
                    'title': match['metadata']['title'],
                    'category': match['metadata']['category'],
                    'score': match['score']
                })
            
            return contexts
        except Exception as e:
            raise Exception(f"Failed to retrieve context: {str(e)}")
    
    def generate_response(self, query: str, contexts: List[Dict], 
                         temperature: float = 0.3, max_tokens: int = 500,
                         language: str = "en") -> str:
        """Generate response using OpenAI with retrieved context"""
        try:
            # Prepare context string
            context_str = "\n\n".join([
                f"[{ctx['category']}] {ctx['title']}:\n{ctx['content']}"
                for ctx in contexts
            ])
            
            # Language-specific instructions
            lang_instructions = {
                "en": "Respond in English.",
                "fr": "Répondez en français.",
                "rw": "Subiza mu Kinyarwanda."
            }
            
            # Create system message
            system_message = f"""You are a helpful assistant for CMU-Africa (Carnegie Mellon University Africa campus in Kigali, Rwanda). 
Your role is to provide accurate, helpful information about CMU-Africa based on the provided context.

IMPORTANT GUIDELINES:
- Only answer based on the provided context. Do not make up information.
- If the context doesn't contain the answer, say "I don't have that information in my knowledge base."
- Be concise and clear. Use bullet points when appropriate.
- Be friendly and professional.
- {lang_instructions.get(language, "Respond in English.")}
- Focus on providing actionable information.

Context:
{context_str}"""
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",  # Using GPT-4 (gpt-4-mini is not a valid model name)
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def query(self, user_query: str, language: str = "en") -> Tuple[str, List[Dict]]:
        """Main query method - retrieve and generate"""
        # Retrieve relevant context
        contexts = self.retrieve_context(user_query, top_k=5)
        
        # Generate response
        response = self.generate_response(user_query, contexts, language=language)
        
        return response, contexts
    
    def add_document(self, doc_id: str, title: str, content: str, 
                     category: str = "General", keywords: List[str] = None) -> bool:
        """Add a single document to the knowledge base"""
        document = {
            'id': doc_id,
            'title': title,
            'content': content,
            'category': category,
            'keywords': keywords or []
        }
        return self.index_documents([document])
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the knowledge base"""
        try:
            self.index.delete(ids=[doc_id])
            return True
        except Exception as e:
            raise Exception(f"Failed to delete document: {str(e)}")
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the vector index"""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vectors': stats.get('total_vector_count', 0),
                'dimension': stats.get('dimension', 0),
                'index_fullness': stats.get('index_fullness', 0)
            }
        except Exception as e:
            return {'error': str(e)}
