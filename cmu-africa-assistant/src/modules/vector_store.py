"""
Vector Store Module - Handles Pinecone vector database operations
"""

import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
import time


class VectorStore:
    """
    Wrapper class for Pinecone vector database operations
    """
    
    def __init__(self, api_key: str = None, environment: str = None, index_name: str = None):
        """
        Initialize Pinecone vector store
        
        Args:
            api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Name of the Pinecone index
        """
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.environment = environment or os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.index_name = index_name or os.getenv("PINECONE_INDEX_NAME", "cmu-africa-kb")
        
        if not self.api_key:
            raise ValueError("Pinecone API key not provided. Set PINECONE_API_KEY in environment.")
        
        self.pc = None
        self.index = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and index"""
        try:
            print("Initializing Pinecone client...")
            self.pc = Pinecone(api_key=self.api_key)
            print("Pinecone client initialized successfully.")
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            raise
    
    def create_index(self, dimension: int = 384, metric: str = "cosine"):
        """
        Create a new Pinecone index if it doesn't exist
        
        Args:
            dimension: Dimension of the embeddings
            metric: Distance metric (cosine, euclidean, dotproduct)
        """
        try:
            existing_indexes = self.pc.list_indexes()
            index_names = [index.name for index in existing_indexes]
            
            if self.index_name not in index_names:
                print(f"Creating index '{self.index_name}' with dimension {dimension}...")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=dimension,
                    metric=metric,
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=self.environment
                    )
                )
                # Wait for index to be ready
                while not self.pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
                print(f"Index '{self.index_name}' created successfully.")
            else:
                print(f"Index '{self.index_name}' already exists.")
            
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            print(f"Error creating index: {e}")
            raise
    
    def connect_to_index(self):
        """Connect to existing Pinecone index"""
        try:
            existing_indexes = self.pc.list_indexes()
            index_names = [index.name for index in existing_indexes]
            
            if self.index_name not in index_names:
                raise ValueError(f"Index '{self.index_name}' does not exist. Create it first.")
            
            self.index = self.pc.Index(self.index_name)
            print(f"Connected to index '{self.index_name}'.")
        except Exception as e:
            print(f"Error connecting to index: {e}")
            raise
    
    def upsert_vectors(self, vectors: List[tuple], batch_size: int = 100):
        """
        Upsert vectors to Pinecone index
        
        Args:
            vectors: List of tuples (id, embedding, metadata)
            batch_size: Batch size for upserting
        """
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            total = len(vectors)
            for i in range(0, total, batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
                print(f"Upserted {min(i + batch_size, total)}/{total} vectors")
            
            print(f"Successfully upserted {total} vectors to index.")
        except Exception as e:
            print(f"Error upserting vectors: {e}")
            raise
    
    def query(self, query_vector: List[float], top_k: int = 5, 
              filter: Dict[str, Any] = None, include_metadata: bool = True) -> Dict[str, Any]:
        """
        Query the vector index
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            filter: Metadata filter
            include_metadata: Whether to include metadata in results
            
        Returns:
            Query results
        """
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            results = self.index.query(
                vector=query_vector.tolist() if hasattr(query_vector, 'tolist') else query_vector,
                top_k=top_k,
                filter=filter,
                include_metadata=include_metadata
            )
            return results
        except Exception as e:
            print(f"Error querying index: {e}")
            raise
    
    def delete_vectors(self, ids: List[str]):
        """
        Delete vectors from index by IDs
        
        Args:
            ids: List of vector IDs to delete
        """
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            self.index.delete(ids=ids)
            print(f"Deleted {len(ids)} vectors from index.")
        except Exception as e:
            print(f"Error deleting vectors: {e}")
            raise
    
    def delete_all(self):
        """Delete all vectors from the index"""
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            self.index.delete(delete_all=True)
            print("Deleted all vectors from index.")
        except Exception as e:
            print(f"Error deleting all vectors: {e}")
            raise
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index
        
        Returns:
            Index statistics
        """
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            print(f"Error getting index stats: {e}")
            raise
    
    def fetch_vectors(self, ids: List[str]) -> Dict[str, Any]:
        """
        Fetch vectors by IDs
        
        Args:
            ids: List of vector IDs
            
        Returns:
            Fetched vectors with metadata
        """
        if self.index is None:
            raise ValueError("Index not connected. Call connect_to_index() first.")
        
        try:
            results = self.index.fetch(ids=ids)
            return results
        except Exception as e:
            print(f"Error fetching vectors: {e}")
            raise


def get_vector_store() -> VectorStore:
    """
    Create and return a VectorStore instance
    
    Returns:
        VectorStore instance
    """
    return VectorStore()
