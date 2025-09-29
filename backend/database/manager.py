"""
Database connection and management utilities.
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from ..config.settings import Config

class DatabaseManager:
    """Manages database connections and provides query utilities."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = True) -> Optional[List[Dict[str, Any]]]:
        """Execute a query and return results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            elif fetch_all:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return None
    
    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Execute a query with multiple parameter sets."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
    
    def execute_script(self, script: str) -> None:
        """Execute a SQL script."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(script)
            conn.commit()

# Global database manager instance
db_manager = DatabaseManager()
