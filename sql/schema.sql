-- ============================================
-- Schema definition for EdTech SaaS retention
-- ============================================

DROP TABLE IF EXISTS usage_events;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date DATE NOT NULL,
    acquisition_channel TEXT,
    country TEXT
);

CREATE TABLE usage_events (
    user_id INT REFERENCES users(user_id),
    event_date DATE NOT NULL,
    sessions INT NOT NULL,
    PRIMARY KEY (user_id, event_date)
);
