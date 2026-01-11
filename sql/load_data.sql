-- ============================================
-- Load CSV data into PostgreSQL
-- ============================================

-- Adjust paths if needed
COPY users(user_id, signup_date, acquisition_channel, country)
FROM 'C:/temp/edtech_data/users.csv'
DELIMITER ','
CSV HEADER;

COPY usage_events(user_id, event_date, sessions)
FROM 'C:/temp/edtech_data/usage_events.csv'
DELIMITER ','
CSV HEADER;
