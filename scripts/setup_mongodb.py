"""
setup_mongodb.py
This script sets up MongoDB with hotel data as a source system.
Run this BEFORE running the ETL pipeline.
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)

# Create/connect to database and collection
db = client['hotel_source_db']
hotels_collection = db['hotels']

# Clear existing data
hotels_collection.delete_many({})

# Insert hotel data into MongoDB
hotels_data = [
    {
        'hotel_id': 1,
        'hotel_name': 'Grand Hotel',
        'location': 'New York',
        'star_rating': 5,
        'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant'],
        'year_opened': 2010
    },
    {
        'hotel_id': 2,
        'hotel_name': 'Ocean View',
        'location': 'Miami',
        'star_rating': 4,
        'amenities': ['WiFi', 'Beach Access', 'Bar'],
        'year_opened': 2015
    },
    {
        'hotel_id': 3,
        'hotel_name': 'Mountain Lodge',
        'location': 'Denver',
        'star_rating': 4,
        'amenities': ['WiFi', 'Ski Access', 'Fireplace'],
        'year_opened': 2018
    }
]

result = hotels_collection.insert_many(hotels_data)
print(f"✓ Inserted {len(result.inserted_ids)} hotels into MongoDB")

# Verify the data
print("\nHotels in MongoDB:")
for hotel in hotels_collection.find():
    print(f"  - {hotel['hotel_name']} ({hotel['location']}) - {hotel['star_rating']} stars")

client.close()
print("\n✓ MongoDB setup complete!")