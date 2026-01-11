-- ============================================
-- User activity lifecycle summary
-- ============================================

SELECT
    u.user_id,
    MIN(e.event_date) AS first_activity_date,
    MAX(e.event_date) AS last_activity_date,
    COUNT(DISTINCT e.event_date) AS active_days,
    SUM(e.sessions) AS total_sessions
FROM users u
LEFT JOIN usage_events e
    ON u.user_id = e.user_id
GROUP BY u.user_id;
