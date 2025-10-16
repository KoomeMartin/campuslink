"""
Admin panel for knowledge base management
"""
import streamlit as st
import json
from src.utils.translations import get_text, format_text


def show():
    """Display the admin panel"""
    lang = st.session_state.language
    
    st.markdown(f"# {get_text('admin_title', lang)}")
    
    # Check if RAG pipeline is initialized
    if st.session_state.rag_pipeline is None:
        st.error(get_text("error_api_keys", lang))
        st.info("👉 Please configure your API keys in the Settings page.")
        return
    
    rag = st.session_state.rag_pipeline
    
    # Tabs for different admin functions
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("admin_add_doc", lang),
        get_text("admin_bulk_upload", lang),
        get_text("admin_index_stats", lang),
        "Delete Document"
    ])
    
    # Tab 1: Add Single Document
    with tab1:
        st.markdown(f"### ➕ {get_text('admin_add_doc', lang)}")
        
        with st.form("add_document_form"):
            doc_id = st.text_input(get_text("doc_id", lang), placeholder="e.g., prog_005")
            doc_title = st.text_input(get_text("doc_title", lang), placeholder="e.g., PhD Programs")
            doc_category = st.text_input(get_text("doc_category", lang), placeholder="e.g., Academic Programs")
            doc_content = st.text_area(
                get_text("doc_content", lang),
                placeholder="Enter the document content here...",
                height=200
            )
            doc_lang = st.selectbox(
                get_text("doc_language", lang),
                options=["en", "fr"],
                format_func=lambda x: "English" if x == "en" else "Français"
            )
            
            submit_button = st.form_submit_button(get_text("doc_add_button", lang), type="primary")
            
            if submit_button:
                if not doc_id or not doc_title or not doc_content:
                    st.error("Please fill in all required fields (ID, Title, Content)")
                else:
                    with st.spinner("Adding document..."):
                        metadata = {
                            "title": doc_title,
                            "category": doc_category,
                            "language": doc_lang
                        }
                        
                        success = rag.upsert_document(doc_id, doc_content, metadata)
                        
                        if success:
                            st.success(get_text("doc_added", lang))
                        else:
                            st.error(get_text("doc_error", lang))
    
    # Tab 2: Bulk Upload
    with tab2:
        st.markdown(f"### 📤 {get_text('admin_bulk_upload', lang)}")
        st.info(get_text("bulk_upload_info", lang))
        
        # Show sample format
        with st.expander("📋 Sample JSON Format"):
            sample_format = [
                {
                    "id": "doc_001",
                    "title": "Document Title",
                    "category": "Category Name",
                    "content": "Document content goes here...",
                    "metadata": {
                        "language": "en",
                        "last_updated": "2024-10-01"
                    }
                }
            ]
            st.json(sample_format)
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=["json"],
            help="Upload a JSON file containing an array of documents"
        )
        
        if uploaded_file is not None:
            try:
                # Read and parse JSON
                content = uploaded_file.read().decode("utf-8")
                documents = json.loads(content)
                
                if not isinstance(documents, list):
                    st.error("JSON file must contain an array of documents")
                else:
                    st.success(f"✅ Loaded {len(documents)} documents from file")
                    
                    # Preview first few documents
                    with st.expander(f"👀 Preview (first 3 documents)"):
                        for doc in documents[:3]:
                            st.json(doc)
                    
                    if st.button(get_text("bulk_upload_button", lang), type="primary"):
                        with st.spinner(f"Uploading {len(documents)} documents..."):
                            success_count, fail_count = rag.upsert_documents_batch(documents)
                            
                            if fail_count == 0:
                                st.success(f"✅ Successfully uploaded all {success_count} documents!")
                            else:
                                st.warning(format_text("bulk_success", lang, success_count, fail_count))
            
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {str(e)}")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    # Tab 3: Index Statistics
    with tab3:
        st.markdown(f"### 📊 {get_text('admin_index_stats', lang)}")
        
        if st.button("🔄 Refresh Statistics"):
            st.rerun()
        
        stats = rag.get_index_stats()
        
        if "error" in stats:
            st.error(f"Error fetching stats: {stats['error']}")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    get_text("stats_total", lang),
                    stats.get("total_vectors", 0)
                )
            
            with col2:
                st.metric(
                    get_text("stats_dimension", lang),
                    stats.get("dimension", 0)
                )
            
            with col3:
                fullness = stats.get("index_fullness", 0)
                st.metric(
                    get_text("stats_fullness", lang),
                    f"{fullness:.2%}"
                )
        
        # Display sample queries
        st.markdown("### 🔍 Test Search")
        test_query = st.text_input("Enter a test query", placeholder="e.g., What shuttle services are available?")
        
        if test_query:
            with st.spinner("Searching..."):
                results = rag.search(test_query)
                
                if results:
                    st.success(f"Found {len(results)} relevant documents")
                    for i, doc in enumerate(results):
                        with st.expander(f"Result {i+1}: {doc['title']} (Score: {doc['score']:.3f})"):
                            st.markdown(f"**Category:** {doc['category']}")
                            st.markdown(f"**Content:** {doc['text'][:300]}...")
                else:
                    st.info("No relevant documents found")
    
    # Tab 4: Delete Document
    with tab4:
        st.markdown("### 🗑️ Delete Document")
        st.warning("⚠️ This action cannot be undone!")
        
        with st.form("delete_document_form"):
            delete_id = st.text_input("Document ID to delete", placeholder="e.g., doc_001")
            
            confirm = st.checkbox("I understand this action is permanent")
            delete_button = st.form_submit_button("Delete Document", type="secondary")
            
            if delete_button:
                if not delete_id:
                    st.error("Please enter a document ID")
                elif not confirm:
                    st.error("Please confirm the deletion")
                else:
                    with st.spinner("Deleting document..."):
                        success = rag.delete_document(delete_id)
                        
                        if success:
                            st.success(f"✅ Document '{delete_id}' deleted successfully")
                        else:
                            st.error(f"❌ Failed to delete document '{delete_id}'")
