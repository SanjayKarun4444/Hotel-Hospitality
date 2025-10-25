USE hotel_datamart;

-- Date Dimension
CREATE TABLE IF NOT EXISTS date (
    date_id INT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT,
    quarter INT,
    day_name VARCHAR(10),
    month_name VARCHAR(10)
);

-- Guest Dimension
CREATE TABLE IF NOT EXISTS guest (
    guest_id INT PRIMARY KEY,
    guest_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50)
);

-- Room Dimension
CREATE TABLE IF NOT EXISTS room (
    room_id INT PRIMARY KEY,
    room_type VARCHAR(50),
    price_per_night DECIMAL(10, 2),
    capacity INT
);

-- Hotel Dimension
CREATE TABLE IF NOT EXISTS hotel (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR(100),
    location VARCHAR(100),
    star_rating INT
);

-- Fact Table: Bookings
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT PRIMARY KEY,
    date_id INT,
    guest_id INT,
    room_id INT,
    hotel_id INT,
    nights_stayed INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (date_id) REFERENCES date(date_id),
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id),
    FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id)
);

-- Insert sample data into date
INSERT INTO date (date_id, date, day, month, year, quarter, day_name, month_name)
VALUES
(1, '2023-01-15', 15, 1, 2023, 1, 'Sunday', 'January'),
(2, '2023-02-20', 20, 2, 2023, 1, 'Monday', 'February'),
(3, '2023-03-25', 25, 3, 2023, 1, 'Saturday', 'March');

-- Insert sample data into hotel
INSERT INTO hotel (hotel_id, hotel_name, location, star_rating)
VALUES
(1, 'Grand Hotel', 'New York', 5),
(2, 'Ocean View', 'Miami', 4);


SHOW TABLES;

SELECT * FROM date;
SELECT * FROM guest;
SELECT * FROM room;
SELECT * FROM hotel;
SELECT * FROM bookings;
