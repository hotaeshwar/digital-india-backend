from motor.motor_asyncio import AsyncIOMotorClient

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Using the DigitalOcean MongoDB connection string instead of localhost
            self.mongo_uri = "mongodb+srv://doadmin:t460JQE13wbMl985@db-mongodb-blr1-70752-7f07ae90.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client["admin"]
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
