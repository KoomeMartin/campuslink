
"""
Database utilities for chat history and feedback
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class ChatHistoryDB:
    """Manages chat history storage"""
    
    def __init__(self, db_path: str = "data/chat_history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                context TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
            )
        """)
        conn.commit()
        conn.close()
    
    def create_session(self, session_id: str):
        """Create a new chat session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO chat_sessions (session_id) VALUES (?)",
            (session_id,)
        )
        conn.commit()
        conn.close()
    
    def add_message(self, session_id: str, role: str, content: str, context: Optional[str] = None):
        """Add a message to the chat history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content, context) VALUES (?, ?, ?, ?)",
            (session_id, role, content, context)
        )
        cursor.execute(
            "UPDATE chat_sessions SET last_updated = CURRENT_TIMESTAMP WHERE session_id = ?",
            (session_id,)
        )
        conn.commit()
        conn.close()
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get messages for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """SELECT role, content, context, timestamp 
               FROM messages 
               WHERE session_id = ? 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            (session_id, limit)
        )
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "role": row[0],
                "content": row[1],
                "context": row[2],
                "timestamp": row[3]
            })
        conn.close()
        return list(reversed(messages))
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all chat sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, created_at, last_updated FROM chat_sessions ORDER BY last_updated DESC"
        )
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                "session_id": row[0],
                "created_at": row[1],
                "last_updated": row[2]
            })
        conn.close()
        return sessions
    
    def delete_session(self, session_id: str):
        """Delete a chat session and its messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()


class FeedbackDB:
    """Manages user feedback storage"""
    
    def __init__(self, db_path: str = "data/feedback.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_content TEXT,
                feedback_type TEXT,
                comment TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_feedback(self, session_id: str, message_content: str, 
                     feedback_type: str, comment: Optional[str] = None):
        """Add user feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (session_id, message_content, feedback_type, comment) VALUES (?, ?, ?, ?)",
            (session_id, message_content, feedback_type, comment)
        )
        conn.commit()
        conn.close()
    
    def get_all_feedback(self) -> List[Dict]:
        """Get all feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, session_id, message_content, feedback_type, comment, timestamp FROM feedback ORDER BY timestamp DESC"
        )
        feedback_list = []
        for row in cursor.fetchall():
            feedback_list.append({
                "id": row[0],
                "session_id": row[1],
                "message_content": row[2],
                "feedback_type": row[3],
                "comment": row[4],
                "timestamp": row[5]
            })
        conn.close()
        return feedback_list
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT feedback_type, COUNT(*) FROM feedback GROUP BY feedback_type")
        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = row[1]
        conn.close()
        return stats
