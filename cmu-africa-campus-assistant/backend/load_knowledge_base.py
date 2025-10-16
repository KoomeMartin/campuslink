
"""
Script to load sample CMU-Africa knowledge base into Pinecone
"""
import json
import os
from dotenv import load_dotenv
from rag_pipeline import EnhancedRAGPipeline

# Load environment variables
load_dotenv()

def load_knowledge_base():
    """Load sample knowledge base into vector store"""
    
    # Path to existing knowledge base
    kb_path = "../data/sample_knowledge_base.json"
    
    # Check if file exists, if not, use the original one
    if not os.path.exists(kb_path):
        kb_path = "/home/ubuntu/code_artifacts/cmu-africa-assistant/data/cmu_africa_knowledge_base.json"
    
    print(f"Loading knowledge base from: {kb_path}")
    
    # Load documents
    try:
        with open(kb_path, 'r') as f:
            documents = json.load(f)
        print(f"Loaded {len(documents)} documents")
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at {kb_path}")
        return
    
    # Initialize RAG pipeline
    print("Initializing RAG pipeline...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    
    if not openai_api_key or not pinecone_api_key:
        print("Error: Please set OPENAI_API_KEY and PINECONE_API_KEY in .env file")
        return
    
    try:
        pipeline = EnhancedRAGPipeline(
            openai_api_key=openai_api_key,
            pinecone_api_key=pinecone_api_key,
            pinecone_environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        )
        print("RAG pipeline initialized successfully!")
    except Exception as e:
        print(f"Error initializing RAG pipeline: {e}")
        return
    
    # Index documents
    print("Indexing documents into Pinecone...")
    try:
        pipeline.index_documents(documents)
        print(f"✅ Successfully indexed {len(documents)} documents!")
        
        # Get stats
        stats = pipeline.get_index_stats()
        print(f"\nIndex Statistics:")
        print(f"  Total vectors: {stats.get('total_vectors', 0)}")
        print(f"  Dimension: {stats.get('dimension', 0)}")
        
    except Exception as e:
        print(f"Error indexing documents: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("CMU-Africa Campus Assistant - Knowledge Base Loader")
    print("=" * 60)
    load_knowledge_base()
    print("\n✅ Knowledge base loading complete!")
    print("You can now start the FastAPI server: python main.py")
