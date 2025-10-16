"""
Admin Panel for CMU-Africa Information Assistant
"""
import streamlit as st
import json
import pandas as pd
from datetime import datetime
from src.utils.config import Config
from src.utils.i18n import get_text, set_language
from src.components.rag_pipeline import RAGPipeline
from src.components.feedback_handler import FeedbackHandler

# Page configuration
st.set_page_config(
    page_title="Admin Panel - CMU-Africa Assistant",
    page_icon="🔧",
    layout="wide"
)

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None

if 'feedback_handler' not in st.session_state:
    st.session_state.feedback_handler = FeedbackHandler()

if 'language' not in st.session_state:
    st.session_state.language = 'en'

set_language(st.session_state.language)

st.title(get_text("admin_panel"))

# Check if RAG pipeline is initialized
if not st.session_state.rag_pipeline:
    st.warning("⚠️ Please configure your API keys in the main app first.")
    if st.button("Go to Main App"):
        st.switch_page("app.py")
    st.stop()

# Tabs for different admin functions
tab1, tab2, tab3 = st.tabs([
    "📚 " + get_text("knowledge_base"),
    "📊 " + get_text("view_feedback"),
    "📈 Analytics"
])

# Tab 1: Knowledge Base Management
with tab1:
    st.header(get_text("knowledge_base"))
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(get_text("add_document"))
        
        with st.form("add_document_form"):
            doc_id = st.text_input("Document ID", value=f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            doc_title = st.text_input(get_text("document_title"))
            doc_category = st.selectbox(
                "Category",
                ["Academic Programs", "Transportation", "Campus Facilities", "Faculty", "Student Life", 
                 "Admissions", "Career Services", "Contact", "General"]
            )
            doc_content = st.text_area(get_text("document_content"), height=200)
            doc_keywords = st.text_input("Keywords (comma-separated)")
            
            submit_button = st.form_submit_button(get_text("upload_button"))
            
            if submit_button:
                if doc_title and doc_content:
                    try:
                        keywords = [k.strip() for k in doc_keywords.split(",") if k.strip()]
                        success = st.session_state.rag_pipeline.add_document(
                            doc_id=doc_id,
                            title=doc_title,
                            content=doc_content,
                            category=doc_category,
                            keywords=keywords
                        )
                        if success:
                            st.success(f"✅ Document '{doc_title}' added successfully!")
                        else:
                            st.error("Failed to add document.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill in all required fields.")
    
    with col2:
        st.subheader("📊 Knowledge Base Statistics")
        
        try:
            stats = st.session_state.rag_pipeline.get_index_stats()
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Documents", stats.get('total_vectors', 0))
            with col_b:
                st.metric("Dimension", stats.get('dimension', 0))
            
            st.info(f"Index Fullness: {stats.get('index_fullness', 0):.2%}")
        except Exception as e:
            st.error(f"Could not load statistics: {str(e)}")
    
    st.divider()
    
    # Bulk upload section
    st.subheader("📤 Bulk Upload Documents")
    
    uploaded_file = st.file_uploader("Upload JSON file with documents", type=['json'])
    
    if uploaded_file is not None:
        try:
            documents = json.load(uploaded_file)
            
            st.write(f"Found {len(documents)} documents in file:")
            
            # Preview documents
            df = pd.DataFrame(documents)
            st.dataframe(df[['title', 'category', 'id']].head(10), use_container_width=True)
            
            if st.button("Upload All Documents", type="primary"):
                with st.spinner("Uploading documents..."):
                    success = st.session_state.rag_pipeline.index_documents(documents)
                    if success:
                        st.success(f"✅ Successfully uploaded {len(documents)} documents!")
                    else:
                        st.error("Failed to upload documents.")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    st.divider()
    
    # Delete documents section
    st.subheader("🗑️ Delete Document")
    
    with st.form("delete_document_form"):
        delete_doc_id = st.text_input("Enter Document ID to delete")
        delete_button = st.form_submit_button("Delete Document", type="secondary")
        
        if delete_button:
            if delete_doc_id:
                try:
                    success = st.session_state.rag_pipeline.delete_document(delete_doc_id)
                    if success:
                        st.success(f"✅ Document '{delete_doc_id}' deleted successfully!")
                    else:
                        st.error("Failed to delete document.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a document ID.")

# Tab 2: Feedback Management
with tab2:
    st.header(get_text("view_feedback"))
    
    # Feedback statistics
    st.subheader(get_text("feedback_stats"))
    
    try:
        stats = st.session_state.feedback_handler.get_feedback_statistics()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👍 Positive", stats.get('positive', 0))
        with col2:
            st.metric("👎 Negative", stats.get('negative', 0))
        with col3:
            total = stats.get('positive', 0) + stats.get('negative', 0)
            satisfaction = (stats.get('positive', 0) / total * 100) if total > 0 else 0
            st.metric("😊 Satisfaction", f"{satisfaction:.1f}%")
    except Exception as e:
        st.error(f"Could not load statistics: {str(e)}")
    
    st.divider()
    
    # All feedback
    st.subheader("📝 Recent Feedback")
    
    try:
        feedback_list = st.session_state.feedback_handler.get_all_feedback()
        
        if feedback_list:
            df = pd.DataFrame(feedback_list)
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox(
                    "Filter by type",
                    ["All", "positive", "negative"]
                )
            with col2:
                limit = st.slider("Number of records", 10, 100, 50)
            
            # Apply filters
            if filter_type != "All":
                df = df[df['feedback_type'] == filter_type]
            
            df = df.head(limit)
            
            # Display feedback
            st.dataframe(
                df[['timestamp', 'feedback_type', 'message_content', 'comment']],
                use_container_width=True,
                hide_index=True
            )
            
            # Export option
            if st.button("📥 Export Feedback as CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No feedback records yet.")
    except Exception as e:
        st.error(f"Could not load feedback: {str(e)}")

# Tab 3: Analytics
with tab3:
    st.header("📈 Analytics Dashboard")
    
    st.info("🚧 Analytics features coming soon!")
    
    st.markdown("""
    ### Planned Features:
    - 📊 Usage statistics and trends
    - 🔍 Most common queries
    - ⏱️ Response time metrics
    - 👥 User engagement metrics
    - 📈 Knowledge base coverage analysis
    - 🎯 Query success rate
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>CMU-Africa Information Assistant - Admin Panel</p>
</div>
""", unsafe_allow_html=True)
