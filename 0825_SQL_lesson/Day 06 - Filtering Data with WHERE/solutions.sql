-- Solutions for Day 6: Filtering Data with WHERE

-- 1. Find all customers in the city of 'Berlin'.
SELECT * FROM Customers
WHERE City = 'Berlin';

-- 2. Find all customers in Mexico.
SELECT * FROM Customers
WHERE Country = 'Mexico';

-- 3. Find all products with a price greater than 20.
SELECT * FROM Products
WHERE Price > 20;

-- 4. Find all products with a price less than or equal to 15.
SELECT * FROM Products
WHERE Price <= 15;

-- 5. Find all orders that were placed on or after July 8th, 1996.
SELECT * FROM Orders
WHERE OrderDate >= '1996-07-08';

-- 6. Find all products with a ProductName that contains the word 'syrup'.
SELECT * FROM Products
WHERE ProductName LIKE '%syrup%';

-- 7. Find all customers with a PostalCode that starts with '0'.
SELECT * FROM Customers
WHERE PostalCode LIKE '0%';

-- 8. Find all orders from EmployeeID 4 or 5.
SELECT * FROM Orders
WHERE EmployeeID IN (4, 5);
