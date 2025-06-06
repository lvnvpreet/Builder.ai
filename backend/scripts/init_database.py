"""
Database initialization script
Creates collections and indexes for the AI Website Builder
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from pathlib import Path

# Add parent directory to path to import modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.config import settings


async def init_database():
    """Initialize MongoDB database with collections and indexes"""
    try:
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        # Create collections
        print("\nCreating collections...")
        
        collections = ["users", "websites", "generations", "templates"]
        for collection_name in collections:
            try:
                await db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  Collection {collection_name} already exists")
                else:
                    print(f"❌ Failed to create collection {collection_name}: {e}")
        
        # Create indexes
        print("\nCreating indexes...")
        
        # Users collection indexes
        try:
            await db.users.create_index("email", unique=True)
            print("✅ Created unique index on users.email")
        except Exception as e:
            print(f"ℹ️  Users email index: {e}")
        
        # Websites collection indexes
        try:
            await db.websites.create_index("user_id")
            await db.websites.create_index("created_at")
            print("✅ Created indexes on websites collection")
        except Exception as e:
            print(f"ℹ️  Websites indexes: {e}")
        
        # Generations collection indexes
        try:
            await db.generations.create_index("generation_id", unique=True)
            await db.generations.create_index("created_at")
            await db.generations.create_index("status")
            print("✅ Created indexes on generations collection")
        except Exception as e:
            print(f"ℹ️  Generations indexes: {e}")
        
        # Templates collection indexes
        try:
            await db.templates.create_index("name")
            await db.templates.create_index("category")
            print("✅ Created indexes on templates collection")
        except Exception as e:
            print(f"ℹ️  Templates indexes: {e}")
        
        print("\n🎉 Database initialization completed successfully!")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    print("🤖 AI Website Builder - Database Initialization")
    print("=" * 50)
    
    asyncio.run(init_database())
