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
        'hotel_name': 'Grand Plaza Hotel',
        'location': 'New York City, USA',
        'star_rating': 5,
        'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant', 'Gym', 'Business Center'],
        'year_opened': 2010,
        'rooms_available': 200,
        'has_parking': True
    },
    {
        'hotel_id': 2,
        'hotel_name': 'Seaside Resort & Spa',
        'location': 'Miami Beach, USA',
        'star_rating': 4,
        'amenities': ['WiFi', 'Beach Access', 'Pool', 'Spa', 'Restaurant'],
        'year_opened': 2015,
        'rooms_available': 150,
        'has_parking': True
    },
    {
        'hotel_id': 3,
        'hotel_name': 'Mountain View Lodge',
        'location': 'Denver, USA',
        'star_rating': 4,
        'amenities': ['WiFi', 'Ski Access', 'Spa', 'Restaurant', 'Fireplace'],
        'year_opened': 2018,
        'rooms_available': 100,
        'has_parking': True
    },
    {
        'hotel_id': 4,
        'hotel_name': 'City Center Hotel',
        'location': 'Chicago, USA',
        'star_rating': 4,
        'amenities': ['WiFi', 'Restaurant', 'Business Center', 'Gym'],
        'year_opened': 2012,
        'rooms_available': 180,
        'has_parking': False
    },
    {
        'hotel_id': 5,
        'hotel_name': 'Pacific Paradise Resort',
        'location': 'Los Angeles, USA',
        'star_rating': 5,
        'amenities': ['WiFi', 'Pool', 'Beach Access', 'Spa', 'Restaurant', 'Tennis Court'],
        'year_opened': 2019,
        'rooms_available': 250,
        'has_parking': True
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