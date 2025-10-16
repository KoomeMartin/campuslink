
"""
Main Streamlit application for CMU-Africa Information Assistant
"""
import streamlit as st
from src.config import config
from src.utils.rag_pipeline import RAGPipeline
from src.utils.storage import storage_manager
from src.utils.translations import get_text

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #C41230;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e8f4f8;
    }
    .source-card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #C41230;
        margin-bottom: 0.5rem;
    }
    .feedback-section {
        margin-top: 1rem;
        padding: 1rem;
        background-color: #f9f9f9;
        border-radius: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = config.DEFAULT_LANGUAGE

if "user_id" not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Carnegie_Mellon_wordmark.svg/1024px-Carnegie_Mellon_wordmark.svg.png", width=200)
    
    st.markdown("---")
    
    # Language selector
    language_options = {code: name for code, name in config.SUPPORTED_LANGUAGES.items()}
    selected_language = st.selectbox(
        get_text("language", st.session_state.language),
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=list(language_options.keys()).index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Go to",
        ["Chat", "Admin Panel", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Status indicators
    st.markdown("### 📊 Status")
    
    # Check API configuration
    missing_keys = config.validate()
    if missing_keys:
        st.error(f"❌ Missing: {', '.join(missing_keys)}")
    else:
        st.success("✅ API Keys Configured")
    
    # Initialize RAG pipeline if not done
    if st.session_state.rag_pipeline is None and not missing_keys:
        with st.spinner("Initializing..."):
            try:
                rag = RAGPipeline()
                if rag.initialize_index():
                    st.session_state.rag_pipeline = rag
                    st.success("✅ Connected to Pinecone")
                else:
                    st.error("❌ Failed to connect to Pinecone")
            except Exception as e:
                st.error(f"❌ Initialization error: {str(e)}")
    
    # Display index stats if available
    if st.session_state.rag_pipeline:
        stats = st.session_state.rag_pipeline.get_index_stats()
        if "error" not in stats:
            st.metric("Documents", stats.get("total_vectors", 0))

# Main content based on selected page
if page == "Chat":
    from src.pages import chat
    chat.show()
elif page == "Admin Panel":
    from src.pages import admin
    admin.show()
elif page == "Settings":
    from src.pages import settings
    settings.show()
