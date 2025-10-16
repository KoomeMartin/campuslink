"""
Embeddings Module - Handles text embeddings using sentence-transformers
"""

import os
from typing import List, Union
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:
    """
    Wrapper class for sentence-transformer embeddings
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        if model_name is None:
            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence-transformer model"""
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded successfully. Embedding dimension: {self.get_dimension()}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def encode(self, texts: Union[str, List[str]], batch_size: int = 32, show_progress: bool = False) -> np.ndarray:
        """
        Generate embeddings for input text(s)
        
        Args:
            texts: Single text string or list of text strings
            batch_size: Number of texts to process at once
            show_progress: Whether to show progress bar
            
        Returns:
            numpy array of embeddings
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please initialize the model first.")
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
    
    def get_dimension(self) -> int:
        """
        Get the embedding dimension of the model
        
        Returns:
            Embedding dimension
        """
        if self.model is None:
            raise ValueError("Model not loaded.")
        
        return self.model.get_sentence_embedding_dimension()
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Encode a single query text
        
        Args:
            query: Query text string
            
        Returns:
            numpy array of embedding
        """
        return self.encode(query)
    
    def encode_documents(self, documents: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Encode multiple documents
        
        Args:
            documents: List of document text strings
            batch_size: Batch size for processing
            
        Returns:
            numpy array of embeddings
        """
        return self.encode(documents, batch_size=batch_size, show_progress=True)


# Global instance for reuse
_embedding_model_instance = None


def get_embedding_model() -> EmbeddingModel:
    """
    Get or create a singleton embedding model instance
    
    Returns:
        EmbeddingModel instance
    """
    global _embedding_model_instance
    
    if _embedding_model_instance is None:
        _embedding_model_instance = EmbeddingModel()
    
    return _embedding_model_instance
