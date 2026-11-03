
-- Module 9: Update and delete calculation records

-- Update the result of calculation ID 1
UPDATE calculations
SET result = 6
WHERE id = 1;

-- Delete calculation ID 2
DELETE FROM calculations
WHERE id = 2;
