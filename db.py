import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the .env file
MONGODB_URI = os.getenv('MONGODB_URI')

# Create a MongoDB client
client = MongoClient(MONGODB_URI)

# Access a specific database
ArtKartDB = client['artkart']
