-- Total Revenue by Hotel
SELECT h.hotel_name, SUM(b.total_amount) AS total_revenue
FROM bookings b
JOIN hotel h ON b.hotel_id = h.hotel_id
GROUP BY h.hotel_name;

-- Average Stay by Room Type
SELECT r.room_type, AVG(b.nights_stayed) AS avg_stay
FROM bookings b
JOIN room r ON b.room_id = r.room_id
GROUP BY r.room_type;

-- Bookings Trend by Quarter
SELECT d.quarter, COUNT(b.booking_id) AS booking_count
FROM bookings b
JOIN date d ON b.date_id = d.date_id
GROUP BY d.quarter;
