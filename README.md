# Hotel Booking Data Mart - ETL Pipeline

**DS-2002 Project 1: Midterm**  
**Author**: Sanjay Karunamoorthy 
**University of Virginia**

A dimensional data mart ETL pipeline that extracts data from CSV files, MongoDB, and programmatic sources, transforms it, and loads into a MySQL star schema for analytical queries.

---

## Project Overview

This ETL pipeline demonstrates:
- **Extract** from 3 source types: CSV files (file system), MongoDB (NoSQL), and Python-generated date dimension
- **Transform** data through calculations, column modifications, and validation
- **Load** into MySQL star schema (4 dimensions + 1 fact table)
- **Analyze** with SQL queries demonstrating JOINs and aggregations

**Business Process**: Hotel booking transactions analyzing revenue, occupancy, and booking trends.

---

## Requirements Met ✅

**Data Sources (3 types)**:
- CSV files: guests.csv, rooms.csv, bookings.csv
- MongoDB: hotels collection in hotel_source_db
- Programmatic: Date dimension with time hierarchy

**Star Schema**:
- 1 Fact table: bookings (nights_stayed, total_amount)
- 4 Dimensions: date, guest, room, hotel

**Transformations**:
- Calculate total_amount = nights_stayed × price_per_night
- Drop price_per_night column (column count modification)
- Normalize MongoDB documents to flat structure
- Validate referential integrity

**Queries** (all with JOINs + aggregations):
1. Total revenue by hotel (SUM)
2. Average stay by room type (AVG)
3. Booking trends by quarter (COUNT)

---

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- MongoDB Atlas account (free tier)

### Setup

1. **Clone and install dependencies**:
```bash
git clone <your-repo-url>
cd hotel-booking-etl
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

`.env` format:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=hotel_datamart
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/
```

3. **Setup MongoDB Atlas**:
- Create free account at https://www.mongodb.com/cloud/atlas
- Create M0 cluster
- Database Access: Add user with read/write permissions
- Network Access: Allow 0.0.0.0/0
- Get connection string and add to `.env`

4. **Create MySQL database**:
```sql
CREATE DATABASE hotel_datamart;
```

5. **Run the pipeline**:
```bash
python scripts/setup_mongodb.py    # Populate MongoDB source
python scripts/etl_pipeline.py     # Run ETL
```

6. **Verify with queries**:
```bash
mysql -u root -p hotel_datamart < scripts/queries.sql
```

---

## Project Structure

```
hotel-booking-etl/
├── scripts/
│   ├── etl_pipeline.py          # Main ETL script
│   ├── setup_mongodb.py         # MongoDB initialization
│   ├── schema.sql               # Table definitions
│   └── queries.sql              # Analytical queries
├── data/csv/
│   ├── guests.csv               # 3 guest records
│   ├── rooms.csv                # 3 room records
│   └── bookings.csv             # 3 booking records
├── .env                         # Credentials (not in Git)
├── .env.example                 # Template
├── requirements.txt             # Dependencies
└── README.md
```

---

## Data Flow

```
SOURCES → TRANSFORM → LOAD

CSV Files          ┐
MongoDB (hotels)   ├→ ETL Pipeline → MySQL Star Schema
Date Generation    ┘
```

**Extract**: 3 guests, 3 rooms, 3 bookings (CSV) + 3 hotels (MongoDB) + 3 dates (Python)  
**Transform**: Calculate revenue, drop columns, validate integrity  
**Load**: 5 tables in MySQL (date, guest, room, hotel, bookings)

---

## Star Schema

```
       date
        │
   ┌────┼────┐
guest-bookings-hotel
        │
       room
```

**Fact Table**: `bookings` (booking_id, date_id, guest_id, room_id, hotel_id, nights_stayed, total_amount)

**Dimensions**:
- `date`: date_id, date, day, month, year, quarter, day_name, month_name
- `guest`: guest_id, guest_name, email, country
- `room`: room_id, room_type, price_per_night, capacity
- `hotel`: hotel_id, hotel_name, location, star_rating

---

## Sample Queries

**Query 1: Revenue by Hotel**
```sql
SELECT h.hotel_name, SUM(b.total_amount) AS total_revenue
FROM bookings b
JOIN hotel h ON b.hotel_id = h.hotel_id
GROUP BY h.hotel_name;
```

**Query 2: Average Stay by Room Type**
```sql
SELECT r.room_type, AVG(b.nights_stayed) AS avg_stay
FROM bookings b
JOIN room r ON b.room_id = r.room_id
GROUP BY r.room_type;
```

**Query 3: Bookings by Quarter**
```sql
SELECT d.quarter, COUNT(b.booking_id) AS booking_count
FROM bookings b
JOIN date d ON b.date_id = d.date_id
GROUP BY d.quarter;
```

---

## Technology Stack

- **Python 3.8+**: ETL pipeline
- **MySQL 8.0+**: Data mart
- **MongoDB Atlas**: NoSQL source
- **Libraries**: pandas, pymongo, pymysql, SQLAlchemy, python-dotenv

---

## Troubleshooting

**MongoDB connection error**: 
- Verify MONGODB_URI in `.env`
- Replace `<password>` with actual password
- Check Network Access in Atlas allows 0.0.0.0/0

**MySQL connection refused**:
- Ensure MySQL is running
- Verify credentials in `.env`
- Check database exists: `CREATE DATABASE hotel_datamart;`

**Module not found**:
```bash
pip install -r requirements.txt
```

**Empty MongoDB**:
```bash
python scripts/setup_mongodb.py
```

---

## Deployment

**Current**: Local MySQL + Cloud MongoDB Atlas + Local Python

