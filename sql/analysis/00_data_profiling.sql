-- ============================================
-- Basic data profiling
-- ============================================

SELECT COUNT(*) AS total_users FROM users;

SELECT COUNT(*) AS total_events FROM usage_events;

SELECT
    MIN(event_date) AS min_event_date,
    MAX(event_date) AS max_event_date
FROM usage_events;

SELECT
    AVG(sessions) AS avg_sessions_per_day,
    MAX(sessions) AS max_sessions
FROM usage_events;
