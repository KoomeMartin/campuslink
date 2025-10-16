
"""
Feedback handling component
"""
from typing import Optional
from src.utils.database import FeedbackDB

class FeedbackHandler:
    """Handles user feedback collection and storage"""
    
    def __init__(self):
        self.db = FeedbackDB()
    
    def record_feedback(self, session_id: str, message_content: str, 
                       feedback_type: str, comment: Optional[str] = None):
        """Record user feedback"""
        self.db.add_feedback(session_id, message_content, feedback_type, comment)
    
    def get_all_feedback(self):
        """Get all feedback records"""
        return self.db.get_all_feedback()
    
    def get_feedback_statistics(self):
        """Get feedback statistics"""
        return self.db.get_feedback_stats()
