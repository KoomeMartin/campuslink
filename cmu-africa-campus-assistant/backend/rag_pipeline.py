
"""
Enhanced RAG Pipeline for CMU-Africa Campus Assistant
Implements strict JSON response format with suggestions and follow-up questions
"""
import json
from typing import List, Dict, Optional, Tuple
import openai
from pinecone import Pinecone, ServerlessSpec
import time
import re

class EnhancedRAGPipeline:
    """Enhanced RAG pipeline with structured JSON responses"""
    
    def __init__(self, openai_api_key: str, pinecone_api_key: str, 
                 pinecone_environment: str = "us-east-1", 
                 index_name: str = "cmu-africa-assistant"):
        """Initialize the enhanced RAG pipeline"""
        self.openai_api_key = openai_api_key
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        self.index_name = index_name
        self.embedding_model = "text-embedding-3-small"
        self.dimension = 1536
        
        # Initialize OpenAI
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index = None
        self._init_pinecone_index()
    
    def _init_pinecone_index(self):
        """Initialize or connect to Pinecone index"""
        try:
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                time.sleep(1)
            
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
                embedding = self.create_embedding(doc['content'])
                
                metadata = {
                    'title': doc.get('title', ''),
                    'category': doc.get('category', ''),
                    'content': doc['content'][:1000],  # Pinecone metadata limit
                    'keywords': ','.join(doc.get('keywords', []))
                }
                
                vectors.append({
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': metadata
                })
            
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
            query_embedding = self.create_embedding(query)
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            contexts = []
            for match in results.get('matches', []):
                contexts.append({
                    'id': match.get('id', ''),
                    'content': match['metadata']['content'],
                    'title': match['metadata']['title'],
                    'category': match['metadata']['category'],
                    'score': match['score']
                })
            
            return contexts
        except Exception as e:
            raise Exception(f"Failed to retrieve context: {str(e)}")
    
    def _extract_snippet(self, content: str, max_words: int = 25) -> str:
        """Extract a meaningful snippet from content"""
        words = content.split()
        if len(words) <= max_words:
            return content
        return ' '.join(words[:max_words]) + '...'
    
    def _generate_suggestions(self, query: str, contexts: List[Dict], 
                            user_profile: Optional[Dict] = None) -> List[Dict]:
        """Generate personalized suggestion buttons"""
        suggestions = []
        categories = set([ctx['category'] for ctx in contexts])
        
        # Context-based suggestions
        suggestion_templates = {
            'Transportation': [
                {'id': 'bus_schedule', 'label': '📅 Bus Schedule', 
                 'prompt': 'What are the shuttle bus timings today?'},
                {'id': 'bus_routes', 'label': '🗺️ View Routes', 
                 'prompt': 'Show me all shuttle bus routes and stops'}
            ],
            'Academic Programs': [
                {'id': 'program_requirements', 'label': '📚 Requirements', 
                 'prompt': 'What are the graduation requirements for my program?'},
                {'id': 'courses', 'label': '📖 Course List', 
                 'prompt': 'Show me available courses this semester'}
            ],
            'Student Life': [
                {'id': 'events', 'label': '🎉 Campus Events', 
                 'prompt': 'What events are happening this week?'},
                {'id': 'clubs', 'label': '👥 Join Clubs', 
                 'prompt': 'Tell me about student clubs and organizations'}
            ],
            'Housing': [
                {'id': 'housing_options', 'label': '🏠 Housing', 
                 'prompt': 'What housing options are available?'},
                {'id': 'housing_apply', 'label': '📝 Apply', 
                 'prompt': 'How do I apply for on-campus housing?'}
            ]
        }
        
        # Add category-specific suggestions
        for category in categories:
            if category in suggestion_templates:
                suggestions.extend(suggestion_templates[category][:2])
        
        # Add general helpful suggestions
        general_suggestions = [
            {'id': 'contact_admin', 'label': '📞 Contact Admin', 
             'prompt': 'How can I contact the administration office?'},
            {'id': 'portal_access', 'label': '🌐 Student Portal', 
             'prompt': 'How do I access the student portal?'},
            {'id': 'library_hours', 'label': '📚 Library Hours', 
             'prompt': 'What are the library opening hours?'}
        ]
        
        # Limit to 5 suggestions
        if len(suggestions) < 5:
            suggestions.extend(general_suggestions[:5 - len(suggestions)])
        
        return suggestions[:5]
    
    def _generate_follow_up(self, query: str, contexts: List[Dict]) -> Optional[str]:
        """Generate a natural follow-up question"""
        if not contexts:
            return None
        
        category = contexts[0]['category']
        
        follow_ups = {
            'Transportation': 'Would you like to know about weekend shuttle schedules?',
            'Academic Programs': 'Would you like to see the course curriculum details?',
            'Student Life': 'Want to know about upcoming student activities?',
            'Housing': 'Need help with the housing application process?',
            'Admissions': 'Would you like information about application deadlines?'
        }
        
        return follow_ups.get(category, 'Is there anything else you\'d like to know?')
    
    def query(self, user_query: str, user_profile: Optional[Dict] = None, 
              session_id: Optional[str] = None) -> Dict:
        """
        Main query method - retrieve context and generate structured JSON response
        
        Returns:
            {
                "answer": str,
                "sources": List[Dict],
                "suggestions": List[Dict],
                "follow_up": Optional[str]
            }
        """
        try:
            # Retrieve relevant context
            contexts = self.retrieve_context(user_query, top_k=5)
            
            # Check if we have sufficient context
            if not contexts or (contexts and contexts[0]['score'] < 0.5):
                return self._generate_fallback_response(user_query)
            
            # Prepare context for LLM
            context_str = "\n\n".join([
                f"[{ctx['category']}] {ctx['title']}:\n{ctx['content']}"
                for ctx in contexts[:3]
            ])
            
            # Create strict system prompt
            system_prompt = f"""You are the CMU-Africa Campus Assistant. Follow these STRICT rules:

1. RAG-FIRST: Only use the provided context. No hallucination allowed.
2. If context is insufficient, say: "I don't have verified information about that right now."
3. Be concise: 1-5 short paragraphs or bullet points.
4. Be factual and accurate.
5. Be friendly and student-focused.

Context:
{context_str}

Respond with ONLY the answer text. Do not add any extra formatting or metadata."""

            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Format sources (top 3)
            sources = []
            for i, ctx in enumerate(contexts[:3]):
                sources.append({
                    'id': ctx.get('id', f'source_{i+1}'),
                    'title': ctx['title'],
                    'snippet': self._extract_snippet(ctx['content'], 25),
                    'category': ctx['category']
                })
            
            # Generate suggestions
            suggestions = self._generate_suggestions(user_query, contexts, user_profile)
            
            # Generate follow-up
            follow_up = self._generate_follow_up(user_query, contexts)
            
            return {
                'answer': answer,
                'sources': sources,
                'suggestions': suggestions,
                'follow_up': follow_up
            }
            
        except Exception as e:
            return self._generate_error_response(str(e))
    
    def _generate_fallback_response(self, query: str) -> Dict:
        """Generate fallback response when context is insufficient"""
        return {
            'answer': "I don't have verified information about that right now. Would you like me to:\n\n• Search the student portal\n• Contact the admin office\n• Save this as a follow-up question\n\nPlease let me know how I can help!",
            'sources': [],
            'suggestions': [
                {'id': 'portal_search', 'label': '🔍 Search Portal', 
                 'prompt': 'Help me search the student portal'},
                {'id': 'contact_admin', 'label': '📞 Contact Admin', 
                 'prompt': 'How do I contact the administration?'},
                {'id': 'general_info', 'label': 'ℹ️ General Info', 
                 'prompt': 'Tell me about CMU-Africa campus'},
                {'id': 'programs', 'label': '🎓 Programs', 
                 'prompt': 'What programs does CMU-Africa offer?'}
            ],
            'follow_up': 'What would you like to know about CMU-Africa?'
        }
    
    def _generate_error_response(self, error: str) -> Dict:
        """Generate error response"""
        return {
            'answer': "I'm having trouble processing your request right now. Please try again in a moment.",
            'sources': [],
            'suggestions': [
                {'id': 'retry', 'label': '🔄 Try Again', 
                 'prompt': 'Let me try that question again'},
                {'id': 'help', 'label': '❓ Get Help', 
                 'prompt': 'How can I get technical support?'}
            ],
            'follow_up': None
        }
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the vector index"""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vectors': stats.get('total_vector_count', 0),
                'dimension': stats.get('dimension', 0)
            }
        except Exception as e:
            return {'error': str(e)}
