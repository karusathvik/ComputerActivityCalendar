-- Run this file first, after creating your tables.
USE trackerdb;

-- These placeholder values are not valid password hashes or login credentials.
-- They let you test activity queries without implementing authentication.
INSERT INTO login (username, password)
VALUES
    ('demo_alex', 'TEST_ONLY_NO_VALID_PASSWORD_HASH'),
    ('demo_sam', 'TEST_ONLY_NO_VALID_PASSWORD_HASH')
ON DUPLICATE KEY UPDATE username = VALUES(username);
