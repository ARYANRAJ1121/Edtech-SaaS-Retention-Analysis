-- ============================================
-- Churn definition based on inactivity window
-- Business rule:
-- A user is churned if inactive for 30+ days
-- ============================================

WITH last_activity AS (
    SELECT
        user_id,
        MAX(event_date) AS last_activity_date
    FROM usage_events
    GROUP BY user_id
),
reference_date AS (
    SELECT MAX(event_date) AS snapshot_date
    FROM usage_events
)
SELECT
    l.user_id,
    l.last_activity_date,
    r.snapshot_date,
    (r.snapshot_date - l.last_activity_date) AS days_since_last_activity,
    CASE
        WHEN (r.snapshot_date - l.last_activity_date) >= 30 THEN 1
        ELSE 0
    END AS churned
FROM last_activity l
CROSS JOIN reference_date r;
