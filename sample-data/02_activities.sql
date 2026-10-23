-- Run 01_users.sql first. Dates are fixed for predictable frontend testing.
USE trackerdb;

-- Replace only these demo users' records on the three sample dates so reruns
-- do not duplicate the sample data. Other users and dates are untouched.
START TRANSACTION;

DELETE a FROM activities AS a
JOIN login AS u ON u.id = a.user_id
WHERE u.username IN ('demo_alex', 'demo_sam')
  AND a.recorded_at >= '2026-10-21 00:00:00'
  AND a.recorded_at < '2026-10-24 00:00:00';

INSERT INTO activities (user_id, recorded_at, app, title)
SELECT u.id, sample.recorded_at, sample.app, sample.title
FROM login AS u
JOIN (
    SELECT 'demo_alex' AS username, '2026-10-21 09:00:00' AS recorded_at, 'IntelliJ IDEA' AS app, 'Designing the database schema' AS title
    UNION ALL SELECT 'demo_alex', '2026-10-21 09:01:00', 'IntelliJ IDEA', 'Designing the database schema'
    UNION ALL SELECT 'demo_alex', '2026-10-21 09:02:00', 'IntelliJ IDEA', 'Designing the database schema'
    UNION ALL SELECT 'demo_alex', '2026-10-21 09:15:00', 'Chrome', 'Reading MySQL documentation'
    UNION ALL SELECT 'demo_alex', '2026-10-21 10:30:00', 'Terminal', 'Running database queries'
    UNION ALL SELECT 'demo_alex', '2026-10-21 14:00:00', 'Figma', 'Sketching the calendar layout'
    UNION ALL SELECT 'demo_alex', '2026-10-22 08:45:00', 'Chrome', 'Reading servlet documentation'
    UNION ALL SELECT 'demo_alex', '2026-10-22 09:00:00', 'IntelliJ IDEA', 'Building the activities servlet'
    UNION ALL SELECT 'demo_alex', '2026-10-22 09:01:00', 'IntelliJ IDEA', 'Building the activities servlet'
    UNION ALL SELECT 'demo_alex', '2026-10-22 09:02:00', 'IntelliJ IDEA', 'Building the activities servlet'
    UNION ALL SELECT 'demo_alex', '2026-10-22 12:00:00', 'Notes', NULL
    UNION ALL SELECT 'demo_alex', '2026-10-22 15:30:00', 'Chrome', 'Testing the calendar frontend'
    UNION ALL SELECT 'demo_alex', '2026-10-22 23:59:59', 'Terminal', 'Checking the end-of-day boundary'
    UNION ALL SELECT 'demo_alex', '2026-10-23 00:00:00', 'Terminal', 'Checking the start-of-day boundary'
    UNION ALL SELECT 'demo_alex', '2026-10-23 09:00:00', 'IntelliJ IDEA', 'Connecting the frontend to the API'
    UNION ALL SELECT 'demo_alex', '2026-10-23 09:01:00', 'IntelliJ IDEA', 'Connecting the frontend to the API'
    UNION ALL SELECT 'demo_alex', '2026-10-23 09:02:00', 'IntelliJ IDEA', 'Connecting the frontend to the API'
    UNION ALL SELECT 'demo_alex', '2026-10-23 09:20:00', 'Chrome', 'Reviewing JSON responses'
    UNION ALL SELECT 'demo_alex', '2026-10-23 10:00:00', 'Notes', 'Planning: filters, colors, and empty days'
    UNION ALL SELECT 'demo_alex', '2026-10-23 11:30:00', 'Chrome', 'A long activity title to check how the calendar handles text wrapping when a record contains more detail than fits in a single line'
    UNION ALL SELECT 'demo_alex', '2026-10-23 14:00:00', 'Terminal', 'Running a query for Alex''s activities'
    UNION ALL SELECT 'demo_alex', '2026-10-23 14:00:00', 'Chrome', 'A second observation at the same timestamp'
    UNION ALL SELECT 'demo_sam', '2026-10-21 10:00:00', 'Chrome', 'Researching calendar interfaces'
    UNION ALL SELECT 'demo_sam', '2026-10-21 11:00:00', 'Notes', 'Writing project notes'
    UNION ALL SELECT 'demo_sam', '2026-10-22 09:00:00', 'Visual Studio Code', 'Styling the calendar'
    UNION ALL SELECT 'demo_sam', '2026-10-22 09:01:00', 'Visual Studio Code', 'Styling the calendar'
    UNION ALL SELECT 'demo_sam', '2026-10-22 13:00:00', 'Chrome', 'Checking the mobile layout'
    UNION ALL SELECT 'demo_sam', '2026-10-23 09:00:00', 'Figma', 'Choosing activity colors'
    UNION ALL SELECT 'demo_sam', '2026-10-23 10:15:00', 'Notes', NULL
    UNION ALL SELECT 'demo_sam', '2026-10-23 16:00:00', 'Chrome', 'Reviewing the finished calendar'
) AS sample ON sample.username = u.username;

COMMIT;

-- View sample records, including the generated user IDs:
SELECT u.id AS user_id, u.username, a.id AS activity_id,
       a.recorded_at, a.app, a.title
FROM activities AS a
JOIN login AS u ON u.id = a.user_id
WHERE u.username IN ('demo_alex', 'demo_sam')
  AND a.recorded_at >= '2026-10-21 00:00:00'
  AND a.recorded_at < '2026-10-24 00:00:00'
ORDER BY u.username, a.recorded_at, a.id;
