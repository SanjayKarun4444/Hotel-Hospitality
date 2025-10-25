-- Date Dimension
CREATE TABLE date (
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
CREATE TABLE guest (
    guest_id INT PRIMARY KEY,
    guest_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50)
);

-- Room Dimension
CREATE TABLE room (
    room_id INT PRIMARY KEY,
    room_type VARCHAR(50),
    price_per_night DECIMAL(10, 2),
    capacity INT
);

-- Hotel Dimension
CREATE TABLE hotel (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR(100),
    location VARCHAR(100),
    star_rating INT
);

-- Fact Table: Bookings
CREATE TABLE bookings (
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
