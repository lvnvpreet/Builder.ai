"""
Database connection and initialization
"""

from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global database client
client: AsyncIOMotorClient = None
database = None


async def init_database():
    """Initialize MongoDB connection"""
    global client, database
    
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        database = client[settings.MONGODB_DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        # Set database to None so the app can still run without DB
        database = None
        client = None


async def create_indexes():
    """Create necessary database indexes"""
    try:
        # Users collection indexes
        await database.users.create_index("email", unique=True)
        
        # Websites collection indexes
        await database.websites.create_index("user_id")
        await database.websites.create_index("created_at")
        
        # Generations collection indexes
        await database.generations.create_index("website_id")
        await database.generations.create_index("created_at")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")


async def close_database():
    """Close database connection"""
    global client
    if client:
        client.close()
        logger.info("Database connection closed")


def get_database():
    """Get database instance"""
    return database
