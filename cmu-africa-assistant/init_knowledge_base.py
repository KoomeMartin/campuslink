"""
Knowledge Base Initialization Script
Loads the knowledge base data and indexes it to Pinecone
"""

import os
import sys
import json
from dotenv import load_dotenv
from tqdm import tqdm

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.embeddings import get_embedding_model
from modules.vector_store import get_vector_store

# Load environment variables
load_dotenv()


def load_knowledge_base(file_path):
    """Load knowledge base from JSON file"""
    print(f"\n📂 Loading knowledge base from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} entries")
        return data
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        return None


def initialize_embeddings():
    """Initialize embedding model"""
    print("\n🔧 Initializing embedding model...")
    try:
        model = get_embedding_model()
        print(f"✅ Embedding model loaded (dimension: {model.get_dimension()})")
        return model
    except Exception as e:
        print(f"❌ Error initializing embedding model: {e}")
        return None


def initialize_vector_store():
    """Initialize vector store"""
    print("\n🔧 Initializing vector store...")
    try:
        store = get_vector_store()
        print("✅ Vector store initialized")
        return store
    except Exception as e:
        print(f"❌ Error initializing vector store: {e}")
        return None


def create_index(vector_store, dimension):
    """Create Pinecone index"""
    print("\n🏗️ Creating/connecting to Pinecone index...")
    try:
        vector_store.create_index(dimension=dimension, metric="cosine")
        print("✅ Index ready")
        return True
    except Exception as e:
        print(f"❌ Error creating index: {e}")
        return False


def prepare_documents(kb_data):
    """Prepare documents for embedding"""
    print("\n📝 Preparing documents for embedding...")
    
    documents = []
    metadata_list = []
    ids = []
    
    for entry in kb_data:
        # Combine title and content for better semantic search
        text = f"{entry['title']}. {entry['content']}"
        documents.append(text)
        ids.append(entry['id'])
        
        # Prepare metadata
        metadata_list.append({
            'id': entry['id'],
            'category': entry['category'],
            'title': entry['title'],
            'content': entry['content'],
            'tags': ','.join(entry.get('tags', []))
        })
    
    print(f"✅ Prepared {len(documents)} documents")
    return documents, ids, metadata_list


def generate_embeddings(embedding_model, documents):
    """Generate embeddings for documents"""
    print("\n🔮 Generating embeddings...")
    print("This may take a few minutes depending on the number of documents...")
    
    try:
        embeddings = embedding_model.encode_documents(documents, batch_size=32)
        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return None


def index_to_pinecone(vector_store, ids, embeddings, metadata_list):
    """Upload vectors to Pinecone"""
    print("\n☁️ Uploading vectors to Pinecone...")
    
    try:
        # Prepare vectors
        vectors = []
        for doc_id, embedding, metadata in zip(ids, embeddings, metadata_list):
            vectors.append((doc_id, embedding.tolist(), metadata))
        
        # Upsert in batches
        vector_store.upsert_vectors(vectors, batch_size=100)
        
        print(f"✅ Successfully uploaded {len(vectors)} vectors to Pinecone")
        return True
    except Exception as e:
        print(f"❌ Error uploading to Pinecone: {e}")
        return False


def verify_index(vector_store):
    """Verify the indexed data"""
    print("\n🔍 Verifying index...")
    
    try:
        stats = vector_store.get_index_stats()
        print(f"✅ Index verification successful!")
        print(f"   Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"   Index fullness: {stats.get('index_fullness', 0)}")
        return True
    except Exception as e:
        print(f"❌ Error verifying index: {e}")
        return False


def main():
    """Main initialization function"""
    print("=" * 60)
    print("🎓 CMU-Africa Information Assistant")
    print("📚 Knowledge Base Initialization")
    print("=" * 60)
    
    # Check for required environment variables
    if not os.getenv("PINECONE_API_KEY"):
        print("\n❌ Error: PINECONE_API_KEY not found in environment variables")
        print("Please set it in your .env file")
        return False
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️ Warning: OPENAI_API_KEY not found")
        print("This is required for the chat interface but not for indexing")
    
    # Define knowledge base path
    kb_path = os.path.join(os.path.dirname(__file__), 'src', 'data', 'knowledge_base.json')
    
    # Step 1: Load knowledge base
    kb_data = load_knowledge_base(kb_path)
    if not kb_data:
        return False
    
    # Step 2: Initialize embedding model
    embedding_model = initialize_embeddings()
    if not embedding_model:
        return False
    
    # Step 3: Initialize vector store
    vector_store = initialize_vector_store()
    if not vector_store:
        return False
    
    # Step 4: Create/connect to index
    dimension = embedding_model.get_dimension()
    if not create_index(vector_store, dimension):
        return False
    
    # Step 5: Prepare documents
    documents, ids, metadata_list = prepare_documents(kb_data)
    
    # Step 6: Generate embeddings
    embeddings = generate_embeddings(embedding_model, documents)
    if embeddings is None:
        return False
    
    # Step 7: Upload to Pinecone
    if not index_to_pinecone(vector_store, ids, embeddings, metadata_list):
        return False
    
    # Step 8: Verify
    verify_index(vector_store)
    
    print("\n" + "=" * 60)
    print("✅ Knowledge base initialization completed successfully!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Visit http://localhost:8501 in your browser")
    print("3. Start asking questions about CMU-Africa!")
    print("\n💡 Tip: You can manage the knowledge base through the Admin Panel")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
