"""
CMU-Africa Information Assistant - Main Application
"""
import streamlit as st
import uuid
import json
from datetime import datetime
from src.utils.config import Config
from src.utils.i18n import get_text, set_language, get_available_languages
from src.components.rag_pipeline import RAGPipeline
from src.components.chat_interface import ChatInterface
from src.components.feedback_handler import FeedbackHandler

# Page configuration
st.set_page_config(
    page_title="CMU-Africa Information Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'language' not in st.session_state:
    st.session_state.language = 'en'

if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None

if 'chat_interface' not in st.session_state:
    st.session_state.chat_interface = ChatInterface()

if 'feedback_handler' not in st.session_state:
    st.session_state.feedback_handler = FeedbackHandler()

if 'api_keys_configured' not in st.session_state:
    st.session_state.api_keys_configured = False

if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = {}

# Apply language setting
set_language(st.session_state.language)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .feedback-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .source-box {
        background-color: #e8eaf6;
        border-left: 4px solid #3f51b5;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration and settings
with st.sidebar:
    st.header(get_text("sidebar_config"))
    
    # Language selector
    languages = get_available_languages()
    selected_lang = st.selectbox(
        get_text("sidebar_language"),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(st.session_state.language)
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        set_language(selected_lang)
        st.rerun()
    
    st.divider()
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    openai_key = st.text_input(
        get_text("sidebar_openai_key"),
        type="password",
        value=Config.OPENAI_API_KEY if Config.OPENAI_API_KEY else "",
        help="Enter your OpenAI API key"
    )
    
    pinecone_key = st.text_input(
        get_text("sidebar_pinecone_key"),
        type="password",
        value=Config.PINECONE_API_KEY if Config.PINECONE_API_KEY else "",
        help="Enter your Pinecone API key"
    )
    
    pinecone_env = st.text_input(
        get_text("sidebar_pinecone_env"),
        value=Config.PINECONE_ENVIRONMENT if Config.PINECONE_ENVIRONMENT else "",
        help="Enter your Pinecone environment (e.g., us-east-1)"
    )
    
    if st.button(get_text("sidebar_save_config"), type="primary"):
        if openai_key and pinecone_key and pinecone_env:
            try:
                # Initialize RAG pipeline
                st.session_state.rag_pipeline = RAGPipeline(
                    openai_api_key=openai_key,
                    pinecone_api_key=pinecone_key,
                    pinecone_environment=pinecone_env
                )
                
                # Load initial knowledge base
                try:
                    with open('data/cmu_africa_knowledge_base.json', 'r') as f:
                        documents = json.load(f)
                    
                    # Check if index is empty and needs initial data
                    stats = st.session_state.rag_pipeline.get_index_stats()
                    if stats.get('total_vectors', 0) == 0:
                        with st.spinner("Loading knowledge base..."):
                            st.session_state.rag_pipeline.index_documents(documents)
                        st.success("Knowledge base loaded successfully!")
                
                except Exception as e:
                    st.warning(f"Could not load initial knowledge base: {str(e)}")
                
                st.session_state.api_keys_configured = True
                st.success("✅ Configuration saved successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please fill in all API configuration fields.")
    
    st.divider()
    
    # Chat history
    st.subheader(get_text("chat_history"))
    
    if st.button(get_text("new_chat"), use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.show_feedback = {}
        st.rerun()
    
    # Display recent sessions
    sessions = st.session_state.chat_interface.get_all_sessions()
    if sessions:
        st.write("Recent Sessions:")
        for session in sessions[:5]:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(
                    f"📝 {session['session_id'][:8]}...",
                    key=f"session_{session['session_id']}",
                    use_container_width=True
                ):
                    st.session_state.session_id = session['session_id']
                    st.session_state.messages = st.session_state.chat_interface.get_session_messages(
                        session['session_id']
                    )
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{session['session_id']}"):
                    st.session_state.chat_interface.delete_session(session['session_id'])
                    st.rerun()
    
    st.divider()
    
    # Index statistics
    if st.session_state.rag_pipeline:
        st.subheader("📊 Knowledge Base Stats")
        stats = st.session_state.rag_pipeline.get_index_stats()
        st.metric("Total Documents", stats.get('total_vectors', 0))

# Main chat interface
st.title(get_text("app_title"))

# Check if API keys are configured
if not st.session_state.api_keys_configured or not st.session_state.rag_pipeline:
    st.info(get_text("error_no_config"))
    st.info("👈 Please configure your API keys in the sidebar to get started.")
    
    # Display sample questions
    st.subheader("Sample Questions You Can Ask:")
    st.markdown("""
    - 🚌 What are the shuttle bus timings?
    - 🎓 What Master's programs does CMU-Africa offer?
    - 👨‍🏫 Tell me about the faculty at CMU-Africa
    - 🏫 What facilities are available on campus?
    - 💰 Are there scholarships available?
    - 📞 How can I contact CMU-Africa?
    """)
else:
    # Display welcome message
    if not st.session_state.messages:
        st.info(get_text("welcome_message"))
        st.session_state.chat_interface.create_session(st.session_state.session_id)
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources", expanded=False):
                    for source in message["sources"]:
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>{source['title']}</strong> ({source['category']})<br>
                            <small>Relevance: {source['score']:.2f}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Feedback buttons for assistant messages
            if message["role"] == "assistant":
                feedback_key = f"feedback_{idx}"
                if feedback_key not in st.session_state.show_feedback:
                    col1, col2, col3 = st.columns([1, 1, 10])
                    with col1:
                        if st.button("👍", key=f"thumbs_up_{idx}"):
                            st.session_state.feedback_handler.record_feedback(
                                st.session_state.session_id,
                                message["content"],
                                "positive"
                            )
                            st.session_state.show_feedback[feedback_key] = True
                            st.rerun()
                    with col2:
                        if st.button("👎", key=f"thumbs_down_{idx}"):
                            st.session_state.feedback_handler.record_feedback(
                                st.session_state.session_id,
                                message["content"],
                                "negative"
                            )
                            st.session_state.show_feedback[feedback_key] = True
                            st.rerun()
                else:
                    st.success(get_text("feedback_thanks"))
    
    # Chat input
    if prompt := st.chat_input(get_text("chat_input_placeholder")):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner(get_text("thinking")):
                try:
                    # Query the RAG pipeline
                    response, contexts = st.session_state.rag_pipeline.query(
                        prompt,
                        language=st.session_state.language
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Show sources
                    if contexts:
                        with st.expander("📚 Sources", expanded=False):
                            for source in contexts:
                                st.markdown(f"""
                                <div class="source-box">
                                    <strong>{source['title']}</strong> ({source['category']})<br>
                                    <small>Relevance: {source['score']:.2f}</small>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": contexts
                    })
                    
                    # Save to database
                    st.session_state.chat_interface.add_message(
                        st.session_state.session_id,
                        "user",
                        prompt
                    )
                    st.session_state.chat_interface.add_message(
                        st.session_state.session_id,
                        "assistant",
                        response,
                        json.dumps(contexts)
                    )
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"{get_text('error_general')}: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>CMU-Africa Information Assistant | Powered by OpenAI GPT-4 & Pinecone</p>
    <p>For official information, visit <a href='https://www.africa.engineering.cmu.edu/' target='_blank'>CMU-Africa Website</a></p>
</div>
""", unsafe_allow_html=True)
