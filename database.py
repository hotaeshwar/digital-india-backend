from motor.motor_asyncio import AsyncIOMotorClient

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, mongo_uri: str = None, db_name: str = "contact_db"):
        if not self._initialized:
            self._initialized = True
            self.mongo_uri = mongo_uri or "mongodb://localhost:27017/"
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[db_name]
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

# Initialize connection and expose collection
database = DatabaseConnection()
contact_collection = database.contact_collection  # Add this line