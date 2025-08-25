-- Examples for Day 6: Filtering Data with WHERE

-- Find all customers in Germany
SELECT * FROM Customers
WHERE Country = 'Germany';

-- Find all customers with a CustomerID greater than 10
SELECT * FROM Customers
WHERE CustomerID > 10;

-- Find all products with a price between 10 and 20
SELECT * FROM Products
WHERE Price BETWEEN 10 AND 20;

-- Find all products with a ProductName that starts with 'Ch'
SELECT * FROM Products
WHERE ProductName LIKE 'Ch%';

-- Find all orders from customers with CustomerID 1, 3, or 5
SELECT * FROM Orders
WHERE CustomerID IN (1, 3, 5);
