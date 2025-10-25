
## Setup Instructions

### Prerequisites
- MySQL Server
- Python 3.x
- Required Python packages: `pandas`, `sqlalchemy`, `pymysql`

### Steps
1. **Set up MySQL Database:**
   - Create the `hotel_datamart` database:
     ```sql
     CREATE DATABASE hotel_datamart;
     USE hotel_datamart;
     ```

2. **Create Tables:**
   - Run the `schema.sql` script to create tables:
     ```bash
     mysql -u root -p hotel_datamart < scripts/schema.sql
     ```

3. **Run ETL Script:**
   - Execute the ETL script to load data from CSV files:
     ```bash
     python scripts/etl_pipeline.py
     ```

4. **Insert Sample Data:**
   - Run the `insert_data.sql` script to insert sample data for `date` and `hotel` tables:
     ```bash
     mysql -u root -p hotel_datamart < scripts/insert_data.sql
     ```

5. **Run Analysis Queries:**
   - Execute the analysis queries in `queries.sql`:
     ```bash
     mysql -u root -p hotel_datamart
     ```
     Copy and paste the queries from `scripts/queries.sql`.

## ETL Process
- **Extract:** Data is extracted from CSV files (`guests.csv`, `rooms.csv`, `bookings.csv`).
- **Transform:** The `total_amount` for bookings is calculated.
- **Load:** Data is loaded into the MySQL database.

## Analysis Queries
- **Total Revenue by Hotel:** Calculates the total revenue for each hotel.
- **Average Stay by Room Type:** Calculates the average stay duration for each room type.
- **Bookings Trend by Quarter:** Counts the number of bookings per quarter.

## Documentation
- **Schema:** Defined in `schema.sql`.
- **Sample Data:** Provided in CSV files and `insert_data.sql`.
- **ETL Script:** `etl_pipeline.py`.
- **Analysis Queries:** `queries.sql`.
