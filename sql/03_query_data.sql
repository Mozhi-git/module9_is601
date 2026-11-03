
-- Module 9: Retrieve data from PostgreSQL

-- Show all users
SELECT * FROM users;

-- Show all calculations
SELECT * FROM calculations;

-- Connect users with their calculations
SELECT
    u.username,
    c.operation,
    c.operand_a,
    c.operand_b,
    c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;
