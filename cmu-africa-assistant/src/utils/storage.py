
"""
Storage utilities for chat history and feedback
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class StorageManager:
    """Manage persistent storage for chat history and feedback"""
    
    def __init__(self, history_file: str = "data/chat_history.json", 
                 feedback_file: str = "data/feedback.json"):
        """
        Initialize storage manager
        
        Args:
            history_file: Path to chat history file
            feedback_file: Path to feedback file
        """
        self.history_file = history_file
        self.feedback_file = feedback_file
        
        # Ensure data directory exists
        Path(history_file).parent.mkdir(parents=True, exist_ok=True)
        Path(feedback_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(history_file):
            self._write_json(history_file, [])
        if not os.path.exists(feedback_file):
            self._write_json(feedback_file, [])
    
    def _read_json(self, filepath: str) -> List:
        """Read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []
    
    def _write_json(self, filepath: str, data: List):
        """Write JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
    
    # Chat History Methods
    
    def add_chat_message(self, user_id: str, query: str, response: str, 
                        sources: List[Dict], language: str = "en") -> str:
        """
        Add a chat message to history
        
        Args:
            user_id: User identifier
            query: User query
            response: Assistant response
            sources: Retrieved source documents
            language: Message language
            
        Returns:
            Message ID
        """
        history = self._read_json(self.history_file)
        
        message_id = f"msg_{datetime.now().timestamp()}"
        message = {
            "id": message_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "sources": sources,
            "language": language,
            "feedback": None  # Will be updated when user provides feedback
        }
        
        history.append(message)
        self._write_json(self.history_file, history)
        
        return message_id
    
    def get_chat_history(self, user_id: Optional[str] = None, 
                         limit: Optional[int] = None) -> List[Dict]:
        """
        Get chat history
        
        Args:
            user_id: Filter by user ID (optional)
            limit: Maximum number of messages to return (optional)
            
        Returns:
            List of chat messages
        """
        history = self._read_json(self.history_file)
        
        # Filter by user if specified
        if user_id:
            history = [msg for msg in history if msg.get("user_id") == user_id]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Limit results if specified
        if limit:
            history = history[:limit]
        
        return history
    
    def clear_chat_history(self, user_id: Optional[str] = None) -> int:
        """
        Clear chat history
        
        Args:
            user_id: Clear only for specific user (optional)
            
        Returns:
            Number of messages deleted
        """
        history = self._read_json(self.history_file)
        original_count = len(history)
        
        if user_id:
            history = [msg for msg in history if msg.get("user_id") != user_id]
        else:
            history = []
        
        self._write_json(self.history_file, history)
        
        return original_count - len(history)
    
    def get_message_by_id(self, message_id: str) -> Optional[Dict]:
        """Get a specific message by ID"""
        history = self._read_json(self.history_file)
        for msg in history:
            if msg.get("id") == message_id:
                return msg
        return None
    
    # Feedback Methods
    
    def add_feedback(self, message_id: str, feedback_type: str, 
                     comment: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        """
        Add feedback for a message
        
        Args:
            message_id: Message identifier
            feedback_type: 'positive' or 'negative'
            comment: Optional feedback comment
            user_id: User identifier
            
        Returns:
            True if successful, False otherwise
        """
        # Update chat history with feedback
        history = self._read_json(self.history_file)
        updated = False
        
        for msg in history:
            if msg.get("id") == message_id:
                msg["feedback"] = {
                    "type": feedback_type,
                    "comment": comment,
                    "timestamp": datetime.now().isoformat()
                }
                updated = True
                break
        
        if updated:
            self._write_json(self.history_file, history)
        
        # Add to feedback file
        feedback_data = self._read_json(self.feedback_file)
        feedback_entry = {
            "message_id": message_id,
            "user_id": user_id,
            "feedback_type": feedback_type,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        feedback_data.append(feedback_entry)
        self._write_json(self.feedback_file, feedback_data)
        
        return True
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        feedback_data = self._read_json(self.feedback_file)
        
        total = len(feedback_data)
        positive = sum(1 for f in feedback_data if f.get("feedback_type") == "positive")
        negative = sum(1 for f in feedback_data if f.get("feedback_type") == "negative")
        
        return {
            "total_feedback": total,
            "positive": positive,
            "negative": negative,
            "positive_rate": positive / total if total > 0 else 0
        }
    
    def get_all_feedback(self) -> List[Dict]:
        """Get all feedback entries"""
        return self._read_json(self.feedback_file)


# Global storage manager instance
storage_manager = StorageManager()
