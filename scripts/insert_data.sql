-- Insert sample data into date
INSERT INTO date (date_id, date, day, month, year, quarter, day_name, month_name)
VALUES
(1, '2023-01-15', 15, 1, 2023, 1, 'Sunday', 'January'),
(2, '2023-02-20', 20, 2, 2023, 1, 'Monday', 'February'),
(3, '2023-03-25', 25, 3, 2023, 1, 'Saturday', 'March');

-- Insert sample data into guest
INSERT INTO guest (guest_id, guest_name, email, country)
VALUES
(1, 'John Doe', 'john@example.com', 'USA'),
(2, 'Jane Smith', 'jane@example.com', 'Canada'),
(3, 'Alice Johnson', 'alice@example.com', 'UK');

-- Insert sample data into room
INSERT INTO room (room_id, room_type, price_per_night, capacity)
VALUES
(1, 'Standard', 100.00, 2),
(2, 'Deluxe', 150.00, 2),
(3, 'Suite', 250.00, 4);

-- Insert sample data into hotel
INSERT INTO hotel (hotel_id, hotel_name, location, star_rating)
VALUES
(1, 'Grand Hotel', 'New York', 5),
(2, 'Ocean View', 'Miami', 4);

-- Insert sample data into bookings
INSERT INTO bookings (booking_id, date_id, guest_id, room_id, hotel_id, nights_stayed, total_amount)
VALUES
(1, 1, 1, 1, 1, 2, 200.00),
(2, 2, 2, 2, 1, 3, 450.00),
(3, 3, 3, 3, 2, 1, 250.00);
