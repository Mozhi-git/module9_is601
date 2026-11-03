
-- Module 9: Insert sample users and calculations

-- Add two users
INSERT INTO users (username, email)
VALUES
    ('alice', 'alice@example.com'),
    ('bob', 'bob@example.com');

-- Add three calculations linked to their users
INSERT INTO calculations
    (operation, operand_a, operand_b, result, user_id)
VALUES
    ('add', 2, 3, 5,
        (SELECT id FROM users WHERE username = 'alice')),
    ('divide', 10, 2, 5,
        (SELECT id FROM users WHERE username = 'alice')),
    ('multiply', 4, 5, 20,
        (SELECT id FROM users WHERE username = 'bob'));
