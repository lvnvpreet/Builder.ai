"""
Database package initialization
"""

from .connection import init_database, close_database, get_database

__all__ = ["init_database", "close_database", "get_database"]
