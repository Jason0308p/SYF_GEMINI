-- Day 3: Creating Tables

CREATE TABLE Customers (
    CustomerID int,
    CustomerName varchar(255),
    ContactName varchar(255),
    Address varchar(255),
    City varchar(255),
    PostalCode varchar(255),
    Country varchar(255)
);

CREATE TABLE Products (
    ProductID int,
    ProductName varchar(255),
    SupplierID int,
    CategoryID int,
    Unit varchar(255),
    Price int
);

CREATE TABLE Orders (
    OrderID int,
    CustomerID int,
    EmployeeID int,
    OrderDate date,
    ShipperID int
);
