#!/usr/bin/env python3
"""
Script to populate Pinecone with sample CMU-Africa knowledge base data
"""
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import config
from src.utils.rag_pipeline import RAGPipeline


def load_sample_data(filepath: str = "src/data/sample_knowledge_base.json"):
    """Load sample knowledge base data from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} documents from {filepath}")
        return data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []


def populate_database():
    """Main function to populate Pinecone with sample data"""
    print("=" * 60)
    print("CMU-Africa Information Assistant - Data Population Script")
    print("=" * 60)
    print()
    
    # Check configuration
    missing_keys = config.validate()
    if missing_keys:
        print("❌ Error: Missing required configuration:")
        for key in missing_keys:
            print(f"   - {key}")
        print()
        print("Please set up your API keys in the .env file or environment variables.")
        print("See .env.example for reference.")
        return False
    
    print("✅ Configuration validated")
    print()
    
    # Initialize RAG pipeline
    print("🔄 Initializing RAG pipeline...")
    try:
        rag = RAGPipeline()
        if not rag.initialize_index():
            print("❌ Failed to initialize Pinecone index")
            return False
        print("✅ RAG pipeline initialized")
        print()
    except Exception as e:
        print(f"❌ Error initializing pipeline: {e}")
        return False
    
    # Check current index stats
    print("📊 Current index statistics:")
    stats = rag.get_index_stats()
    if "error" not in stats:
        print(f"   - Total vectors: {stats.get('total_vectors', 0)}")
        print(f"   - Dimension: {stats.get('dimension', 0)}")
        print(f"   - Index fullness: {stats.get('index_fullness', 0):.2%}")
    print()
    
    # Load sample data
    print("📂 Loading sample data...")
    documents = load_sample_data()
    
    if not documents:
        print("❌ No documents to upload")
        return False
    
    print()
    
    # Populate database
    print(f"📤 Uploading {len(documents)} documents to Pinecone...")
    print()
    
    successful, failed = rag.upsert_documents_batch(documents)
    
    print()
    print("=" * 60)
    print("Results:")
    print(f"   ✅ Successfully uploaded: {successful}")
    print(f"   ❌ Failed: {failed}")
    print("=" * 60)
    print()
    
    if failed > 0:
        print("⚠️  Some documents failed to upload. Check the logs above.")
    else:
        print("🎉 All documents uploaded successfully!")
    
    # Show updated stats
    print()
    print("📊 Updated index statistics:")
    stats = rag.get_index_stats()
    if "error" not in stats:
        print(f"   - Total vectors: {stats.get('total_vectors', 0)}")
        print(f"   - Dimension: {stats.get('dimension', 0)}")
        print(f"   - Index fullness: {stats.get('index_fullness', 0):.2%}")
    print()
    
    # Test search
    print("🔍 Testing search functionality...")
    test_query = "What shuttle services are available?"
    print(f"   Query: '{test_query}'")
    results = rag.search(test_query, top_k=3)
    
    if results:
        print(f"   ✅ Found {len(results)} relevant documents:")
        for i, doc in enumerate(results, 1):
            print(f"      {i}. {doc['title']} (Score: {doc['score']:.3f})")
    else:
        print("   ⚠️  No results found")
    
    print()
    print("✅ Population script completed!")
    print()
    print("You can now run the application with:")
    print("   streamlit run src/app.py")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = populate_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
