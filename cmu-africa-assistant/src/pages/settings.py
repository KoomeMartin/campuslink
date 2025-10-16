"""
Settings page for configuration management
"""
import streamlit as st
import os
from src.config import config
from src.utils.translations import get_text


def show():
    """Display the settings page"""
    lang = st.session_state.language
    
    st.markdown(f"# {get_text('settings_title', lang)}")
    
    st.markdown("---")
    
    # API Configuration Section
    st.markdown(f"### 🔑 {get_text('settings_api', lang)}")
    
    st.info("""
    ℹ️ **Important Information:**
    - API keys are loaded from environment variables or a `.env` file
    - For production deployment, use environment variables
    - For local development, create a `.env` file in the project root
    - Never commit API keys to version control
    """)
    
    # Display current configuration status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### OpenAI Configuration")
        if config.OPENAI_API_KEY:
            masked_key = config.OPENAI_API_KEY[:8] + "..." + config.OPENAI_API_KEY[-4:]
            st.success(f"✅ Configured: `{masked_key}`")
        else:
            st.error("❌ Not configured")
        
        st.markdown(f"**Model:** {config.OPENAI_MODEL}")
        st.markdown(f"**Max Tokens:** {config.MAX_TOKENS}")
        st.markdown(f"**Temperature:** {config.TEMPERATURE}")
    
    with col2:
        st.markdown("#### Pinecone Configuration")
        if config.PINECONE_API_KEY:
            masked_key = config.PINECONE_API_KEY[:8] + "..." + config.PINECONE_API_KEY[-4:]
            st.success(f"✅ Configured: `{masked_key}`")
        else:
            st.error("❌ Not configured")
        
        st.markdown(f"**Environment:** {config.PINECONE_ENVIRONMENT or 'Not set'}")
        st.markdown(f"**Index Name:** {config.PINECONE_INDEX_NAME}")
        st.markdown(f"**Dimension:** {config.PINECONE_DIMENSION}")
    
    st.markdown("---")
    
    # Configuration Instructions
    with st.expander("📖 Setup Instructions"):
        st.markdown("""
        ### How to Configure API Keys
        
        #### Option 1: Using .env file (Recommended for local development)
        
        1. Copy `.env.example` to `.env` in the project root:
           ```bash
           cp .env.example .env
           ```
        
        2. Edit the `.env` file and add your API keys:
           ```
           OPENAI_API_KEY=your_openai_api_key_here
           PINECONE_API_KEY=your_pinecone_api_key_here
           PINECONE_ENVIRONMENT=your_pinecone_environment_here
           ```
        
        3. Restart the application
        
        #### Option 2: Using Environment Variables (Recommended for production)
        
        Set environment variables before running the application:
        
        ```bash
        export OPENAI_API_KEY="your_openai_api_key_here"
        export PINECONE_API_KEY="your_pinecone_api_key_here"
        export PINECONE_ENVIRONMENT="your_pinecone_environment_here"
        ```
        
        #### Getting API Keys
        
        **OpenAI:**
        1. Go to https://platform.openai.com/
        2. Sign up or log in
        3. Navigate to API Keys section
        4. Create a new API key
        
        **Pinecone:**
        1. Go to https://www.pinecone.io/
        2. Sign up or log in
        3. Create a new project
        4. Get your API key and environment from the dashboard
        """)
    
    st.markdown("---")
    
    # RAG Configuration
    st.markdown("### ⚙️ RAG Configuration")
    
    st.markdown(f"""
    - **Top K Results:** {config.TOP_K_RESULTS} documents
    - **Similarity Threshold:** {config.SIMILARITY_THRESHOLD}
    - **Embedding Model:** text-embedding-ada-002
    """)
    
    st.markdown("---")
    
    # Application Configuration
    st.markdown("### 🎨 Application Configuration")
    
    st.markdown(f"""
    - **Title:** {config.APP_TITLE}
    - **Description:** {config.APP_DESCRIPTION}
    - **Default Language:** {config.DEFAULT_LANGUAGE}
    - **Supported Languages:** {', '.join([f"{name} ({code})" for code, name in config.SUPPORTED_LANGUAGES.items()])}
    """)
    
    st.markdown("---")
    
    # Data Storage
    st.markdown("### 💾 Data Storage")
    
    st.markdown(f"""
    - **Chat History:** `{config.CHAT_HISTORY_FILE}`
    - **Feedback Data:** `{config.FEEDBACK_FILE}`
    """)
    
    # Show feedback statistics
    from src.utils.storage import storage_manager
    
    feedback_stats = storage_manager.get_feedback_stats()
    
    if feedback_stats["total_feedback"] > 0:
        st.markdown("#### Feedback Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Feedback", feedback_stats["total_feedback"])
        
        with col2:
            st.metric("👍 Positive", feedback_stats["positive"])
        
        with col3:
            st.metric("👎 Negative", feedback_stats["negative"])
        
        st.progress(feedback_stats["positive_rate"])
        st.caption(f"Positive Rate: {feedback_stats['positive_rate']:.1%}")
    
    st.markdown("---")
    
    # Advanced Actions
    st.markdown("### 🛠️ Advanced Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reinitialize RAG Pipeline", help="Reconnect to Pinecone and OpenAI"):
            with st.spinner("Reinitializing..."):
                try:
                    from src.utils.rag_pipeline import RAGPipeline
                    rag = RAGPipeline()
                    if rag.initialize_index():
                        st.session_state.rag_pipeline = rag
                        st.success("✅ Pipeline reinitialized successfully!")
                    else:
                        st.error("❌ Failed to initialize pipeline")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("🗑️ Clear All Chat History", help="Delete all stored conversations"):
            if st.session_state.get("confirm_clear"):
                count = storage_manager.clear_chat_history()
                st.success(f"✅ Cleared {count} messages")
                st.session_state.messages = []
                st.session_state.confirm_clear = False
            else:
                st.warning("⚠️ Click again to confirm")
                st.session_state.confirm_clear = True
    
    st.markdown("---")
    
    # About Section
    with st.expander("ℹ️ About This Application"):
        st.markdown("""
        ### CMU-Africa Information Assistant
        
        **Version:** 1.0.0
        
        **Description:**
        A Retrieval Augmented Generation (RAG) application designed to provide accurate information about CMU-Africa.
        
        **Features:**
        - 💬 Interactive chat interface
        - 🔍 Semantic search using Pinecone
        - 🤖 AI responses powered by OpenAI GPT-4-mini
        - 📚 Knowledge base management
        - 🌐 Multi-language support (English, French)
        - 👍👎 User feedback system
        - 📊 Admin panel for content management
        
        **Technology Stack:**
        - Streamlit
        - OpenAI API (GPT-4-mini + Embeddings)
        - Pinecone Vector Database
        - Python 3.9+
        
        **Deployment:**
        - Domain: campuslink.apps.cximmersion.com
        
        ---
        
        Built with ❤️ for CMU-Africa
        """)
