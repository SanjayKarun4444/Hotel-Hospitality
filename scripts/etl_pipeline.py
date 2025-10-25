"""
etl_pipeline.py
ETL Pipeline that extracts data from multiple sources:
1. CSV files (guests, rooms, bookings)
2. MongoDB (hotels)
3. Python-generated data (date dimension)

Then transforms and loads into MySQL data mart.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=" * 60)
print("Starting ETL Pipeline")
print("=" * 60)

# ============================================================================
# EXTRACT Phase
# ============================================================================
print("\n[EXTRACT] Loading data from multiple sources...")

# Source 1: Extract from CSV files (File System)
print("  ✓ Extracting from CSV files...")
guests_df = pd.read_csv('data/csv/guests.csv')
rooms_df = pd.read_csv('data/csv/rooms.csv')
bookings_df = pd.read_csv('data/csv/bookings.csv')
print(f"    - Loaded {len(guests_df)} guests")
print(f"    - Loaded {len(rooms_df)} rooms")
print(f"    - Loaded {len(bookings_df)} bookings")

# Source 2: Extract from MongoDB (NoSQL Database)
print("  ✓ Extracting from MongoDB...")
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['hotel_source_db']
hotels_collection = mongo_db['hotels']

# Convert MongoDB documents to DataFrame
hotels_data = list(hotels_collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
hotels_df = pd.DataFrame(hotels_data)

# Keep only required columns for data mart
hotels_df = hotels_df[['hotel_id', 'hotel_name', 'location', 'star_rating']]
print(f"    - Loaded {len(hotels_df)} hotels from MongoDB")

mongo_client.close()

# Source 3: Generate Date dimension (Programmatic/In-memory source)
print("  ✓ Generating date dimension...")
dates_df = pd.DataFrame({
    'date_id': [1, 2, 3],
    'date': ['2023-01-15', '2023-02-20', '2023-03-25'],
    'day': [15, 20, 25],
    'month': [1, 2, 3],
    'year': [2023, 2023, 2023],
    'quarter': [1, 1, 1],
    'day_name': ['Sunday', 'Monday', 'Saturday'],
    'month_name': ['January', 'February', 'March']
})
print(f"    - Generated {len(dates_df)} date records")

# ============================================================================
# TRANSFORM Phase
# ============================================================================
print("\n[TRANSFORM] Transforming data...")

# Transformation 1: Calculate total_amount for bookings
bookings_df['total_amount'] = bookings_df['nights_stayed'] * bookings_df['price_per_night']
print("  ✓ Calculated total_amount (nights_stayed × price_per_night)")

# Transformation 2: Drop unnecessary columns (modify column count)
bookings_df = bookings_df.drop(columns=['price_per_night'])
print("  ✓ Removed price_per_night column from bookings")

# Transformation 3: Data validation
print("  ✓ Validating data integrity...")
assert bookings_df['guest_id'].isin(guests_df['guest_id']).all(), "Invalid guest_id references"
assert bookings_df['room_id'].isin(rooms_df['room_id']).all(), "Invalid room_id references"
assert bookings_df['hotel_id'].isin(hotels_df['hotel_id']).all(), "Invalid hotel_id references"
print("    - All foreign key references validated")

# ============================================================================
# LOAD Phase
# ============================================================================
print("\n[LOAD] Loading data into MySQL data mart...")

# Create MySQL connection using environment variables
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_port = os.getenv('MYSQL_PORT', '3306')
mysql_database = os.getenv('MYSQL_DATABASE')

# Build connection string
connection_string = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'
engine = create_engine(connection_string)

# Drop existing tables and recreate schema
print("  ✓ Preparing database...")
with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    conn.execute(text("DROP TABLE IF EXISTS bookings;"))
    conn.execute(text("DROP TABLE IF EXISTS guest;"))
    conn.execute(text("DROP TABLE IF EXISTS room;"))
    conn.execute(text("DROP TABLE IF EXISTS hotel;"))
    conn.execute(text("DROP TABLE IF EXISTS date;"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    conn.commit()
    print("    - Dropped existing tables")

# Read and execute schema.sql
print("  ✓ Creating tables from schema...")
with open('scripts/schema.sql', 'r') as f:
    schema_sql = f.read()
    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
    with engine.connect() as conn:
        for stmt in statements:
            if stmt:
                conn.execute(text(stmt))
        conn.commit()
print("    - Tables created successfully")

# Load data into tables (dimensions first, then fact table)
print("  ✓ Loading data into tables...")
dates_df.to_sql('date', engine, if_exists='append', index=False)
print(f"    - Loaded {len(dates_df)} records into date dimension")

hotels_df.to_sql('hotel', engine, if_exists='append', index=False)
print(f"    - Loaded {len(hotels_df)} records into hotel dimension")

guests_df.to_sql('guest', engine, if_exists='append', index=False)
print(f"    - Loaded {len(guests_df)} records into guest dimension")

rooms_df.to_sql('room', engine, if_exists='append', index=False)
print(f"    - Loaded {len(rooms_df)} records into room dimension")

bookings_df.to_sql('bookings', engine, if_exists='append', index=False)
print(f"    - Loaded {len(bookings_df)} records into bookings fact table")

# ============================================================================
# VERIFICATION
# ============================================================================
print("\n[VERIFY] Checking data mart contents...")
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) as count FROM bookings"))
    count = result.fetchone()[0]
    print(f"  ✓ Bookings fact table contains {count} records")
    
    result = conn.execute(text("SELECT COUNT(*) as count FROM hotel"))
    count = result.fetchone()[0]
    print(f"  ✓ Hotel dimension contains {count} records")

print("\n" + "=" * 60)
print("ETL Pipeline completed successfully!")
print("=" * 60)
print("\nYou can now run queries.sql to verify the data mart functionality.")