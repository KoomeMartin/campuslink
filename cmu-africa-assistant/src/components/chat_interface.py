
"""
Chat interface component
"""
from typing import List, Dict
from src.utils.database import ChatHistoryDB

class ChatInterface:
    """Manages chat sessions and history"""
    
    def __init__(self):
        self.db = ChatHistoryDB()
    
    def create_session(self, session_id: str):
        """Create a new chat session"""
        self.db.create_session(session_id)
    
    def add_message(self, session_id: str, role: str, content: str, context: str = None):
        """Add a message to the chat history"""
        self.db.add_message(session_id, role, content, context)
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get messages for a session"""
        return self.db.get_session_messages(session_id, limit)
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all chat sessions"""
        return self.db.get_all_sessions()
    
    def delete_session(self, session_id: str):
        """Delete a chat session"""
        self.db.delete_session(session_id)
