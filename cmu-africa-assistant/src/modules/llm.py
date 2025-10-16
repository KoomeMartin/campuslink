"""
LLM Module - Handles OpenAI GPT-4 integration for response generation
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI


class LLMClient:
    """
    Wrapper class for OpenAI GPT-4 operations
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key
            model: Model name to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY in environment.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        print(f"OpenAI client initialized with model: {self.model}")
    
    def generate_response(self, query: str, context: List[Dict[str, Any]], 
                         conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using retrieved context
        
        Args:
            query: User's question
            context: List of retrieved documents with metadata
            conversation_history: Previous conversation messages
            
        Returns:
            Generated response
        """
        # Build context string from retrieved documents
        context_str = self._build_context_string(context)
        
        # Build system prompt
        system_prompt = self._build_system_prompt()
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Keep last 3 exchanges (6 messages)
        
        # Add current query with context
        user_message = f"""Context information from CMU-Africa knowledge base:
{context_str}

Question: {query}

Please provide a helpful, accurate answer based on the context above. If the context doesn't contain enough information to answer the question, say so clearly."""
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=500,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again later."
    
    def _build_context_string(self, context: List[Dict[str, Any]]) -> str:
        """
        Build a formatted context string from retrieved documents
        
        Args:
            context: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not context:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        for i, doc in enumerate(context, 1):
            metadata = doc.get('metadata', {})
            content = metadata.get('content', '')
            title = metadata.get('title', 'Unknown')
            category = metadata.get('category', 'General')
            
            context_parts.append(f"[Source {i}] Category: {category} | Title: {title}\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _build_system_prompt(self) -> str:
        """
        Build the system prompt for the assistant
        
        Returns:
            System prompt string
        """
        prompt = """You are an intelligent information assistant for Carnegie Mellon University Africa (CMU-Africa). 
Your role is to help students, faculty, and staff find accurate information about the campus.

Guidelines:
1. Provide accurate, helpful information based ONLY on the context provided from the CMU-Africa knowledge base
2. If the context doesn't contain enough information to answer confidently, clearly state: "I currently don't have enough verified information on that. You may refer to the CMU-Africa student handbook or administration office."
3. Be concise but thorough - use bullet points for lists, short paragraphs for explanations
4. Always maintain a professional, friendly tone
5. When providing schedules or specific details, be precise
6. If appropriate, suggest follow-up questions or related topics the user might want to know about
7. NEVER make up or hallucinate information that isn't in the provided context
8. If you're referencing specific information, you can mention the source (e.g., "According to the transportation policies...")

Remember: Accuracy and honesty are more important than trying to answer every question."""
        
        return prompt
    
    def check_availability(self) -> bool:
        """
        Check if the OpenAI API is available
        
        Returns:
            True if available, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"OpenAI API check failed: {e}")
            return False


def get_llm_client() -> LLMClient:
    """
    Create and return an LLMClient instance
    
    Returns:
        LLMClient instance
    """
    return LLMClient()
