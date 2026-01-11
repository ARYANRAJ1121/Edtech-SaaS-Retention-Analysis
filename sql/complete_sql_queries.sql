/* ============================================================
   Project: EdTech SaaS Retention & Churn Risk Analysis
   File: complete_sql_queries.sql

   Purpose:
   This file contains the complete SQL analytics pipeline used to:
   1. Profile raw user and usage data
   2. Define churn based on behavioral inactivity
   3. Engineer ML-ready features at the user level

   Notes:
   - Queries are written in execution order
   - Churn is defined using a 30-day inactivity window
   - No future data leakage is introduced
   - Final output feeds the ML churn risk model

   Author: Aryan Raj
   ============================================================ */


-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date DATE NOT NULL,
    acquisition_channel TEXT,
    country TEXT
);

-- USAGE EVENTS TABLE
CREATE TABLE usage_events (
    user_id INT REFERENCES users(user_id),
    event_date DATE NOT NULL,
    sessions INT NOT NULL,
    PRIMARY KEY (user_id, event_date)
);

TRUNCATE TABLE users CASCADE;

COPY users (user_id, signup_date, acquisition_channel, country)
FROM 'C:/temp/edtech_data/users.csv'
DELIMITER ','
CSV HEADER;


COPY usage_events (user_id, event_date, sessions)
FROM 'C:/temp/edtech_data/usage_events.csv'
DELIMITER ','
CSV HEADER;


SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM usage_events;
SELECT * FROM usage_events;
SELECT * FROM users;


-- Understand user behavior (before talking about churn)
SELECT
    user_id,
    MIN(event_date) AS first_activity_date,
    MAX(event_date) AS last_activity_date,
    COUNT(*)        AS active_days
FROM usage_events
GROUP BY user_id
ORDER BY active_days DESC
LIMIT 10;

-- How many users barely engaged at all?
SELECT
    active_days,
    COUNT(*) AS users
FROM (
    SELECT user_id, COUNT(*) AS active_days
    FROM usage_events
    GROUP BY user_id
) t
GROUP BY active_days
ORDER BY active_days ASC
LIMIT 15;

-- How many users truly stop engaging for 28+ days?
WITH ordered_events AS (
    SELECT
        user_id,
        event_date,
        LEAD(event_date) OVER (
            PARTITION BY user_id
            ORDER BY event_date
        ) AS next_event_date
    FROM usage_events
),
gaps AS (
    SELECT
        user_id,
        event_date,
        next_event_date,
        next_event_date - event_date AS gap_days
    FROM ordered_events
)
SELECT
    COUNT(DISTINCT user_id) AS churned_users
FROM gaps
WHERE gap_days >= 28;


-- create behavioral features.
WITH analysis_date AS (
    SELECT MAX(event_date) AS max_date
    FROM usage_events
)
SELECT
    u.user_id,
    COUNT(e.event_date)              AS active_days,
    MAX(e.event_date)                AS last_active_date,
    a.max_date - MAX(e.event_date)   AS days_since_last_activity,
    AVG(e.sessions)                  AS avg_sessions_per_day,
    SUM(e.sessions)                  AS total_sessions
FROM users u
LEFT JOIN usage_events e
    ON u.user_id = e.user_id
CROSS JOIN analysis_date a
GROUP BY u.user_id, a.max_date;

-- Create churn labels

WITH ordered_events AS (
    SELECT
        user_id,
        event_date,
        LEAD(event_date) OVER (
            PARTITION BY user_id
            ORDER BY event_date
        ) AS next_event_date
    FROM usage_events
),
gaps AS (
    SELECT
        user_id,
        event_date,
        next_event_date,
        next_event_date - event_date AS gap_days
    FROM ordered_events
),
churned_users AS (
    SELECT DISTINCT user_id
    FROM gaps
    WHERE gap_days >= 28
)
SELECT
    u.user_id,
    CASE
        WHEN c.user_id IS NOT NULL THEN 1
        ELSE 0
    END AS churned
FROM users u
LEFT JOIN churned_users c
    ON u.user_id = c.user_id;

-- Join features + labels (this is the ML handoff point)
WITH analysis_date AS (
    SELECT MAX(event_date) AS max_date
    FROM usage_events
),
features AS (
    SELECT
        u.user_id,
        COUNT(e.event_date)              AS active_days,
        MAX(e.event_date)                AS last_active_date,
        a.max_date - MAX(e.event_date)   AS days_since_last_activity,
        AVG(e.sessions)                  AS avg_sessions_per_day,
        SUM(e.sessions)                  AS total_sessions
    FROM users u
    LEFT JOIN usage_events e
        ON u.user_id = e.user_id
    CROSS JOIN analysis_date a
    GROUP BY u.user_id, a.max_date
),
churn_labels AS (
    SELECT DISTINCT user_id
    FROM (
        SELECT
            user_id,
            event_date,
            LEAD(event_date) OVER (
                PARTITION BY user_id
                ORDER BY event_date
            ) AS next_event_date
        FROM usage_events
    ) t
    WHERE next_event_date - event_date >= 28
)
SELECT
    f.*,
    CASE
        WHEN c.user_id IS NOT NULL THEN 1
        ELSE 0
    END AS churned
FROM features f
LEFT JOIN churn_labels c
    ON f.user_id = c.user_id;


