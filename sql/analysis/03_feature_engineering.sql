-- ============================================
-- ML-ready churn feature table
-- ============================================

WITH user_aggregates AS (
    SELECT
        u.user_id,
        COUNT(DISTINCT e.event_date) AS active_days,
        SUM(e.sessions) AS total_sessions,
        AVG(e.sessions::FLOAT) AS avg_sessions_per_day,
        MAX(e.event_date) AS last_active_date
    FROM users u
    LEFT JOIN usage_events e
        ON u.user_id = e.user_id
    GROUP BY u.user_id
),
snapshot AS (
    SELECT MAX(event_date) AS snapshot_date
    FROM usage_events
)
SELECT
    ua.user_id,
    ua.active_days,
    ua.last_active_date,
    (s.snapshot_date - ua.last_active_date) AS days_since_last_activity,
    ua.avg_sessions_per_day,
    ua.total_sessions,
    CASE
        WHEN (s.snapshot_date - ua.last_active_date) >= 30 THEN 1
        ELSE 0
    END AS churned
FROM user_aggregates ua
CROSS JOIN snapshot s;
