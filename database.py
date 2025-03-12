from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Get MongoDB connection details from environment variables
            mongo_user = os.getenv("MONGO_USER", "doadmin")
            mongo_password = os.getenv("MONGO_PASSWORD", "t460JQE13wbMl985")
            mongo_host = os.getenv("MONGO_HOST", "db-mongodb-blr1-70752-7f07ae90.mongo.ondigitalocean.com")
            mongo_db = os.getenv("MONGO_DB", "admin")
            
            # Construct the connection string using environment variables
            self.mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/{mongo_db}?tls=true&authSource=admin"
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[mongo_db]
            self.contact_collection = self.db['contact_submissions']

    async def connect(self):
        """Verify database connection"""
        try:
            await self.client.admin.command('ping')
            print(f"Connected to MongoDB: {self.db.name}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    async def close(self):
        """Close connection"""
        try:
            self.client.close()
            print("MongoDB connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

# Initialize connection and expose database
database = DatabaseConnection()

# Export the collection directly so it can be imported
contact_collection = database.contact_collection