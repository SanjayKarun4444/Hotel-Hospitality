SELECT 
    d.quarter,
    d.year,
    COUNT(b.booking_id) AS booking_count,
    SUM(b.total_amount) AS quarter_revenue
FROM bookings b
JOIN date d ON b.date_id = d.date_id
GROUP BY d.quarter, d.year