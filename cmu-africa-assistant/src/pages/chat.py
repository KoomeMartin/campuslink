"""
Chat interface page
"""
import streamlit as st
from datetime import datetime
from src.utils.storage import storage_manager
from src.utils.translations import get_text


def show():
    """Display the chat interface"""
    lang = st.session_state.language
    
    # Header
    st.markdown(f'<div class="main-header">{get_text("app_title", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{get_text("app_description", lang)}</div>', unsafe_allow_html=True)
    
    # Check if RAG pipeline is initialized
    if st.session_state.rag_pipeline is None:
        st.error(get_text("error_api_keys", lang))
        st.info("👉 Please configure your API keys in the Settings page.")
        return
    
    # Chat container
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            # User message
            with st.container():
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["query"]}</div>', 
                          unsafe_allow_html=True)
            
            # Assistant message
            with st.container():
                st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong><br>{message["response"]}</div>', 
                          unsafe_allow_html=True)
                
                # Show sources if available
                if message.get("sources"):
                    with st.expander(f"📚 {get_text('sources_title', lang)} ({len(message['sources'])})"):
                        for i, source in enumerate(message["sources"]):
                            st.markdown(f"""
                            <div class="source-card">
                                <strong>{get_text('source', lang)} {i+1}:</strong> {source.get('title', 'N/A')}<br>
                                <strong>{get_text('category', lang)}:</strong> {source.get('category', 'N/A')}<br>
                                <strong>{get_text('relevance', lang)}:</strong> {source.get('score', 0):.2f}<br>
                                <small>{source.get('text', '')[:200]}...</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Feedback section
                feedback_key = f"feedback_{idx}"
                if message.get("message_id") and not message.get("feedback_given"):
                    st.markdown(f'<div class="feedback-section">', unsafe_allow_html=True)
                    st.markdown(f"**{get_text('feedback_title', lang)}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(get_text("feedback_positive", lang), key=f"pos_{idx}"):
                            storage_manager.add_feedback(
                                message["message_id"],
                                "positive",
                                user_id=st.session_state.user_id
                            )
                            st.session_state.messages[idx]["feedback_given"] = True
                            st.success(get_text("feedback_thankyou", lang))
                            st.rerun()
                    
                    with col2:
                        if st.button(get_text("feedback_negative", lang), key=f"neg_{idx}"):
                            storage_manager.add_feedback(
                                message["message_id"],
                                "negative",
                                user_id=st.session_state.user_id
                            )
                            st.session_state.messages[idx]["feedback_given"] = True
                            st.success(get_text("feedback_thankyou", lang))
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif message.get("feedback_given"):
                    st.success("✅ " + get_text("feedback_thankyou", lang))
                
                st.markdown("---")
    
    # Input area
    st.markdown("### 💬 " + get_text("chat_title", lang))
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_query = st.text_input(
            "Query",
            placeholder=get_text("chat_input", lang),
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button(get_text("chat_send", lang), type="primary", use_container_width=True)
    
    # Handle query submission
    if send_button and user_query:
        with st.spinner("🤔 Thinking..."):
            try:
                # Get answer from RAG pipeline
                result = st.session_state.rag_pipeline.get_answer(user_query, language=lang)
                
                # Save to chat history
                message_id = storage_manager.add_chat_message(
                    user_id=st.session_state.user_id,
                    query=user_query,
                    response=result["answer"],
                    sources=result["sources"],
                    language=lang
                )
                
                # Add to session messages
                st.session_state.messages.append({
                    "query": user_query,
                    "response": result["answer"],
                    "sources": result["sources"],
                    "message_id": message_id,
                    "feedback_given": False,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"{get_text('error_query', lang)}: {str(e)}")
    
    # Clear history button
    st.markdown("---")
    if st.button(get_text("chat_clear", lang)):
        if st.session_state.messages:
            st.session_state.messages = []
            st.success(get_text("chat_history_cleared", lang))
            st.rerun()
    
    # Load previous history on first load
    if not st.session_state.messages:
        previous_history = storage_manager.get_chat_history(
            user_id=st.session_state.user_id,
            limit=10
        )
        
        if previous_history:
            st.info(f"📜 Loaded {len(previous_history)} previous messages")
            # Reverse to show oldest first
            for msg in reversed(previous_history):
                st.session_state.messages.append({
                    "query": msg.get("query", ""),
                    "response": msg.get("response", ""),
                    "sources": msg.get("sources", []),
                    "message_id": msg.get("id"),
                    "feedback_given": msg.get("feedback") is not None,
                    "timestamp": msg.get("timestamp")
                })
